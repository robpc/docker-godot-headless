# docker-godot-headless

Docker builds for [Godot Engine](https://godotengine.org/) (headless) with export templates

The entrypoint calls the Godot Engine (`/usr/local/bin/godot`) so override the `command` with any arguments (default is `--help`).

### Usage Example (docker-compose)

```yaml
version: '2'
services:
  godot:
    image: godot-headless:3.4.5-desktop
    volumes:
      - ./:/project
    command: --path /project --export win64 bin/win64/maze-test.exe
```

## Docker Tags

The tags follow the Godot version and allow for different export template installs (for filesize). When in doubt use the base version (ex. 3.4.5) which includes all templates provided by Godot.

- `3.4.5`, `3.4.5-all`, `latest`
  - `3.4.5-desktop`
    - `3.4.5-linux`
    - `3.4.5-osx`
    - `3.4.5-windows`
      - `3.4.5-win`
        - `3.4.5-win32`
        - `3.4.5-win64`
      - `3.4.5-uwp`
        - `3.4.5-uwp32`
        - `3.4.5-uwp64`
  - `3.4.5-mobile`
    - `3.4.5-android`
    - `3.4.5-iphone`
  - `3.4.5-html`

Legacy versions also supported include:

- `3.4.4`
- `3.4.3`
- `3.4.2`
- `3.4.1`
- `3.4`
- `3.3.4`
- `3.3.3`
- `3.2.3`
- `3.3`
- `3.3.1`
- `3.3.2`