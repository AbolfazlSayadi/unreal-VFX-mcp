#Requires -Version 5.1
<#
.SYNOPSIS
  Copy UnrealMCP into a UE project and optionally build the editor target.

.EXAMPLE
  .\Scripts\Install-UnrealMCP-Plugin.ps1 -ProjectRoot "D:\Projects\JAssets2UEFN"

.EXAMPLE
  .\Scripts\Install-UnrealMCP-Plugin.ps1 -ProjectRoot "D:\Projects\JAssets2UEFN" -EngineRoot "C:\Program Files\Epic Games\UE_5.6" -Build
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $ProjectRoot,

    [string] $EngineRoot = "",

    [switch] $Build,

    [ValidateSet("Development Editor", "Development")]
    [string] $Target = "Development Editor",

    [string] $Platform = "Win64"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$PluginSource = Join-Path $RepoRoot "MCPGameProject\Plugins\UnrealMCP"
if (-not (Test-Path $PluginSource)) {
    throw "Plugin source not found: $PluginSource (run this script from a cloned unreal-mcp repo)"
}

$ProjectRoot = $ProjectRoot.TrimEnd('\')
if (-not (Test-Path $ProjectRoot)) {
    throw "Project folder does not exist: $ProjectRoot"
}

$UProject = Get-ChildItem -Path $ProjectRoot -Filter "*.uproject" -File | Select-Object -First 1
if (-not $UProject) {
    throw "No .uproject file in $ProjectRoot"
}

$PluginsDir = Join-Path $ProjectRoot "Plugins"
$PluginDest = Join-Path $PluginsDir "UnrealMCP"
New-Item -ItemType Directory -Force -Path $PluginsDir | Out-Null

Write-Host "Copying UnrealMCP plugin..."
if (Test-Path $PluginDest) {
    Write-Host "  Removing existing $PluginDest"
    Remove-Item -Recurse -Force $PluginDest
}
Copy-Item -Path $PluginSource -Destination $PluginDest -Recurse
Write-Host "  -> $PluginDest"

# Enable plugin in .uproject (merge if missing)
$uprojectPath = $UProject.FullName
$json = Get-Content -Raw -Path $uprojectPath | ConvertFrom-Json
if (-not $json.Plugins) {
    $json | Add-Member -NotePropertyName Plugins -NotePropertyValue @()
}
$existing = @($json.Plugins | Where-Object { $_.Name -eq "UnrealMCP" })
if ($existing.Count -eq 0) {
    $json.Plugins += @{
        Name    = "UnrealMCP"
        Enabled = $true
    }
    Write-Host "Added UnrealMCP to $($UProject.Name)"
} else {
    $existing[0].Enabled = $true
    Write-Host "UnrealMCP already listed in $($UProject.Name); set Enabled=true"
}
$json | ConvertTo-Json -Depth 10 | Set-Content -Path $uprojectPath -Encoding UTF8

if (-not $Build) {
    Write-Host ""
    Write-Host "Done. Next steps:"
    Write-Host "  1. Right-click $($UProject.Name) -> Generate Visual Studio project files"
    Write-Host "  2. Open the .sln and build target: $Target"
    Write-Host "  3. Or re-run with -Build and -EngineRoot pointing to UE 5.6"
    exit 0
}

if ([string]::IsNullOrWhiteSpace($EngineRoot)) {
    $guess = "C:\Program Files\Epic Games\UE_5.6"
    if (Test-Path $guess) { $EngineRoot = $guess }
}
if (-not (Test-Path $EngineRoot)) {
    throw "UE engine not found. Pass -EngineRoot 'C:\Program Files\Epic Games\UE_5.6'"
}

$BuildBat = Join-Path $EngineRoot "Engine\Build\BatchFiles\Build.bat"
if (-not (Test-Path $BuildBat)) {
    throw "Build.bat not found under $EngineRoot"
}

$ProjectName = [System.IO.Path]::GetFileNameWithoutExtension($UProject.Name)
Write-Host "Generating project files..."
$UBT = Join-Path $EngineRoot "Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.dll"
$GenCmd = @(
    $UBT,
    "-projectfiles",
    "-project=`"$uprojectPath`"",
    "-game",
    "-rocket",
    "-progress"
)
& dotnet $GenCmd
if ($LASTEXITCODE -ne 0) {
    throw "Generate project files failed (exit $LASTEXITCODE)"
}

Write-Host "Building $ProjectName $Target $Platform ..."
& $BuildBat $ProjectName $Platform $Target "-project=`"$uprojectPath`"" -WaitMutex
if ($LASTEXITCODE -ne 0) {
    throw "Build failed (exit $LASTEXITCODE)"
}

Write-Host ""
Write-Host "Build succeeded. Open the project in UE 5.6 and confirm Plugins -> UnrealMCP is enabled."
Write-Host "MCP listens on 127.0.0.1:55557 when the editor runs."
