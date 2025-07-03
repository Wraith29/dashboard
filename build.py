#!/home/iacna/.local/bin/uv run

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from subprocess import run


def hash_dir(dirpath: Path) -> str:
    print(f"Hashing {dirpath}")
    hash = sha256()

    for subpath in dirpath.iterdir():
        if subpath.is_dir():
            hash.update(hash_dir(subpath))
        else:
            hash.update(subpath.read_bytes())

    return hash.hexdigest()


@dataclass
class Module:
    name: str
    path: Path

    def calculate_hash(self) -> str:
        return hash_dir(self.path)

    def get_existing_hash(self, cache_dir: Path) -> str:
        child = Path(cache_dir.absolute(), self.name + ".sum")

        if not child.exists():
            return ""

        return child.read_text()

    def save_hash(self, cache_dir: Path, hash: str) -> None:
        child = Path(cache_dir.absolute(), self.name + ".sum")
        child.write_text(hash)

    def build(self, lib_dir: Path) -> None:
        outpath = Path(lib_dir.absolute(), self.name+".so")

        result = run(
            args=[
                "go", "build",
                "-o", str(outpath.absolute()),
                "-buildmode=plugin", str(self.path.absolute()),
            ],
            cwd=str(self.path.absolute()),
            capture_output=True,
        )

        result.check_returncode()


def get_modules() -> list[Module]:
    modpath = Path("./modules")

    return [
        Module(path.stem, path)
        for path in modpath.iterdir()
    ]


def main() -> int:
    lib_dir = Path("/home/iacna/.config/dashboard/libs")
    if not lib_dir.exists():
        lib_dir.mkdir()

    cache_dir = Path(".build-cache")
    if not cache_dir.exists():
        cache_dir.mkdir()

    modules = get_modules()

    for module in modules:
        print(f"Checking {module.name}")
        existing = module.get_existing_hash(cache_dir)
        print(f"Existing Hash: {existing}")
        new = module.calculate_hash()
        print(f"New: {new}")

        if existing != new:
            print(f"Building {module.name}")
            module.build(lib_dir)
            module.save_hash(cache_dir, new)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
