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

import os
from datetime import datetime

import itertools
import socket
import typing as t
from collections import defaultdict

from jinja2 import Environment

__version__ = "0.1"
term_colors = itertools.cycle([2, 6, 3, 4])


def parse_host_spec(s, hostconf):
    host_tags = {}
    tag_hosts = defaultdict(set)
    for host, cfg in hostconf.items():
        host_tags[host] = cfg.get("tags", "").split()
        for tag in host_tags[host]:
            tag_hosts[tag].add(host)

    parts = (item.strip() for item in s.split("+"))
    candidates = set(host_tags)
    for p in parts:
        if p.upper() == "@ALL":
            return set(host_tags)
        elif p.startswith("@"):
            tag = p[1:]
            candidates = candidates.intersection(
                {h for h in host_tags if tag in host_tags[h]}
            )
        else:
            return [p]
    return candidates


def get_hosts(hostspecs, configured_hosts):
    all_hosts = [
        h for hostspec in hostspecs for h in parse_host_spec(hostspec, configured_hosts)
    ]
    all_hosts = [h for h in all_hosts if "DISABLED" not in configured_hosts.get(h, {})]
    return all_hosts


def get_tags_for_host(tag_conf, host_conf):
    tags = [tag for tag in host_conf.get("tags", "").split()]
    while True:
        tagc = len(tags)
        tags.extend(
            new_tag
            for tag in tags
            for new_tag in tag_conf.get(tag, {}).get("tags", "").split()
            if new_tag not in tags
        )
        if len(tags) == tagc:
            break
    return tags


def get_template_context_for_host(config, host):
    """
    Return a dict containing OS environment variables
    any configured environ read from the configured host + tags.
    """

    def render_values(d: dict[str, t.Any]):
        return {
            k: render_jinja(v, env) if isinstance(v, str) else v for k, v in d.items()
        }

    tag_conf = config["tags"]
    hosts_conf = config["hosts"]
    host_conf = hosts_conf.get(host, {})
    env = config.get("environ", {})
    env |= {
        "PONGO_HOST": host,
        "PONGO_HOSTNAME": host_conf.get("hostname", host),
        "PONGO_SUDO": host_conf.get("sudo", "sudo"),
        "PONGO_CONNECT_USER": host_conf.get("user", os.getlogin()),
        "PONGO_SHELL": host_conf.get("shell", "/bin/sh"),
        "PONGO_SSH": host_conf.get("ssh", "ssh"),
    }
    try:
        env["PONGO_HOST_IP"] = socket.gethostbyname(env["PONGO_HOSTNAME"])
    except OSError:
        env["PONGO_HOST_IP"] = ""

    tags = get_tags_for_host(tag_conf, host_conf)
    for tag in reversed(tags):
        env = env | render_values(tag_conf.get(tag, {}).get("environ", {}))
    env = env | render_values(host_conf.get("environ", {}))
    return env


def render_jinja(s, environ, j2env=Environment(autoescape=False)):
    template = j2env.from_string(s)
    now = datetime.now().astimezone()
    environ.setdefault(
        "pongo_managed",
        (
            f"--- Pongo managed. "
            f"File generated "
            f"{now:%Y-%m-%d %H:%M:%S %Z} "
            f"by {os.environ.get('user', 'unknown')}"
        ),
    )

    return template.render(**environ)
