"""
Project Tools for Unreal MCP.

This module provides tools for managing project-wide settings and configuration.
"""

import logging
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_project_tools(mcp: FastMCP):
    """Register project tools with the MCP server."""
    
    @mcp.tool()
    def create_input_mapping(
        ctx: Context,
        action_name: str,
        key: str,
        input_type: str = "Action",
        shift: bool = False,
        ctrl: bool = False,
        alt: bool = False,
        cmd: bool = False
    ) -> Dict[str, Any]:
        """
        Create a legacy input mapping for the project.
        
        Args:
            action_name: Name of the input action
            key: Key to bind (SpaceBar, LeftMouseButton, etc.)
            input_type: Type of input mapping (Action or Axis)
            shift: Require Shift
            ctrl: Require Ctrl
            alt: Require Alt
            cmd: Require Cmd
            
        Example:
            create_input_mapping(action_name="Jump", key="SpaceBar")
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "action_name": action_name,
                "key": key,
                "input_type": input_type,
                "shift": shift,
                "ctrl": ctrl,
                "alt": alt,
                "cmd": cmd
            }
            
            logger.info(f"Creating input mapping '{action_name}' with key '{key}'")
            response = unreal.send_command("create_input_mapping", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input mapping creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating input mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def create_folder(ctx: Context, folder_path: str) -> Dict[str, Any]:
        """
        Create a content browser folder.

        Args:
            folder_path: Unreal content path, e.g. "/Game/VFX/Textures"

        Example:
            create_folder("/Game/Materials/Generated")
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            return unreal.send_command("create_folder", {"folder_path": folder_path}) or {}
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_enhanced_input_action(
        ctx: Context,
        action_name: str,
        path: str = "/Game/Input/Actions",
        description: str = "",
        value_type: str = "Digital"
    ) -> Dict[str, Any]:
        """
        Create an Enhanced Input Action asset (UE 5.5+).

        Args:
            action_name: Name of the action (IA_ prefix added if missing)
            path: Content path
            description: Optional description
            value_type: "Digital"|"Analog"|"Axis2D"|"Axis3D"

        Example:
            create_enhanced_input_action(action_name="Jump", value_type="Digital")
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            return unreal.send_command("create_enhanced_input_action", {
                "action_name": action_name,
                "path": path,
                "description": description,
                "value_type": value_type
            }) or {}
        except Exception as e:
            logger.error(f"Error creating Enhanced Input Action: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_input_mapping_context(
        ctx: Context,
        context_name: str,
        path: str = "/Game/Input",
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Create an Input Mapping Context asset.

        Example:
            create_input_mapping_context(context_name="Default")
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            return unreal.send_command("create_input_mapping_context", {
                "context_name": context_name,
                "path": path,
                "description": description
            }) or {}
        except Exception as e:
            logger.error(f"Error creating Input Mapping Context: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def add_mapping_to_context(
        ctx: Context,
        context_path: str,
        action_path: str,
        key: str,
        shift: bool = False,
        ctrl: bool = False,
        alt: bool = False,
        cmd: bool = False
    ) -> Dict[str, Any]:
        """
        Add a key mapping with optional modifiers to an Input Mapping Context.

        Args:
            context_path: Full path to the IMC asset
            action_path: Full path to the Input Action asset
            key: Key to bind (SpaceBar, LeftMouseButton, W, ...)
            shift, ctrl, alt, cmd: Modifier keys

        Example:
            add_mapping_to_context("/Game/Input/IMC_Default", "/Game/Input/Actions/IA_Jump", "SpaceBar")
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            return unreal.send_command("add_mapping_to_context", {
                "context_path": context_path,
                "action_path": action_path,
                "key": key,
                "shift": shift,
                "ctrl": ctrl,
                "alt": alt,
                "cmd": cmd
            }) or {}
        except Exception as e:
            logger.error(f"Error adding mapping to context: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_struct(
        ctx: Context,
        struct_name: str,
        path: str = "/Game/Data",
        description: str = "",
        properties: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a user-defined struct.

        Args:
            struct_name: Struct asset name
            path: Content path
            description: Optional description
            properties: List of {name, type} e.g. [{"name": "Health", "type": "Float"}]

        Example:
            create_struct("DamageInfo", "/Game/Data", properties=[{"name": "Amount", "type": "Float"}])
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            return unreal.send_command("create_struct", {
                "struct_name": struct_name,
                "path": path,
                "description": description,
                "properties": properties or []
            }) or {}
        except Exception as e:
            logger.error(f"Error creating struct: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def get_project_metadata(
        ctx: Context,
        path: str = "/Game",
        fields: List[str] = None
    ) -> Dict[str, Any]:
        """
        Query project structure: folders, Input Actions, Mapping Contexts, and structs.

        Args:
            path: Folder to inspect
            fields: Optional filter, e.g. ["input_actions", "input_mapping_contexts", "structs", "folders"]

        Example:
            get_project_metadata("/Game/Input", ["input_actions", "input_mapping_contexts"])
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"path": path}
            if fields:
                params["fields"] = fields
            return unreal.send_command("get_project_metadata", params) or {}
        except Exception as e:
            logger.error(f"Error getting project metadata: {e}")
            return {"success": False, "message": str(e)}
    
    logger.info("Project tools registered successfully") 