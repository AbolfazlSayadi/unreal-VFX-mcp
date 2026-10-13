#include "Commands/EditorCommandRegistration.h"
#include "Commands/UnrealMCPCommandRegistry.h"
#include "Commands/Editor/ExecuteConsoleCommandCommand.h"
#include "Commands/Editor/GetPerformanceStatsCommand.h"
#include "Commands/Editor/SetViewportCameraCommand.h"

TArray<TSharedPtr<IUnrealMCPCommand>> FEditorCommandRegistration::RegisteredCommands;

void FEditorCommandRegistration::RegisterAllCommands()
{
	UE_LOG(LogTemp, Log, TEXT("Registering extra Editor commands..."));
	RegisterAndTrackCommand(MakeShared<FExecuteConsoleCommandCommand>());
	RegisterAndTrackCommand(MakeShared<FGetPerformanceStatsCommand>());
	RegisterAndTrackCommand(MakeShared<FSetViewportCameraCommand>());
	UE_LOG(LogTemp, Log, TEXT("Registered %d extra Editor commands"), RegisteredCommands.Num());
}

void FEditorCommandRegistration::UnregisterAllCommands()
{
	FUnrealMCPCommandRegistry& Registry = FUnrealMCPCommandRegistry::Get();
	for (const TSharedPtr<IUnrealMCPCommand>& Command : RegisteredCommands)
	{
		if (Command.IsValid())
		{
			Registry.UnregisterCommand(Command->GetCommandName());
		}
	}
	RegisteredCommands.Empty();
}

void FEditorCommandRegistration::RegisterAndTrackCommand(TSharedPtr<IUnrealMCPCommand> Command)
{
	if (!Command.IsValid())
	{
		return;
	}

	if (FUnrealMCPCommandRegistry::Get().RegisterCommand(Command))
	{
		RegisteredCommands.Add(Command);
	}
}
