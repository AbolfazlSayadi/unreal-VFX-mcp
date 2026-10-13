# VFX workflow (UE 5.6+)

This repo ports Niagara VFX support from [TrishynVolodymyr/unreal-mcp](https://github.com/TrishynVolodymyr/unreal-mcp) (UE 5.8) and targets **Unreal Engine 5.6**.

## Layers

| Layer | Location |
|-------|----------|
| **Cursor skills** | `.cursor/skills/vfx-technical-director`, `vfx-reference-transcriber`, `vfx-texture-generator`, `niagara-vfx-architect` |
| **MCP tools (Python)** | `Python/tools/niagara_tools.py` (registered in `unreal_mcp_server.py`) |
| **Editor plugin (C++)** | `MCPGameProject/Plugins/UnrealMCP` — Niagara command registry + `FNiagaraService` |

## Typical pipeline

1. **vfx-reference-transcriber** — extract frames from reference video/GIF, output a structured VFX spec.
2. **vfx-technical-director** — choose techniques, constraints, and performance budget.
3. **vfx-texture-generator** — procedural PNG sprites/noise/flipbooks for import into UE.
4. **niagara-vfx-architect** — build Niagara systems via MCP tools (`create_niagara_system`, modules, renderers, spawn in level).

## Build notes

- Enable the **Niagara** plugin (already listed in `UnrealMCP.uplugin`).
- Rebuild `MCPGameProject` in **Development Editor** after pulling VFX changes.
- Factory creation uses `UFactory::FactoryCreateNew` so the same code path works on **5.6 and 5.8** (5.8 made Niagara factory subclasses private).

## Texture scripts

Dependencies: `numpy`, `pillow` (see `Python/pyproject.toml`). Reference frame extraction uses `ffmpeg` / `ffprobe` on the PATH.
