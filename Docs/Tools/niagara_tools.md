# Niagara VFX MCP tools

Registered from `Python/tools/niagara_tools.py` when the main `unrealMCP` server runs.

## Asset & system

- `create_niagara_system` — new `UNiagaraSystem` asset
- `create_niagara_emitter` — standalone emitter asset
- `add_emitter_to_system` — attach emitter to a system
- `compile_niagara_asset` — compile system or emitter
- `get_niagara_metadata` — emitters, modules, parameters, renderers, status

## Modules & inputs

- `search_niagara_modules` — asset registry search with optional stage filter
- `add_module_to_emitter` — stack module on an emitter
- `set_module_input` — set module input values
- `move_module` — reorder modules in the stack

## Parameters, data interfaces, renderers

- `add_niagara_parameter` / `set_niagara_parameter`
- `add_data_interface` / `set_data_interface_property`
- `add_renderer` / `set_renderer_property`

## Level

- `spawn_niagara_actor` — place a Niagara system in the current level

Additional registry commands (curve inputs, static switches, diagnostics, duplicate system, etc.) are implemented in the C++ plugin and can be called with the same TCP JSON protocol if you extend the Python tool module.
