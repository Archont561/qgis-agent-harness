# Offline sandbox (orphan branch)

Built 2026-11-12T00:59:12Z from commit `0ed0edd` for platform `linux-64`.
`pixi.lock` sha256 `88647ed0bd019cdd98cf7f4cbd1897c8d268ce32cacd6bb3b0af92e6a4d9454a`.

The verified self-bootstrap binary is stored at `.pixi-sandbox/tools/linux-64/pixi-sandbox`. The branch root intentionally contains documentation only.

| env | platform | packed | unpacked | files |
| --- | --- | ---: | ---: | ---: |
| `js` | linux-64 | 40.3 MiB | 119.8 MiB | 22 |
| `qa` | linux-64 | 93.0 MiB | 331.1 MiB | 45 |


## Restore on the disconnected machine

```bash
./.pixi-sandbox/tools/linux-64/pixi-sandbox doctor --branch-location . --verify
./.pixi-sandbox/tools/linux-64/pixi-sandbox restore --branch-location . --output-path <project> --force
# then, from <project> with no network, use pixi as the sole entrypoint:
pixi install --frozen --offline
pixi run --frozen -- cargo build --offline
```

Every manifest blob is verified before it is written into the working tree.
