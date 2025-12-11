#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

BEGIN_MARKER = "<!-- BEGIN DOCKER TAGS -->"
END_MARKER = "<!-- END DOCKER TAGS -->"


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


def render_family(latest: str, exports: list[str], provides_latest: bool) -> list[str]:
    tags = [f"- `{latest}`, `{latest}-all`"]
    if provides_latest:
        tags[0] = tags[0] + ", `latest`"
    for export in exports:
        tags.append(f"  - `{latest}-{export}`")
    return tags


def render_sections(godot4: dict, godot3: dict) -> str:
    modern_latest = str(godot4.get("latest", ""))
    godot4_exports = [str(e) for e in godot4.get("exports", [])]
    godot3_exports = [str(e) for e in godot3.get("exports", [])]

    lines: list[str] = [
        "## Docker Tags",
        "",
        (
            "The tags follow the Godot version and allow for different export template installs "
            f"(for filesize). When in doubt use the base version (ex. {modern_latest}) which includes "
            "all templates provided by Godot."
        ),
        "",
    ]

    lines.extend(render_family(modern_latest, godot4_exports, normalize_bool(godot4.get("provides_latest", False))))
    lines.append("")
    lines.append("Prior versions:")
    lines.append("")
    for version in [str(v) for v in godot4.get("versions", []) if str(v) != modern_latest]:
        lines.append(f"- `{version}`")

    lines.append("")
    lines.append("Legacy versions also supported include:")
    lines.append("")

    legacy_latest = str(godot3.get("latest", ""))
    lines.extend(render_family(legacy_latest, godot3_exports, normalize_bool(godot3.get("provides_latest", False))))
    lines.append("")
    lines.append("Older Godot 3 releases:")
    lines.append("")
    for version in [str(v) for v in godot3.get("versions", []) if str(v) != legacy_latest]:
        lines.append(f"- `{version}`")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render README tag sections from versions files.")
    parser.add_argument("--output", default="README.md", help="README file to update")
    args = parser.parse_args()

    readme_path = Path(args.output)
    text = readme_path.read_text()
    try:
        begin = text.index(BEGIN_MARKER)
        end = text.index(END_MARKER)
    except ValueError as exc:
        raise SystemExit("Could not find README markers for docker tags") from exc

    before = text[: begin + len(BEGIN_MARKER)]
    after = text[end:]

    godot4 = parse_versions_file(Path("godot4/versions.yml"))
    godot3 = parse_versions_file(Path("godot3/versions.yml"))
    rendered = "\n" + render_sections(godot4, godot3) + "\n"

    readme_path.write_text(before + "\n" + rendered + after)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
