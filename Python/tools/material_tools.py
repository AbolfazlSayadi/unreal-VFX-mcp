"""Material Tools for Unreal MCP."""

import logging
from typing import Dict, List
from mcp.server.fastmcp import FastMCP, Context

logger = logging.getLogger("UnrealMCP")


def __send_unreal_command(command: str, params: Dict) -> Dict:
    """Send a TCP command to the Unreal Editor plugin."""
    from unreal_mcp_server import get_unreal_connection

    unreal = get_unreal_connection()
    if not unreal:
        return {"status": "error", "error": "Failed to connect to Unreal Engine"}

    response = unreal.send_command(command, params)
    if not response:
        return {"status": "error", "error": "No response from Unreal Engine"}
    return response


def register_material_tools(mcp: FastMCP):
    """Register material tools with the MCP server."""

    @mcp.tool()
    def create_material(
        ctx: Context,
        name: str,
        path: str = "/Game/Materials",
        blend_mode: str = "Opaque",
        shading_model: str = "DefaultLit",
    ) -> Dict:
        """
        Create a new Material asset.

        Args:
            name: Material name (e.g. "M_Fire")
            path: Content path for the material
            blend_mode: "Opaque"|"Masked"|"Translucent"|"Additive"|"Modulate"
            shading_model: "DefaultLit"|"Unlit"|"Subsurface"|"ClearCoat"|"TwoSidedFoliage"

        Example:
            create_material(name="M_Wood", path="/Game/Materials", blend_mode="Opaque")
        """
        return __send_unreal_command("create_material", {
            "name": name,
            "path": path,
            "blend_mode": blend_mode,
            "shading_model": shading_model,
        })

    @mcp.tool()
    def set_material_properties(
        ctx: Context,
        material_path: str,
        blend_mode: str = "",
        shading_model: str = "",
        material_domain: str = "",
        two_sided: bool = False,
    ) -> Dict:
        """
        Set material domain, blend mode, and related properties.

        Args:
            material_path: Full path to the material
            blend_mode: "Opaque"|"Masked"|"Translucent"|"Additive"|"Modulate" (empty = unchanged)
            shading_model: "DefaultLit"|"Unlit"|... (empty = unchanged)
            material_domain: "Surface"|"DeferredDecal"|"LightFunction"|"Volume"|"PostProcess"|"UserInterface"
            two_sided: Enable two-sided rendering

        Example:
            set_material_properties(material_path="/Game/Materials/M_Fire", material_domain="Surface", blend_mode="Translucent")
        """
        params = {"material_path": material_path, "two_sided": two_sided}
        if blend_mode:
            params["blend_mode"] = blend_mode
        if shading_model:
            params["shading_model"] = shading_model
        if material_domain:
            params["material_domain"] = material_domain
        return __send_unreal_command("set_material_properties", params)

    @mcp.tool()
    def create_material_instance(
        ctx: Context,
        name: str,
        parent_material: str,
        path: str = "/Game/Materials",
        is_dynamic: bool = False,
    ) -> Dict:
        """
        Create a Material Instance from a parent material.

        Args:
            name: Instance name (e.g. "MI_Wood_Dark")
            parent_material: Path to parent material
            path: Content path for the instance
            is_dynamic: True for runtime-modifiable MaterialInstanceDynamic

        Example:
            create_material_instance(name="MI_Wood_Dark", parent_material="/Game/Materials/M_Wood")
        """
        return __send_unreal_command("create_material_instance", {
            "name": name,
            "parent_material": parent_material,
            "path": path,
            "is_dynamic": is_dynamic,
        })

    @mcp.tool()
    def set_material_parameter(
        ctx: Context,
        material_path: str,
        parameter_name: str,
        parameter_type: str,
        value: str = "",
        vector_value: List[float] = None,
        scalar_value: float = 0.0,
    ) -> Dict:
        """
        Set a parameter on a material instance.

        Args:
            material_path: Path to material instance
            parameter_name: Parameter name (must exist on parent)
            parameter_type: "scalar"|"vector"|"texture"
            value: Texture path for texture params
            vector_value: [R,G,B,A] for vector params
            scalar_value: float for scalar params

        Example:
            set_material_parameter(material_path="/Game/Materials/MI_Metal", parameter_name="Roughness", parameter_type="scalar", scalar_value=0.4)
        """
        params = {
            "material_path": material_path,
            "parameter_name": parameter_name,
            "parameter_type": parameter_type,
        }
        if parameter_type.lower() == "vector":
            params["value"] = vector_value or [0.0, 0.0, 0.0, 1.0]
        elif parameter_type.lower() == "scalar":
            params["value"] = scalar_value
        else:
            params["value"] = value
        return __send_unreal_command("set_material_parameter", params)

    @mcp.tool()
    def get_material_parameter(
        ctx: Context,
        material_path: str,
        parameter_name: str,
        parameter_type: str,
    ) -> Dict:
        """
        Get a material parameter value.

        Args:
            material_path: Path to material or instance
            parameter_name: Parameter name
            parameter_type: "scalar"|"vector"|"texture"

        Example:
            get_material_parameter("/Game/Materials/MI_Metal", "Roughness", "scalar")
        """
        return __send_unreal_command("get_material_parameter", {
            "material_path": material_path,
            "parameter_name": parameter_name,
            "parameter_type": parameter_type,
        })

    @mcp.tool()
    def get_material_metadata(
        ctx: Context,
        material_path: str,
        fields: List[str] = None,
    ) -> Dict:
        """
        Get material metadata including parameters and blend/shading settings.

        Args:
            material_path: Full path to the material
            fields: Optional filter list: "basic"|"parameters"|"properties"|"*"

        Example:
            get_material_metadata("/Game/Materials/M_Wood")
        """
        params = {"material_path": material_path}
        if fields:
            params["fields"] = fields
        return __send_unreal_command("get_material_metadata", params)

    @mcp.tool()
    def apply_material_to_actor(
        ctx: Context,
        actor_name: str,
        material_path: str,
        slot_index: int = 0,
        component_name: str = "",
    ) -> Dict:
        """
        Apply a material to an actor's mesh component.

        Args:
            actor_name: Actor name in the level
            material_path: Path to material
            slot_index: Material slot index
            component_name: Specific component name (empty = first mesh)

        Example:
            apply_material_to_actor(actor_name="Cube_01", material_path="/Game/Materials/M_Wood")
        """
        params = {
            "actor_name": actor_name,
            "material_path": material_path,
            "slot_index": slot_index,
        }
        if component_name:
            params["component_name"] = component_name
        return __send_unreal_command("apply_material_to_actor", params)

    @mcp.tool()
    def add_material_expression(
        ctx: Context,
        material_path: str,
        expression_type: str,
        position: List[float] = None,
        properties: Dict = None,
    ) -> Dict:
        """
        Add a material expression node. Use expression_type "Custom" for HLSL.

        Args:
            material_path: Path to material
            expression_type: "Constant"|"Constant3Vector"|"Add"|"Multiply"|"TextureSample"|"ScalarParameter"|"VectorParameter"|"Custom"|...
            position: [X, Y] editor graph position
            properties: Expression properties. For Custom HLSL use {"Code": "return float3(1,0,0);", "OutputType": 2, "Description": "Red"}

        Example:
            add_material_expression("/Game/Materials/M_Fire", "ScalarParameter", [0, 0], {"ParameterName": "EmissiveStrength", "DefaultValue": 5.0})
        """
        params = {
            "material_path": material_path,
            "expression_type": expression_type,
            "position": position or [0.0, 0.0],
        }
        if properties:
            params["properties"] = properties
        return __send_unreal_command("add_material_expression", params)

    @mcp.tool()
    def connect_material_expressions(
        ctx: Context,
        material_path: str,
        source_expression_id: str,
        target_expression_id: str,
        source_output_index: int = 0,
        target_input_name: str = "",
    ) -> Dict:
        """
        Connect two material expressions.

        Args:
            material_path: Path to material
            source_expression_id: Source expression GUID
            target_expression_id: Target expression GUID
            source_output_index: Output pin index
            target_input_name: Target input name ("A", "B", etc.)

        Example:
            connect_material_expressions("/Game/Materials/M_Fire", "guid-a", "guid-b", 0, "A")
        """
        return __send_unreal_command("connect_material_expressions", {
            "material_path": material_path,
            "source_expression_id": source_expression_id,
            "source_output_index": source_output_index,
            "target_expression_id": target_expression_id,
            "target_input_name": target_input_name,
        })

    @mcp.tool()
    def connect_expression_to_material_output(
        ctx: Context,
        material_path: str,
        expression_id: str,
        material_property: str,
        output_index: int = 0,
    ) -> Dict:
        """
        Connect an expression to a material output (PBR pins).

        Args:
            material_path: Path to material
            expression_id: Expression GUID
            material_property: "BaseColor"|"Metallic"|"Specular"|"Roughness"|"Normal"|"EmissiveColor"|"Opacity"|"OpacityMask"|"WorldPositionOffset"|"AmbientOcclusion"
            output_index: Output pin index

        Example:
            connect_expression_to_material_output("/Game/Materials/M_Fire", "guid-color", "BaseColor")
        """
        return __send_unreal_command("connect_expression_to_material_output", {
            "material_path": material_path,
            "expression_id": expression_id,
            "output_index": output_index,
            "material_property": material_property,
        })

    @mcp.tool()
    def get_material_graph_metadata(
        ctx: Context,
        material_path: str,
        fields: List[str] = None,
    ) -> Dict:
        """
        Inspect a material expression graph.

        Args:
            material_path: Path to material
            fields: "expressions"|"connections"|"material_outputs"|"orphans"|"flow"|"*"

        Example:
            get_material_graph_metadata("/Game/Materials/M_Fire", ["expressions", "connections"])
        """
        params = {"material_path": material_path}
        if fields:
            params["fields"] = fields
        return __send_unreal_command("get_material_expression_metadata", params)

    @mcp.tool()
    def set_material_expression_property(
        ctx: Context,
        material_path: str,
        expression_id: str,
        property_name: str,
        property_value: str = "",
    ) -> Dict:
        """
        Set a property on an existing material expression.

        Args:
            material_path: Path to material
            expression_id: Expression GUID
            property_name: Property name ("Constant", "ParameterName", "Code", "Texture", ...)
            property_value: New value as string

        Example:
            set_material_expression_property("/Game/Materials/M_Fire", "guid", "Code", "return float3(1,0.2,0);")
        """
        return __send_unreal_command("set_material_expression_property", {
            "material_path": material_path,
            "expression_id": expression_id,
            "property_name": property_name,
            "property_value": property_value,
        })

    @mcp.tool()
    def delete_material_expression(
        ctx: Context,
        material_path: str,
        expression_id: str,
    ) -> Dict:
        """
        Delete a material expression from the graph.

        Example:
            delete_material_expression("/Game/Materials/M_Fire", "guid")
        """
        return __send_unreal_command("delete_material_expression", {
            "material_path": material_path,
            "expression_id": expression_id,
        })

    @mcp.tool()
    def compile_material(ctx: Context, material_path: str) -> Dict:
        """
        Compile/apply a material and return validation info.

        Example:
            compile_material("/Game/Materials/M_Fire")
        """
        return __send_unreal_command("compile_material", {"material_path": material_path})

    logger.info("Material tools registered successfully")
