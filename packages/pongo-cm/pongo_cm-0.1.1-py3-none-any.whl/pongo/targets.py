# Copyright 2022 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from importlib import metadata
import contextlib
import dataclasses
import functools
import io
import itertools
import logging
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import typing as t


import pongo
import pongo.connect
import pongo.indentedtext
import pongo.run

logger = logging.getLogger(__name__)

timeout = 15

ScriptdirTargets = dict[pathlib.Path, dict[str, "Target"]]


class TargetNotFound(Exception):
    """
    The specified target could not be found
    """


class Scriptdir(pathlib.Path):

    _flavour = pathlib.Path()._flavour  # type: ignore

    @property
    def remote_path(self):
        return pathlib.Path(f"{self.name}-{hex(hash(str(self)))[-6:]}")


@dataclasses.dataclass
class Target:
    id: int = dataclasses.field(init=False)
    name: str
    scriptdir: t.Optional[Scriptdir] = None
    script: t.Optional[str] = None
    before: list[str] = dataclasses.field(default_factory=list)
    after: list[str] = dataclasses.field(default_factory=list)
    interpreter: str = "/bin/sh"
    args: t.Optional[str] = None
    arg: list[str] = dataclasses.field(default_factory=list)
    user: str = "root"
    pipe_from: t.Optional[str] = None
    local: bool = False
    message: t.Optional[str] = None
    confirm: t.Optional[str] = None
    env: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self, counter=itertools.count()):
        assert re.match(r"^[a-zA-Z_\-0-9.]+$", self.name)
        self.id = next(counter)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and (self.name, self.scriptdir) == (
            other.name,
            other.scriptdir,
        )

    def __hash__(self):
        return hash((self.name, self.scriptdir))

    @property
    def path(self):
        return pathlib.Path(f"{self.id:002d}.{self.name}")

    def get_args(self):
        if self.args is not None:
            args = shlex.split(self.args)
        else:
            args = []
        args.extend(self.arg)
        return args


def run_targets(targets, context, host, term_color, logdir):
    """
    Run a list of targets in order
    """
    # Open an SSH ControlMaster to the server.
    ssh = context["PONGO_SSH"]
    user = context["PONGO_CONNECT_USER"]
    hostname = context["PONGO_HOSTNAME"]

    logger.info(f"Sending log output to {logdir}/")
    with (pathlib.Path(logdir) / f"{host}.log").open("wb") as logfile:
        with pongo.connect.connect_ssh(ssh=ssh, user=user, hostname=hostname) as (
            controlpath,
            _,
        ):
            logger.debug("Opened connection, waiting for ControlPath")
            run_ssh = functools.partial(
                pongo.connect.run_ssh,
                ssh=ssh,
                controlpath=controlpath,
                hostname=hostname,
                user=user,
                stdin=subprocess.PIPE,
            )
            with create_staging_dir(run_ssh, targets, context) as (
                remote_staging,
                local_staging,
            ):
                for pipegroup in targets:
                    result = _run_single_target(
                        context,
                        host,
                        run_ssh,
                        remote_staging,
                        local_staging,
                        pipegroup,
                        term_color,
                        logfile,
                    )
                    if not result:
                        break


