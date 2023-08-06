from collections import namedtuple
from collections.abc import MutableMapping
from datetime import datetime
from itertools import count
from pathlib import Path
from typing import Optional
import enum
import json
import os
import pickle

try:
    import toml
except ImportError:
    toml = None


FileType = namedtuple("FileType", "suffix raw encoding loader dumper")
Datum = namedtuple("Datum", "value filetype modified_since_load")
backup_suffix = ".orig-"


def get_config_dir(name: str, paths=[], create=False) -> Optional[Path]:
    parents = []
    if paths == ["CLOSEST"]:
        cwd = Path.cwd()
        parents.append(cwd)
        parents.extend(cwd.parents)
    standard_locations = [
        os.environ.get("APPDATA"),
        os.environ.get("XDG_CONFIG_HOME"),
        str(Path(os.environ["HOME"]) / ".config"),
    ]
    parents.extend(Path(p) for p in standard_locations if p is not None)

    all_paths = [parent / name for parent in parents if parent.exists()]
    for path in all_paths:
        if path.exists():
            return path

    if create:
        os.makedirs(str(all_paths[0]), exist_ok=True)
        return all_paths[0]

    raise Exception(
        f"Could not find configuration directory in {':'.join(map(str, all_paths))}"
    )


class FileTypes(enum.Enum):
    STR = FileType("", False, "utf-8", lambda n: n.strip(), str)
    JSON = FileType(".json", True, "utf-8", json.load, json.dump)
    PICKLE = FileType(".pickle", True, None, pickle.load, pickle.dump)
    TEXT = FileType(".txt", False, "utf-8", lambda n: n, str)
    if toml:
        TOML = FileType(".toml", True, "utf-8", toml.load, toml.dump)


class ConfigDict(MutableMapping):
    def __init__(self, path=None):
        self.d = {}
        self.path = path

    def __getitem__(self, key):
        return self.d[key].value

    def __setitem__(self, key, value):
        self.d[key] = Datum(value, self.guess_filetype(value), True)

    def __delitem__(self, key, value):
        del self.d[key]

    def __iter__(self):
        return (item for item in self.d)

    def __len__(self):
        return len(self.d)

    def load(self, key, value, filetype=None):
        """
        Same as `set`, but creates the entry with modified_since_load=False
        """
        self.d[key] = Datum(
            value, filetype or self.guess_filetype(value), False
        )

    def set(self, key, value, filetype=None):
        self.d[key] = Datum(value, filetype or self.guess_filetype(value), True)

    def setdefault(self, key, value, filetype=None):
        try:
            return self[key]
        except KeyError:
            self.set(key, value, filetype)
            return value

    def get_filetype(self, key):
        return self.d[key].filetype

    def get_filetype_by_suffix(self, suffix):
        for filetype in FileTypes:
            if filetype.value.suffix == suffix:
                return filetype.value
        raise ValueError(f"Unknown file suffix: {suffix!r}")

    def guess_filetype(self, value):
        if isinstance(value, int):
            return FileTypes.INT.value
        if isinstance(value, str):
            return FileTypes.STR.value
        if isinstance(value, (list, dict, tuple)):
            return FileTypes.JSON.value
        return FileTypes.PICKLE.value

    def get_suffix(self, key):
        return self.get_filetype(key).suffix

    def get_dumped(self, key):
        return self.get_filetype(key).dumper(self[key])

    def get_modified(self, key):
        return self.d[key].modified_since_load


def load(configdir: Path) -> ConfigDict:
    conf = ConfigDict(configdir)
    for entry in configdir.iterdir():
        key = entry.stem
        suffix = entry.suffix
        if suffix.startswith(backup_suffix):
            continue

        if entry.is_dir():
            conf.load(key, load(entry), None)

        else:
            filetype = conf.get_filetype_by_suffix(suffix)
            if filetype.encoding:
                mode = "r"
            else:
                mode = "rb"
            with entry.open(mode, encoding=filetype.encoding) as f:
                if filetype.raw:
                    value = f
                else:
                    value = f.read()
                conf.load(key, filetype.loader(value), filetype)
    return conf


def dump(configdir: Path, conf: ConfigDict):
    saved = set()
    for key, value in conf.items():
        if isinstance(value, ConfigDict):
            filename = configdir / key
            os.makedirs(filename, exist_ok=True)
            dump(filename, value)
            saved.add(filename)
        else:
            filename = configdir / f"{key}{conf.get_suffix(key)}"
            if conf.get_modified(key):
                filetype = conf.get_filetype(key)
                if filetype.encoding:
                    mode = "w"
                else:
                    mode = "wb"
                with filename.open(mode, encoding=filetype.encoding) as f:
                    if filetype.raw:
                        conf.get_dumped(f, key)
                    else:
                        f.write(conf.get_dumped(key))
            saved.add(filename)

    def make_archive_path(path: Path) -> Path:
        ts = datetime.fromtimestamp(path.stat().st_mtime).strftime(
            "%Y%m%d%H%M%S"
        )
        p = path
        p = p.parent / f"{p.name}{backup_suffix}{ts}"
        if p.exists():
            i = count()
            p = p.parent / f"{p.name}.{next(i)}"
            while p.exists():
                p = p.parent / f"{p.stem}.{next(i)}"
        return p

    for item in configdir.iterdir():
        if item.suffix.startswith(backup_suffix):
            continue
        if item not in saved:
            item.rename(make_archive_path(item))
