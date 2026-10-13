# Install UnrealMCP into `JAssets2UEFN` (Windows)

This environment (Cursor Cloud Agent) **cannot** access your PC or run Unreal on `D:\`. Use the steps below on your machine.

## Prerequisites

- **Unreal Engine 5.6** (matches this repo’s Niagara VFX port)
- **Visual Studio 2022** with “Game development with C++”
- This repo cloned locally (or use the branch with PR #1 merged)

## One-command install (copy + optional build)

In **PowerShell** (from the repo root):

```powershell
cd path\to\unreal-VFX-mcp
.\Scripts\Install-UnrealMCP-Plugin.ps1 -ProjectRoot "D:\Projects\JAssets2UEFN" -Build -EngineRoot "C:\Program Files\Epic Games\UE_5.6"
```

Without `-Build`, the script only copies the plugin and enables it in your `.uproject`; you then generate VS files and build in Visual Studio.

## Manual steps

1. Copy folder:
   - **From:** `MCPGameProject\Plugins\UnrealMCP`
   - **To:** `D:\Projects\JAssets2UEFN\Plugins\UnrealMCP`

2. Open `D:\Projects\JAssets2UEFN\*.uproject` in UE 5.6 (or edit JSON):
   - **Edit → Plugins → UnrealMCP → Enable** (restart editor if asked)

3. Right-click the `.uproject` → **Generate Visual Studio project files**

4. Open the `.sln` → configuration **Development Editor** → **Build**

5. **Python MCP** (on your PC): point Cursor’s MCP config at `Python\unreal_mcp_server.py` (see root `mcp.json`). Start the editor before using tools.

## UEFN note

If **JAssets2UEFN** is a UEFN / Verse / restricted template project, Epic may block third-party editor plugins or C++ modules. UnrealMCP is an **Editor** C++ plugin (TCP server in the editor). If your project has no `Source/` folder and no C++ target, you may need a standard UE 5.6 game project for MCP-driven Niagara work, then migrate assets into UEFN.

## Verify

- Editor log: `UnrealMCPBridge: Initializing` and `Niagara VFX commands registered`
- With MCP server running: tool `create_niagara_system` (editor open)
