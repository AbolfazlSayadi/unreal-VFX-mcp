#include "Commands/UnrealMCPVfxDispatcher.h"
#include "Commands/UnrealMCPCommandRegistry.h"
#include "Commands/NiagaraCommandRegistration.h"

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

	UE_LOG(LogTemp, Log, TEXT("FUnrealMCPVfxDispatcher: Registering Niagara VFX commands"));
	FNiagaraCommandRegistration::RegisterAllCommands();
	bIsInitialized = true;
}

void FUnrealMCPVfxDispatcher::Shutdown()
{
	if (!bIsInitialized)
	{
		return;
	}

	FNiagaraCommandRegistration::UnregisterAllCommands();
	FUnrealMCPCommandRegistry::Get().ClearRegistry();
	bIsInitialized = false;
}
