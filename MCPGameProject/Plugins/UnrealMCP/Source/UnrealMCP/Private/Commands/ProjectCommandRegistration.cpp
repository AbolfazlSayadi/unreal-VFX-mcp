#include "Commands/ProjectCommandRegistration.h"
#include "Commands/UnrealMCPCommandRegistry.h"
#include "Commands/Project/CreateFolderCommand.h"
#include "Commands/Project/CreateStructCommand.h"
#include "Commands/Project/UpdateStructCommand.h"
#include "Commands/Project/GetStructPinNamesCommand.h"
#include "Commands/Project/GetProjectMetadataCommand.h"
#include "Commands/Project/CreateEnhancedInputActionCommand.h"
#include "Commands/Project/CreateInputMappingContextCommand.h"
#include "Commands/Project/AddMappingToContextCommand.h"
#include "Commands/Project/RemoveMappingFromContextCommand.h"
#include "Commands/Project/SetInputActionMappableSettingsCommand.h"
#include "Commands/Project/SetIMCMappingSettingsCommand.h"
#include "Services/IProjectService.h"

void FProjectCommandRegistration::RegisterCommands(FUnrealMCPCommandRegistry& Registry, TSharedPtr<IProjectService> ProjectService)
{
	if (!ProjectService.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("ProjectService is null, cannot register project commands"));
		return;
	}

	Registry.RegisterCommand(MakeShared<FCreateFolderCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FCreateStructCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FUpdateStructCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FGetStructPinNamesCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FGetProjectMetadataCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FCreateEnhancedInputActionCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FCreateInputMappingContextCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FAddMappingToContextCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FRemoveMappingFromContextCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FSetInputActionMappableSettingsCommand>(ProjectService));
	Registry.RegisterCommand(MakeShared<FSetIMCMappingSettingsCommand>(ProjectService));

	UE_LOG(LogTemp, Log, TEXT("Registered project organization commands"));
}
