; -------- Inno Setup Script for MakeFlashcards --------
[Setup]
AppId={{A5D9B1C7-3B3D-4C4A-BF0E-0D47F7C2B2C9}
AppName=MakeFlashcards
AppVersion=1.0.0
AppPublisher=Your Name or Company
DefaultDirName={commonpf32}\MakeFlashcards
DefaultGroupName=MakeFlashcards
UninstallDisplayIcon={app}\MakeFlashcards.exe
OutputDir=.
OutputBaseFilename=MakeFlashcardsSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"

[Files]
; Point this to your PyInstaller output
Source: "dist\MakeFlashcards.exe"; DestDir: "{app}"; DestName: "MakeFlashcards.exe"; Flags: ignoreversion

[Icons]
Name: "{group}\MakeFlashcards"; Filename: "{app}\MakeFlashcards.exe"
Name: "{commondesktop}\MakeFlashcards"; Filename: "{app}\MakeFlashcards.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\MakeFlashcards.exe"; Description: "Launch MakeFlashcards"; Flags: nowait postinstall skipifsilent
