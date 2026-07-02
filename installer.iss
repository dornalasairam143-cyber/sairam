#define MyAppName "Dashboard Launcher"
#define MyAppVersion "1.0"
#define MyAppPublisher "Sai Ram"
#define MyAppExeName "Dashboard Launcher.exe"

[Setup]
AppId={{7F41F5C5-71A1-4AA0-B2E4-123456789999}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Dashboard Launcher
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=Installer
OutputBaseFilename=DashboardLauncherSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create Desktop Shortcut"; GroupDescription: "Additional Shortcuts:"

[Files]
Source: "dist\Dashboard Launcher.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Dashboard Launcher"; Filename: "{app}\Dashboard Launcher.exe"
Name: "{autodesktop}\Dashboard Launcher"; Filename: "{app}\Dashboard Launcher.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Dashboard Launcher.exe"; Description: "Launch Dashboard Launcher"; Flags: nowait postinstall skipifsilent
