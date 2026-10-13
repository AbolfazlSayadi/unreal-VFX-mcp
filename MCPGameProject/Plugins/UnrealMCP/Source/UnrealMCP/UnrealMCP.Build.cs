// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class UnrealMCP : ModuleRules
{
	public UnrealMCP(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;
		// Use IWYUSupport instead of the deprecated bEnforceIWYU in UE5.5
		IWYUSupport = IWYUSupport.Full;

		PublicIncludePaths.AddRange(
			new string[] {
				// ... add public include paths required here ...
			}
		);
		
		PrivateIncludePaths.AddRange(
			new string[] {
				// ... add other private include paths required here ...
			}
		);

		string NiagaraEditorPrivatePath = System.IO.Path.GetFullPath(System.IO.Path.Combine(EngineDirectory, "Plugins", "FX", "Niagara", "Source", "NiagaraEditor", "Private"));
		if (System.IO.Directory.Exists(NiagaraEditorPrivatePath))
		{
			PrivateIncludePaths.Add(NiagaraEditorPrivatePath);
		}

		string NiagaraInternalPath = System.IO.Path.GetFullPath(System.IO.Path.Combine(EngineDirectory, "Plugins", "FX", "Niagara", "Source", "Niagara", "Internal"));
		if (System.IO.Directory.Exists(NiagaraInternalPath))
		{
			PrivateIncludePaths.Add(NiagaraInternalPath);
		}

		string NiagaraShaderInternalPath = System.IO.Path.GetFullPath(System.IO.Path.Combine(EngineDirectory, "Plugins", "FX", "Niagara", "Source", "NiagaraShader", "Internal"));
		if (System.IO.Directory.Exists(NiagaraShaderInternalPath))
		{
			PrivateIncludePaths.Add(NiagaraShaderInternalPath);
		}
		
		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"CoreUObject",
				"Engine",
				"InputCore",
				"EnhancedInput",
				"Networking",
				"Sockets",
				"HTTP",
				"Json",
				"JsonUtilities",
				"DeveloperSettings",
				"EditorScriptingUtilities",
				"AssetTools"
			}
		);
		
		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"UnrealEd",
				"EditorScriptingUtilities",
				"EditorSubsystem",
				"Slate",
				"SlateCore",
				"UMG",
				"Kismet",
				"KismetCompiler",
				"BlueprintGraph",
				"Projects",
				"AssetRegistry",
				"EnhancedInput",
				"RenderCore",
				"RHI"
			}
		);
		
		if (Target.bBuildEditor == true)
		{
			PrivateDependencyModuleNames.AddRange(
				new string[]
				{
					"PropertyEditor",      // For widget property editing
					"ToolMenus",           // For editor UI
					"BlueprintEditorLibrary", // For Blueprint utilities
					"UMGEditor",           // For WidgetBlueprint.h and other UMG editor functionality
					"AssetTools",
					"MaterialEditor",
					"EditorFramework",
					"LevelEditor",
					"Niagara",
					"NiagaraCore",
					"NiagaraEditor",
					"NiagaraShader"
				}
			);
		}
		
		DynamicallyLoadedModuleNames.AddRange(
			new string[]
			{
				// ... add any modules that your module loads dynamically here ...
			}
		);
	}
} 