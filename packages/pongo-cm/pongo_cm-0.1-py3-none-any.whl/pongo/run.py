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

import io
import os
import select
import sys


def select_communicate(proc, input) -> tuple[io.IOBase, io.IOBase]:
    """
    Analogue of subprocess.Popen.communicate, but using select to handle larger
    data sizes
    """

    stdout = io.BytesIO()
    stderr = io.BytesIO()
    size = select.PIPE_BUF
    rlist = [proc.stdout, proc.stderr]
    rlist_to = [stdout, stderr]
    wlist = [proc.stdin]
    wlist_from = [input]

    while proc.poll() is None:
        rs, ws, es = select.select(rlist, wlist, [], 0)
        for w, r in zip(wlist, wlist_from):
            if w in ws:
                buf = r.read(size)
                if buf:
                    w.write(buf)
                else:
                    wlist.remove(w)
                    w.close()
        for r, w in zip(rlist, rlist_to):
            if r in rs:
                w.write(r.read(size))

    return stdout, stderr


def pipe(procs, in_=None, out=sys.stdout.buffer, err=sys.stderr.buffer):
    """
    Pipe the output of each process into the input of the next.
    The final process' output will be piped into ``out``.
    All errors will be piped into the single ``err`` stream.
    """
    alive = set(procs)

    pairs = {p.stdout.raw: q.stdin.raw for p, q in zip(procs, procs[1:])}
    if in_ and procs[0].stdin:
        pairs = pairs | {in_: procs[0].stdin}
    if out:
        pairs = pairs | {procs[-1].stdout.raw: out}
    if err:
        pairs = pairs | {p.stderr.raw: err for p in procs if p.stderr}
    while alive:
        read_ready, _, _ = select.select(set(pairs.keys()), [], [])
        _, write_ready, _ = select.select([], set(pairs.values()), [])
        for sock in read_ready:
            if pairs[sock] in write_ready:
                buf = sock.read(select.PIPE_BUF)
                pairs[sock].write(buf)
                pairs[sock].flush()
            else:
                pass

        for p in list(alive):
            if p.poll() is not None:
                alive.remove(p)
                dest = pairs.pop(p.stdout.raw)
                if dest is not out:
                    dest.close()
                if p.stderr:
                    dest = pairs.pop(p.stderr.raw)
                    if dest is not err:
                        dest.close()
