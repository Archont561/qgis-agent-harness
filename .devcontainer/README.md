# Dev container

One container, one toolchain. The repository has exactly one way to run anything — `pixi run <task>` —
and the container adds nothing beside it: no `apt install`, no `pip install`, no Node image. A second
toolchain path is how a container and CI drift apart, and drift is what the harness exists to catch.

```sh
devcontainer up --workspace-folder .
pixi run qa          # alint, ruff, vale — the same gate CI runs
pixi run test        # the checker tests, then the harness suite
```

## What is in the box

| Piece | Why this and not something else |
|---|---|
| `ghcr.io/prefix-dev/pixi:0.84.1@sha256:2d8821a1…` | pixi installs the interpreter, QGIS and the linters from one lockfile; the image is pinned by digest, so a container that ran green in March still does |
| a non-root `dev` user | the container runs the harness, so it should not also be able to rewrite the toolchain that scores it |
| the `/pixi-cache` volume | environments survive a rebuild; pulling QGIS again is three gigabytes per container |
| `QT_QPA_PLATFORM=offscreen` | QGIS is used headless, and a PyQGIS import must not block on a display that is not there |
| `postCreateCommand` → `.devcontainer/post-create.sh` | installs `qa` and `test` only — the `experiment` environment is fetched by the first task that needs QGIS |

## The one thing that is deliberately absent

There is no `experiment` environment at container start. It carries QGIS, GDAL, geopandas and the rest at
about 3.5 GB, and most sessions — a documentation fix, a linter rule, a card's YAML — never touch it. The
first `pixi run harness …` installs it, once, into the cache volume.

## Bumping the pin

```sh
docker buildx imagetools inspect ghcr.io/prefix-dev/pixi:0.84.1 | head -3   # the digest to quote
```

Change the tag **and** the digest in `.devcontainer/Dockerfile` in one commit. A tag without its digest
is a pin that moves; a digest without its tag is unreadable six months later.

## If the manifest is missing

`.devcontainer/post-create.sh` exits cleanly when `pixi.toml` is not there yet, because a repository
skeleton is a legitimate state and a failed post-create is a confusing one. The container still builds;
`pixi run qa` starts working the moment the manifest lands.
