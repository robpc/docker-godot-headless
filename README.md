# docker-godot-headless

Docker builds for [Godot Engine](https://godotengine.org/) (headless) with export templates

The entrypoint calls the Godot Engine (`/usr/local/bin/godot`) so override the `command` with any arguments (default is `--help`).

### Usage Example (docker-compose)

```yaml
version: '2'
services:
  godot:
    image: godot-headless:3.3.4-desktop
    volumes:
      - ./:/project
    command: --path /project --export win64 bin/win64/maze-test.exe
```

## Docker Tags

The tags follow the Godot version and allow for different export template installs (for filesize). When in doubt use the base version (ex. 3.3.4) which includes all templates provided by Godot.

- `3.3.4`, `3.3.4-all`, `latest`
  - `3.3.4-desktop`
    - `3.3.4-linux`
    - `3.3.4-osx`
    - `3.3.4-windows`
      - `3.3.4-win`
        - `3.3.4-win32`
        - `3.3.4-win64`
      - `3.3.4-uwp`
        - `3.3.4-uwp32`
        - `3.3.4-uwp64`
  - `3.3.4-mobile`
    - `3.3.4-android`
    - `3.3.4-iphone`
  - `3.3.4-html`

Legacy versions also supported include:

- `3.3.3`
- `3.2.3`
- `3.3`
- `3.3.1`
- `3.3.2`