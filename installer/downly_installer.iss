; Enable download support
#define MyAppVersion "0.3.0"

[Setup]
; Basic application information
AppName=Downly
AppVersion={#MyAppVersion}
AppPublisher=Morgpo
AppPublisherURL=https://github.com/Morgpo/Downly
AppSupportURL=https://github.com/Morgpo/Downly/issues
AppUpdatesURL=https://github.com/Morgpo/Downly/releases
DefaultDirName={autopf}\Downly
DefaultGroupName=Downly
AllowNoIcons=yes
LicenseFile=
InfoBeforeFile=
InfoAfterFile=
OutputDir=..\installer_output
OutputBaseFilename=Downly-Setup-v{#MyAppVersion}
SetupIconFile=..\src\assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
DisableReadyPage=no
DisableFinishedPage=no
PrivilegesRequired=admin

; Minimum Windows version (Windows 7 SP1)
MinVersion=6.1.7601

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
; Include the entire dist/downly directory
Source: "..\dist\downly\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Include README and other documentation
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
; Include icon for shortcuts
Source: "..\src\assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; Include license if you have one
; Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Downly"; Filename: "{app}\downly.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"
Name: "{group}\{cm:UninstallProgram,Downly}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Downly"; Filename: "{app}\downly.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Downly"; Filename: "{app}\downly.exe"; WorkingDir: "{app}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\downly.exe"; Description: "{cm:LaunchProgram,Downly}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Add any post-install tasks here if needed
  end;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
  // Add any pre-install checks here if needed
end;
