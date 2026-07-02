;=========================================================
; Dashboard Launcher Installer
; Author : Sai Ram
;=========================================================

#define MyAppName "Dashboard Launcher"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Sai Ram"
#define MyAppExeName "Dashboard Launcher.exe"

[Setup]

AppId={{D5E77E6D-3D4F-4D9E-B6A4-123456789001}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://github.com/dornalasairam143-cyber/sairam
AppSupportURL=https://github.com/dornalasairam143-cyber/sairam
AppUpdatesURL=https://github.com/dornalasairam143-cyber/sairam

DefaultDirName={autopf}\Dashboard Launcher
DefaultGroupName=Dashboard Launcher

DisableProgramGroupPage=yes
AllowNoIcons=yes

OutputDir=Installer
OutputBaseFilename=DashboardLauncherSetup

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

ArchitecturesInstallIn64BitMode=x64compatible

PrivilegesRequired=admin

SetupIconFile=launcher.ico

UninstallDisplayIcon={app}\Dashboard Launcher.exe

WizardImageStretch=no

DisableDirPage=no

DisableReadyMemo=no

DisableWelcomePage=no

DisableFinishedPage=no

[Languages]

Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]

Name: "desktopicon"; Description: "Create Desktop Shortcut"; GroupDescription: "Additional Icons:"; Flags: unchecked

[Files]

Source: "dist\Dashboard Launcher.exe"; DestDir: "{app}"; Flags: ignoreversion

Source: "launcher.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]

Name: "{group}\Dashboard Launcher"; \
Filename: "{app}\Dashboard Launcher.exe"; \
IconFilename: "{app}\launcher.ico"

Name: "{autodesktop}\Dashboard Launcher"; \
Filename: "{app}\Dashboard Launcher.exe"; \
IconFilename: "{app}\launcher.ico"; \
Tasks: desktopicon

[Run]

Filename: "{app}\Dashboard Launcher.exe"; \
Description: "Launch Dashboard Launcher"; \
Flags: nowait postinstall skipifsilent

[UninstallDelete]

Type: filesandordirs; Name: "{userdocs}\LauncherFiles"

[Code]

procedure CurStepChanged(CurStep: TSetupStep);
begin
    if CurStep=ssInstall then
    begin
        WizardForm.StatusLabel.Caption :=
        'Installing Dashboard Launcher...';
    end;

    if CurStep=ssPostInstall then
    begin
        WizardForm.StatusLabel.Caption :=
        'Installation Completed.';
    end;
end;
