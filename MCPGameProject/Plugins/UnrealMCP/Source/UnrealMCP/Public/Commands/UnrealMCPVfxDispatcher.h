#pragma once

#include "CoreMinimal.h"

/**
 * Registers and routes Niagara / VFX MCP commands through the command registry.
 */
class UNREALMCP_API FUnrealMCPVfxDispatcher
{
public:
	static FUnrealMCPVfxDispatcher& Get();

	void Initialize();
	void Shutdown();

	bool IsInitialized() const { return bIsInitialized; }

private:
	FUnrealMCPVfxDispatcher() = default;

	bool bIsInitialized = false;
};
