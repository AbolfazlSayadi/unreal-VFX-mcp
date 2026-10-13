#include "UnrealMCPModule.h"
#include "UnrealMCPBridge.h"
#include "Commands/UnrealMCPVfxDispatcher.h"
#include "Modules/ModuleManager.h"
#include "EditorSubsystem.h"
#include "Editor.h"

#define LOCTEXT_NAMESPACE "FUnrealMCPModule"

void FUnrealMCPModule::StartupModule()
{
	FUnrealMCPVfxDispatcher::Get().Initialize();
	UE_LOG(LogTemp, Display, TEXT("Unreal MCP Module has started (Niagara, Material, Editor, Project commands registered)"));
}

void FUnrealMCPModule::ShutdownModule()
{
	FUnrealMCPVfxDispatcher::Get().Shutdown();
	UE_LOG(LogTemp, Display, TEXT("Unreal MCP Module has shut down"));
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FUnrealMCPModule, UnrealMCP) 