def _run_single_target(
    context,
    host: str,
    run_ssh: t.Callable,
    remote_staging,
    local_staging,
    pipegroup,
    term_color,
    logfile,
):
    """
    Run a PipeGroup on host inside the existing staging dir.
    Does not care about any ``before`` dependencies.
    """
    if sys.stdout.isatty():
        out_prefix = f"\033[3{term_color}m{host}:\033[0m ".encode("utf-8")
    else:
        out_prefix = b""

    sudo = context["PONGO_SUDO"]
    render = functools.partial(pongo.render_jinja, environ=context)
    processes = []
    for target in pipegroup:
        if target.confirm:
            print(target.confirm)
            if input("Continue? [yn] ").strip().lower not in {"y", "yes"}:
                return False
    for target in pipegroup:
        interpreter = render(target.interpreter)
        runas = render(target.user)
        argstr = shlex.join(map(render, target.get_args()))
        env = shlex.join(map(render, target.env))
        staging_dir = local_staging if target.local else remote_staging

        if target.script:
            command = f"{interpreter} {target.path} {argstr}"
            command = f'env "PATH=$PATH:{staging_dir}/bin" {env} {command}'
            if sudo and runas and not target.local:
                command = f"{shlex.quote(sudo)} -u {shlex.quote(runas)} {command}"
            command = f"cd {shlex.quote(str(staging_dir / target.scriptdir.remote_path))} && {command}"
            if target.local:
                runner = functools.partial(pongo.connect.run_local, command)
            else:
                runner = functools.partial(run_ssh, command=command)
            logger.debug(render(target.script))
            logger.debug(command)
            processes.append(runner())

    stdin = os.fdopen(os.dup(sys.stdin.fileno()), "rb", buffering=0)
    stdout = os.fdopen(os.dup(sys.stdout.fileno()), "wb", buffering=0)
    stderr = os.fdopen(os.dup(sys.stdout.fileno()), "wb", buffering=0)
    prefixed_stdout = PrefixedIO(out_prefix, stdout)
    pongo.run.pipe(processes, in_=stdin, out=prefixed_stdout, err=stderr)

    for target in pipegroup:
        if target.message:
            prefixed_stdout.write(b"\n")
            prefixed_stdout.write(target.message.encode("utf8"))
    sys.stdout.flush()
    return True


def load_targets(path: pathlib.Path) -> dict[str, Target]:
    path = path.resolve()
    with (path / "Pongofile").open("r", encoding="utf8") as f:
        targets = pongo.targets.parse_targets(pongo.indentedtext.parse_lines(f))
        for name in targets:
            targets[name].scriptdir = Scriptdir(path)
    return targets


def resolve_target(
    scriptdirs: ScriptdirTargets,
    scriptbase: t.Optional[pathlib.Path],
    relativeto: t.Optional[pathlib.Path],
    n: str,
) -> Target:
    """
    Resolve a name to a target.

    Mutates ``scriptdirs`` to include newly loaded scripts.
    """
    if ":" in n:
        scriptdir, name = n.split(":", 1)

        for base in [relativeto, scriptbase]:
            if base is None:
                continue
            trypath = (base / scriptdir).resolve()
            if trypath in scriptdirs:
                if name in scriptdirs[trypath]:
                    return scriptdirs[trypath][name]

            elif (trypath / "Pongofile").is_file():
                parsed = load_targets(trypath)
                scriptdirs[trypath] = parsed
                if name in parsed:
                    return parsed[name]
                parse_targets
        raise TargetNotFound(n)

    if relativeto is not None:
        try:
            return scriptdirs[relativeto][n]
        except KeyError:
            raise TargetNotFound(n)

    raise TargetNotFound(n)


def gather_target_scripts(
    scriptbase: pathlib.Path,
    scriptdirs: ScriptdirTargets,
    path: t.Optional[pathlib.Path],
    name: str,
) -> list["PipeGroup"]:
    before = []
    after = []
    target = resolve_target(scriptdirs, scriptbase, path, name)

    def dedup(items):
        deduped = []
        seen = set()
        for pipegroup in items:
            if tuple(pipegroup) not in seen:
                deduped.append(pipegroup)
                seen.add(tuple(pipegroup))
        return deduped

    for n in target.before:
        before.extend(
            gather_target_scripts(scriptbase, scriptdirs, target.scriptdir, n)
        )
    for n in target.after:
        after.extend(gather_target_scripts(scriptbase, scriptdirs, target.scriptdir, n))

    group = PipeGroup([target])
    if target.pipe_from:
        t_ = target
        while t_.pipe_from:
            for n in t_.before:
                before.extend(
                    gather_target_scripts(scriptbase, scriptdirs, t_.scriptdir, n)
                )
            for n in t_.after:
                after.extend(
                    gather_target_scripts(scriptbase, scriptdirs, t_.scriptdir, n)
                )
            t_ = resolve_target(scriptdirs, scriptbase, path, t_.pipe_from)
            group.insert(0, t_)

    return dedup(before) + [group] + dedup(after)


class PipeGroup(list):
    """
    A list of :class:`Target` objects which will be executed by piping the
    output of one to the next.
    """


