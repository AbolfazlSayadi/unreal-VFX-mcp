#include "Commands/UnrealMCPVfxDispatcher.h"
#include "Commands/UnrealMCPCommandRegistry.h"
#include "Commands/NiagaraCommandRegistration.h"
#include "Commands/MaterialCommandRegistration.h"
#include "Commands/EditorCommandRegistration.h"
#include "Commands/ProjectCommandRegistration.h"
#include "Services/ProjectService.h"

namespace
{
	TSharedPtr<FProjectService> GProjectService;
}

FUnrealMCPVfxDispatcher& FUnrealMCPVfxDispatcher::Get()
{
	static FUnrealMCPVfxDispatcher Instance;
	return Instance;
}

void FUnrealMCPVfxDispatcher::Initialize()
{
	if (bIsInitialized)
	{
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("FUnrealMCPVfxDispatcher: Registering Niagara, Material, Editor, and Project commands"));
	FNiagaraCommandRegistration::RegisterAllCommands();
	FMaterialCommandRegistration::RegisterAllCommands();
	FEditorCommandRegistration::RegisterAllCommands();

	GProjectService = MakeShared<FProjectService>();
	FProjectCommandRegistration::RegisterCommands(FUnrealMCPCommandRegistry::Get(), GProjectService);

	bIsInitialized = true;
}

void FUnrealMCPVfxDispatcher::Shutdown()
{
	if (!bIsInitialized)
	{
		return;
	}

	FEditorCommandRegistration::UnregisterAllCommands();
	FMaterialCommandRegistration::UnregisterAllCommands();
	FNiagaraCommandRegistration::UnregisterAllCommands();
	FUnrealMCPCommandRegistry::Get().ClearRegistry();
	GProjectService.Reset();
	bIsInitialized = false;
}
