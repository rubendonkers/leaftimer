# PowerShell script to install LeafTimer shortcut on Desktop and Start Menu

$WshShell = New-Object -comObject WScript.Shell
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetFile = Join-Path $ScriptDir "run.bat"
$IconFile = Join-Path $ScriptDir "assets\app_icon.ico"

# If standalone exe exists in dist, prioritize it
$ExeFile = Join-Path $ScriptDir "dist\LeafTimer.exe"
if (Test-Path $ExeFile) {
    $TargetFile = $ExeFile
}

# 1. Create Desktop Shortcut
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$DesktopShortcutPath = Join-Path $DesktopPath "LeafTimer.lnk"
$Shortcut = $WshShell.CreateShortcut($DesktopShortcutPath)
$Shortcut.TargetPath = $TargetFile
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.IconLocation = "$IconFile, 0"
$Shortcut.Description = "LeafTimer - Modern Windows 11 Shutdown Timer"
$Shortcut.Save()

# 2. Create Start Menu Shortcut
$StartMenuPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::StartMenu)
$ProgramsPath = Join-Path $StartMenuPath "Programs"
$StartShortcutPath = Join-Path $ProgramsPath "LeafTimer.lnk"
$StartShortcut = $WshShell.CreateShortcut($StartShortcutPath)
$StartShortcut.TargetPath = $TargetFile
$StartShortcut.WorkingDirectory = $ScriptDir
$StartShortcut.IconLocation = "$IconFile, 0"
$StartShortcut.Description = "LeafTimer - Modern Windows 11 Shutdown Timer"
$StartShortcut.Save()

Write-Host "=================================================" -ForegroundColor Green
Write-Host " LeafTimer installed successfully!               " -ForegroundColor Green
Write-Host " Shortcuts created:                              " -ForegroundColor Cyan
Write-Host "  • Desktop: $DesktopShortcutPath                " -ForegroundColor White
Write-Host "  • Start Menu: $StartShortcutPath               " -ForegroundColor White
Write-Host "=================================================" -ForegroundColor Green
