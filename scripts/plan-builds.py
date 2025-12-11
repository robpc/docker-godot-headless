#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def parse_versions_file(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"versions file '{path}' not found")
    data: dict[str, object] = {}
    current_key: str | None = None
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("- "):
                if current_key is None:
                    raise ValueError(f"List item found without key in line: {line}")
                data.setdefault(current_key, [])
                value = stripped[2:].strip().strip("\"'")
                (data[current_key]).append(value)  # type: ignore[index]
                continue
            if ":" in stripped:
                key, value = stripped.split(":", 1)
                key = key.strip()
                value = value.strip()
                if value:
                    data[key] = value.strip("\"'")
                    current_key = None
                else:
                    data[key] = []
                    current_key = key
                continue
            raise ValueError(f"Unsupported line in versions file: {line}")
    return data


def missing_tags(namespace: str, repo: str, desired: set[str]) -> set[str]:
    remaining = set(desired)
    next_url: str | None = (
        f"https://hub.docker.com/v2/repositories/"
        f"{urllib.parse.quote(namespace)}/{urllib.parse.quote(repo)}/tags?page_size=100"
    )
    while next_url and remaining:
        request = urllib.request.Request(next_url)
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        for result in data.get("results", []):
            name = result.get("name")
            if isinstance(name, str) and name in remaining:
                remaining.remove(name)
        next_url = data.get("next")
    return remaining


def normalize_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Target:
    name: str
    versions: list[str]
    exports: list[str]
    dockerfile: Path
    provides_latest: bool
    latest: str


def discover_targets(version_files: Iterable[Path]) -> list[Target]:
    targets: list[Target] = []
    for file_path in version_files:
        data = parse_versions_file(file_path)
        versions = [str(v) for v in data.get("versions", [])]
        exports = [str(v) for v in data.get("exports", [])]
        if not versions:
            raise SystemExit(f"No versions defined in {file_path}")
        if not exports:
            raise SystemExit(f"No exports defined in {file_path}")
        provides_latest = normalize_bool(data.get("provides_latest", False))
        latest = str(data.get("latest", versions[0]))
        dockerfile = file_path.with_name("Dockerfile")
        if not dockerfile.is_file():
            raise SystemExit(f"Dockerfile not found for {file_path}")
        targets.append(
            Target(
                name=file_path.parent.name or file_path.stem,
                versions=versions,
                exports=exports,
                dockerfile=dockerfile,
                provides_latest=provides_latest,
                latest=latest,
            )
        )
    return targets

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Docker build matrix from versions files.")
    parser.add_argument(
        "--versions-file",
        dest="versions_files",
        action="append",
        help="Path to a versions.yml file (repeat for multiple files). Defaults to godot*/versions.yml.",
    )
    parser.add_argument("--repository", required=True, help="DockerHub repository (namespace/name)")
    parser.add_argument("--only-version", help="Build only this version regardless of the versions file")
    parser.add_argument("--force", action="store_true", help="Force builds even if the tag exists on DockerHub")
    parser.add_argument("--output", required=True, help="Where to write the resulting JSON plan")
    args = parser.parse_args()

    versions_files = (
        [Path(p) for p in args.versions_files]
        if args.versions_files
        else sorted(Path(".").glob("godot*/versions.yml"))
    )
    if not versions_files:
        raise SystemExit("No versions.yml files found.")

    targets = discover_targets(versions_files)
    namespace, repo = args.repository.split("/", 1)

    desired_tags: set[str] = set()
    for target in targets:
        for version in target.versions:
            if args.only_version and version != args.only_version:
                continue
            for export in target.exports:
                desired_tags.add(f"{version}-{export}")

    missing: set[str] = set()
    if not args.force:
        missing = missing_tags(namespace, repo, desired_tags)
    else:
        missing = desired_tags

    include: list[dict[str, str]] = []
    for target in targets:
        for version in target.versions:
            if args.only_version and version != args.only_version:
                continue
            for export in target.exports:
                tag = f"{version}-{export}"
                if tag in missing:
                    include.append(
                        {
                            "family": target.name,
                            "version": version,
                            "exports": export,
                            "dockerfile": str(target.dockerfile),
                            "latest": target.latest if target.provides_latest else "",
                        }
                    )

    output_path = Path(args.output)
    output = {"include": include}
    output_path.write_text(json.dumps(output), encoding="utf-8")
    print(f"Discovered {len(include)} build(s) to run", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
