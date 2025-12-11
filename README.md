# docker-godot-headless

Docker builds for [Godot Engine](https://godotengine.org/) (headless) with export templates

The entrypoint calls the Godot Engine (`/usr/local/bin/godot`) so override the `command` with any arguments (default is `--help`).

### Usage Example (docker-compose)

```yaml
version: '2'
services:
  godot:
    image: godot-headless:4.3-desktop
    volumes:
      - ./:/project
    command: --path /project --export win64 bin/win64/maze-test.exe
```

## Updating the Godot version

- Each major version has its Dockerfile and `versions.yml` under `godot4/` and `godot3/`. Update the relevant `versions.yml` (and set `provides_latest: true` only for the major that should publish the `latest` tag).
- Run `bash scripts/update-godot.sh <version> <previous>` locally to update `godot4/Dockerfile`, `godot4/versions.yml`, and the README placeholders. (A similar helper can be added for the legacy `godot3` directory if needed.)
- Or trigger the `Update Godot Version` workflow under *Actions* → *Update Godot Version* and provide the version/previous tags; it will run the script above and open a pull request with the changes.
- The DockerHub workflow syncs the repo's DockerHub description from this README automatically, so keep the summary section focused on what you want to display there.
- The DockerHub publishing workflows auto-run when files in their respective directories change: `Dockerhub` builds the 4.x images, while `Dockerhub Legacy` builds 3.x. You can also trigger them (or the manual `Sync README tags` workflow) from the *Actions* tab to rebuild or refresh documentation on demand.

<!-- BEGIN DOCKER TAGS -->

## Docker Tags

The tags follow the Godot version and allow for different export template installs (for filesize). When in doubt use the base version which includes all templates provided by Godot.

<!-- BEGIN DOCKER 4 TREE -->
- `4.3`, `4.3-all`, `latest`
  - `4.3-desktop`
    - `4.3-linux`
    - `4.3-macos`
    - `4.3-windows`
      - `4.3-win32`
      - `4.3-win64`
  - `4.3-mobile`
    - `4.3-android`
    - `4.3-ios`
  - `4.3-web`
<!-- END DOCKER 4 TREE -->

Prior versions:

<!-- BEGIN DOCKER 4 OLDER -->
- `4.2.2`
- `4.2.1`
- `4.2`
- `4.1.3`
- `4.1.2`
- `4.1.1`
- `4.1`
- `4.0.3`
- `4.0.2`
- `4.0.1`
- `4.0`
<!-- END DOCKER 4 OLDER -->

Legacy versions also supported include:

<!-- BEGIN DOCKER 3 TREE -->
- `3.5.3`, `3.5.3-all`
  - `3.5.3-desktop`
    - `3.5.3-linux`
    - `3.5.3-osx`
    - `3.5.3-windows`
      - `3.5.3-win`
        - `3.5.3-win32`
        - `3.5.3-win64`
      - `3.5.3-uwp`
        - `3.5.3-uwp32`
        - `3.5.3-uwp64`
  - `3.5.3-mobile`
    - `3.5.3-android`
    - `3.5.3-iphone`
  - `3.5.3-html`
<!-- END DOCKER 3 TREE -->

Older Godot 3 releases:

<!-- BEGIN DOCKER 3 OLDER -->
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
- `3.3.2`
- `3.3.1`
- `3.3`
- `3.2.3`
<!-- END DOCKER 3 OLDER -->

<!-- END DOCKER TAGS -->
