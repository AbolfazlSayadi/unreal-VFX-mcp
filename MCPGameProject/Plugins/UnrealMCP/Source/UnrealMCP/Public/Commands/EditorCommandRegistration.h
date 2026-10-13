#pragma once

#include "CoreMinimal.h"
#include "Commands/IUnrealMCPCommand.h"

/**
 * Registers editor commands that are not handled by the legacy editor handler
 * (console, performance stats, viewport camera).
 */
class UNREALMCP_API FEditorCommandRegistration
{
public:
	static void RegisterAllCommands();
	static void UnregisterAllCommands();

private:
	static TArray<TSharedPtr<class IUnrealMCPCommand>> RegisteredCommands;
	static void RegisterAndTrackCommand(TSharedPtr<class IUnrealMCPCommand> Command);
};
