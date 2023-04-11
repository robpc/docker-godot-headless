# docker-godot-headless

Docker builds for [Godot Engine](https://godotengine.org/) (headless) with export templates

The entrypoint calls the Godot Engine (`/usr/local/bin/godot`) so override the `command` with any arguments (default is `--help`).

### Usage Example (docker-compose)

```yaml
version: '2'
services:
  godot:
    image: godot-headless:4.0-desktop
    volumes:
      - ./:/project
    command: --path /project --export win64 bin/win64/maze-test.exe
```

## Docker Tags

The tags follow the Godot version and allow for different export template installs (for filesize). When in doubt use the base version (ex. 4.0) which includes all templates provided by Godot.

- `4.0`, `4.0-all`, `latest`
  - `4.0-desktop`
    - `4.0-linux`
    - `4.0-macos`
    - `4.0-windows`
      - `4.0-win32`
      - `4.0-win64`
  - `4.0-mobile`
    - `4.0-android`
    - `4.0-ios`
  - `4.0-web`

Prior versions:

- None

Legacy versions also supported include:

- `3.5.2`, `3.5.2-all`, `latest`
  - `3.5.2-desktop`
    - `3.5.2-linux`
    - `3.5.2-osx`
    - `3.5.2-windows`
      - `3.5.2-win`
        - `3.5.2-win32`
        - `3.5.2-win64`
      - `3.5.2-uwp`
        - `3.5.2-uwp32`
        - `3.5.2-uwp64`
  - `3.5.2-mobile`
    - `3.5.2-android`
    - `3.5.2-iphone`
  - `3.5.2-html`

- `3.5.2`
- `3.5.1`
- `3.5`
- `3.4.5`
- `3.4.4`
- `3.4.3`
- `3.4.2`
- `3.5.2`
- `3.5.1`
- `3.5`
- `3.4.5`
- `3.4.4`
- `3.4.3`
- `3.4.2`
- `3.5.2`
- `3.5.1`
- `3.5`
- `3.4.5`
- `3.4.4`
- `3.4.3`
- `3.4.2`
- `3.5.2`
- `3.5.1`
- `3.5`
- `3.4.5`
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