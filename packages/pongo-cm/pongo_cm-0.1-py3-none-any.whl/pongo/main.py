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

import argparse
import dirconf
import logging
import pathlib
import tempfile
from datetime import datetime


import pongo
import pongo.config
import pongo.connect
import pongo.indentedtext
import pongo.run
import pongo.targets


logger = logging.getLogger(__name__)


def main():
    argparser = get_argparser()
    args = argparser.parse_args()
    if args.verbose > 1:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose > 0:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)
    confdir = (
        args.config if args.config else dirconf.get_config_dir("pongo.conf.d", paths=[])
    )
    config = dirconf.load(confdir)

    pongo.config.init_config(config)
    pongo.config.save_config(config)
    scriptbase = pathlib.Path(config["scriptbase"]).resolve()

    if args.scriptdir:
        path = pathlib.Path(args.scriptdir)
        targets = []
        for base in [pathlib.Path("."), scriptbase]:
            if (base / path / "Pongofile").is_file():
                scriptdir = (base / path).resolve()
                scriptdirtargets = {scriptdir: pongo.targets.load_targets(scriptdir)}
                targets = pongo.targets.gather_target_scripts(
                    scriptbase, scriptdirtargets, scriptdir, args.script
                )
                break
    elif args.command:
        command = args.command
        targets = [
            pongo.targets.PipeGroup(
                [
                    pongo.targets.Target(
                        name="default",
                        script=command,
                        scriptdir=pongo.targets.Scriptdir("command"),
                    )
                ]
            )
        ]
    else:
        argparser.error("One of --command or scriptdir must be specified")

    if not targets:
        argparser.error("No matching targets found")
    hosts_conf = config["hosts"]
    hosts = pongo.get_hosts(args.host, hosts_conf)
    logdir = tempfile.mkdtemp(
        prefix=f"pongo-{args.script}.{datetime.now().strftime('%Y%m%d-%H%M%S')}."
    )
    for term_color, host in zip(pongo.term_colors, hosts):
        context = pongo.get_template_context_for_host(config, host)
        try:
            pongo.targets.run_targets(
                targets,
                context=context,
                host=host,
                term_color=term_color,
                logdir=logdir,
            )
        except pongo.connect.ConnectionError:
            logger.exception(
                f"Got ConnectionError while running targets on host {host}"
            )


def get_argparser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--command", "-c", help="Run a single command remotely")
    argparser.add_argument("--config", help="Path to configuration directory")
    argparser.add_argument("--verbose", "-v", action="count", default=0)
    argparser.add_argument(
        "--host",
        action="append",
        default=[],
        help="Specify a host ('hostname'), "
        "a tag ('@tag'), or an intersection of tags ('@tag1+@tag2')",
    )
    argparser.add_argument("scriptdir", nargs="?", default=None)
    argparser.add_argument("script", nargs="?", default="default")
    return argparser


if __name__ == "__main__":
    main()
