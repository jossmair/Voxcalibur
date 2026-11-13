[Setup]
AppId={{D90443F2-7D68-4E34-94BE-5D2014C639F7}
AppName=Voxcalibur
AppVersion=1.0.0
AppPublisher=Voxcalibur
DefaultDirName={localappdata}\Programs\Voxcalibur
DefaultGroupName=Voxcalibur
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir=..\dist
OutputBaseFilename=Voxcalibur-1.0.0-Setup
SetupIconFile=..\assets\voxcalibur.ico
UninstallDisplayIcon={app}\Voxcalibur.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Files]
Source: "..\dist\Voxcalibur-1.0.0\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Voxcalibur"; Filename: "{app}\Voxcalibur.exe"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Voxcalibur"; ValueData: """{app}\Voxcalibur.exe"" --minimized"; Flags: uninsdeletevalue

[Run]
Filename: "{app}\Voxcalibur.exe"; Parameters: "--show"; Flags: nowait skipifsilent

; User models/preferences are deliberately retained. No recursive user data deletion.
