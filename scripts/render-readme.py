#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

FOUR_TREE = "<!-- BEGIN DOCKER 4 TREE -->"
FOUR_TREE_END = "<!-- END DOCKER 4 TREE -->"
FOUR_OLDER = "<!-- BEGIN DOCKER 4 OLDER -->"
FOUR_OLDER_END = "<!-- END DOCKER 4 OLDER -->"
THREE_TREE = "<!-- BEGIN DOCKER 3 TREE -->"
THREE_TREE_END = "<!-- END DOCKER 3 TREE -->"
THREE_OLDER = "<!-- BEGIN DOCKER 3 OLDER -->"
THREE_OLDER_END = "<!-- END DOCKER 3 OLDER -->"


def parse_versions_file(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"versions file '{path}' not found")
    data: dict[str, list[str] | str | bool] = {}
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
                    if value.lower() in {"true", "false"}:
                        data[key] = value.lower() == "true"
                    else:
                        data[key] = value.strip("\"'")
                    current_key = None
                else:
                    data[key] = []
                    current_key = key
                continue
            raise ValueError(f"Unsupported line in versions file: {line}")
    return data


def normalize_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def render_godot4_tree(latest: str) -> list[str]:
    return [
        "- `{0}`, `{0}-all`, `latest`".format(latest),
        "  - `{0}-desktop`".format(latest),
        "    - `{0}-linux`".format(latest),
        "    - `{0}-macos`".format(latest),
        "    - `{0}-windows`".format(latest),
        "      - `{0}-win32`".format(latest),
        "      - `{0}-win64`".format(latest),
        "  - `{0}-mobile`".format(latest),
        "    - `{0}-android`".format(latest),
        "    - `{0}-ios`".format(latest),
        "  - `{0}-web`".format(latest),
    ]


def render_godot3_tree(latest: str, provides_latest: bool) -> list[str]:
    latest_line = f"- `{latest}`, `{latest}-all`"
    if provides_latest:
        latest_line += ", `latest`"
    return [
        latest_line,
        "  - `{0}-desktop`".format(latest),
        "    - `{0}-linux`".format(latest),
        "    - `{0}-osx`".format(latest),
        "    - `{0}-windows`".format(latest),
        "      - `{0}-win`".format(latest),
        "        - `{0}-win32`".format(latest),
        "        - `{0}-win64`".format(latest),
        "      - `{0}-uwp`".format(latest),
        "        - `{0}-uwp32`".format(latest),
        "        - `{0}-uwp64`".format(latest),
        "  - `{0}-mobile`".format(latest),
        "    - `{0}-android`".format(latest),
        "    - `{0}-iphone`".format(latest),
        "  - `{0}-html`".format(latest),
    ]


def replace_section(text: str, start_marker: str, end_marker: str, content: str) -> str:
    start_idx = text.index(start_marker) + len(start_marker)
    end_idx = text.index(end_marker)
    return text[:start_idx] + "\n" + content + "\n" + text[end_idx:]


def main() -> int:
    parser = argparse.ArgumentParser(description="Render README tag sections from versions files.")
    parser.add_argument("--output", default="README.md", help="README file to update")
    args = parser.parse_args()

    godot4 = parse_versions_file(Path("godot4/versions.yml"))
    godot3 = parse_versions_file(Path("godot3/versions.yml"))
    modern_latest = str(godot4.get("latest", ""))
    legacy_latest = str(godot3.get("latest", ""))

    modern_versions = [str(v) for v in godot4.get("versions", []) if str(v) != modern_latest]
    legacy_versions = [str(v) for v in godot3.get("versions", []) if str(v) != legacy_latest]

    text = Path(args.output).read_text()
    text = replace_section(text, FOUR_TREE, FOUR_TREE_END, "\n".join(render_godot4_tree(modern_latest)))
    text = replace_section(text, FOUR_OLDER, FOUR_OLDER_END, "\n".join(f"- `{v}`" for v in modern_versions))
    text = replace_section(
        text,
        THREE_TREE,
        THREE_TREE_END,
        "\n".join(render_godot3_tree(legacy_latest, normalize_bool(godot3.get("provides_latest", False)))),
    )
    text = replace_section(text, THREE_OLDER, THREE_OLDER_END, "\n".join(f"- `{v}`" for v in legacy_versions))
    Path(args.output).write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