@contextlib.contextmanager
def create_staging_dir(run_ssh, targets, context):
    """
    Yield the paths to the staging directory on both remote and local machines
    """
    # run mktemp on destination
    proc = run_ssh(command='mktemp -d -t "pongo-staging"', stdin=subprocess.DEVNULL)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise
    if proc.returncode != 0:
        raise pongo.connect.ConnectionError(
            f"Could not create staging directory: got exit status {proc.returncode}"
        )
    remote_staging = out.decode("ascii").strip()
    assert remote_staging != ""
    paths = metadata.files("pongo")
    if paths:
        distfiles = {str(path): path for path in paths}
    else:
        distfiles = {}

    with tempfile.TemporaryDirectory() as local_staging:
        for distfile in ["pongo/scripts/rsub", "pongo/scripts/rinstall"]:
            path = distfiles[distfile].locate()
            assert isinstance(path, pathlib.Path)
            dest = pathlib.Path(local_staging) / "bin" / path.name
            dest.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy(path, dest)
            shutil.copymode(path, dest)

        for pipegroup in targets:
            for target in pipegroup:
                scriptf = (
                    pathlib.Path(local_staging)
                    / target.scriptdir.remote_path
                    / target.path
                )
                logger.info(f"Writing to {scriptf}")
                scriptf.parent.mkdir(exist_ok=True, parents=True)
                scriptf.write_bytes(
                    pongo.render_jinja(target.script, context).encode("utf8")
                )

        for scriptdir in {t.scriptdir for pipegroup in targets for t in pipegroup}:
            for dirpath, dirnames, filenames in os.walk(scriptdir):
                dirpath = pathlib.Path(dirpath)
                p = (
                    pathlib.Path(local_staging)
                    / scriptdir.remote_path
                    / dirpath.relative_to(scriptdir)
                )
                p.mkdir(parents=True, exist_ok=True)
                shutil.copymode(dirpath, p)
                for f in filenames:
                    if f.endswith("j2"):
                        destf = pathlib.Path(f).stem
                        template = (dirpath / f).read_text(encoding="utf8")
                        (p / destf).write_text(
                            pongo.render_jinja(template, context), encoding="utf8"
                        )
                        shutil.copymode(dirpath / f, p / destf)
                    else:
                        shutil.copy(dirpath / f, p / f)
                        shutil.copymode(dirpath / f, p / f)

        tar = subprocess.Popen(
            ["tar", "-C", local_staging, "-cf", "-", "."], stdout=subprocess.PIPE
        )
        untar = run_ssh(command=f"tar -C '{remote_staging}' -xf -")
        pongo.run.pipe([tar, untar])
        yield remote_staging, local_staging

    proc = run_ssh(command=f'rm -rf "{remote_staging}"', stdin=subprocess.DEVNULL)
    out, err = proc.communicate(timeout=timeout)


def parse_targets(indentedtext):
    targets = {}
    fields = {f.name: f for f in dataclasses.fields(Target)}
    for name, definition in indentedtext:
        kwargs = {
            k.replace("-", "_"): v for k, v in nestedliststodict(definition).items()
        }
        for k, v in list(kwargs.items()):
            f = fields[k]
            if f.type != list[str]:
                kwargs[k] = v[0]

        target = Target(name=name, **kwargs)
        targets[name] = target
    return targets


def nestedliststodict(items):
    """
    Transform ``[(a, b), (c, [(d, e)])]`` into
    {a: [b], c: [{d: [e]}]}
    """
    d = {}
    for k, v in items:
        items = d.setdefault(k, [])
        if isinstance(v, list):
            items.append(nestedliststodict(v))
        else:
            items.append(v)
    return d


class PrefixedIO(io.RawIOBase):
    def __init__(self, prefix: bytes, downstream: t.BinaryIO):
        self.prefix = prefix
        self.downstream = downstream
        self.is_at_start = True

    def write(self, bs):
        bytes_written = 0
        if self.is_at_start:
            self.downstream.write(self.prefix)
            bytes_written = len(self.prefix)
            self.is_at_start = False
        if bs.endswith(b"\n"):
            bs = bs[:-1].replace(b"\n", b"\n" + self.prefix) + b"\n"
            self.is_at_start = True
        else:
            bs = bs.replace(b"\n", b"\n" + self.prefix)
        self.downstream.write(bs)
        return bytes_written + len(bs)

    def fileno(self):
        return self.downstream.fileno()
