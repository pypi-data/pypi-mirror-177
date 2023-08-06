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

import contextlib
import logging
import tempfile
import subprocess

logger = logging.getLogger(__name__)


class ConnectionError(Exception):
    pass


@contextlib.contextmanager
def connect_ssh(
    ssh, hostname, user, default_command="sh -c \"echo ''\" && sleep 99999"
):
    """
    Connect to the given host over ssh.

    Yields (<controlpath>, <Popen>)
    """
    with tempfile.NamedTemporaryFile() as control:
        controlpath = control.name
        with run_ssh(
            ssh,
            controlpath,
            hostname,
            user,
            default_command,
            opts=[
                "-oControlMaster=yes",
                "-oControlPersist=yes",
            ],
        ) as proc:
            yield controlpath, proc
            logger.debug("Terminating connection")
            proc.terminate()


def run_ssh(ssh, controlpath, hostname, user, command, opts=[], stdin=subprocess.PIPE):
    if user:
        connstr = f"{user}@{hostname}"
    else:
        connstr = hostname
    args = (
        [
            ssh,
            f'-oControlPath="{controlpath}"',
            "-q",
        ]
        + opts
        + [connstr, command]
    )
    logger.info(f"Running: {args}")
    return subprocess.Popen(
        args,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def run_local(command, stdin=subprocess.PIPE):
    logger.info(f"Running local: {command}")
    return subprocess.Popen(
        [command],
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
