; tools/user/owl.nsi
;
; NSIS Script to build Win32 installer
;
; Copyright 2013 Rice University.
;
; http://www.embeddedpython.org/
;
; This file is part of the Owl Embedded Python System and is provided under
; the MIT open-source license. See the LICENSE and COPYING files for details
; about your rights to use, modify, and distribute Owl.

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "Owl Embedded Python System"
  OutFile "owl.exe"

  ;Default installation folder
  InstallDir "$LOCALAPPDATA\Owl Embedded Python"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Owl" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin

;--------------------------------
;Variables
  Var StartMenuFolder

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

;  !insertmacro MUI_PAGE_LICENSE "${NSISDIR}\Docs\Modern UI\License.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Complete" SecOwl

  SetOutPath "$INSTDIR"
  
  File "API-MS-Win-Core-Debug-L1-1-0.dll"
  File "API-MS-Win-Core-DelayLoad-L1-1-0.dll"
  File "API-MS-Win-Core-ErrorHandling-L1-1-0.dll"
  File "API-MS-Win-Core-File-L1-1-0.dll"
  File "API-MS-Win-Core-Handle-L1-1-0.dll"
  File "API-MS-Win-Core-Heap-L1-1-0.dll"
  File "API-MS-Win-Core-Interlocked-L1-1-0.dll"
  File "API-MS-Win-Core-IO-L1-1-0.dll"
  File "API-MS-Win-Core-LibraryLoader-L1-1-0.dll"
  File "API-MS-Win-Core-Localization-L1-1-0.dll"
  File "API-MS-Win-Core-LocalRegistry-L1-1-0.dll"
  File "API-MS-Win-Core-Misc-L1-1-0.dll"
  File "API-MS-Win-Core-ProcessEnvironment-L1-1-0.dll"
  File "API-MS-Win-Core-ProcessThreads-L1-1-0.dll"
  File "API-MS-Win-Core-Profile-L1-1-0.dll"
  File "API-MS-Win-Core-String-L1-1-0.dll"
  File "API-MS-Win-Core-Synch-L1-1-0.dll"
  File "API-MS-Win-Core-SysInfo-L1-1-0.dll"
  File "atk.pyd"
  File "bz2.pyd"
  File "cairo._cairo.pyd"
  File "DNSAPI.DLL"
  File "freetype6.dll"
  File "gdk-pixbuf-query-loaders.exe"
  File "gio._gio.pyd"
  File "glib._glib.pyd"
  File "gobject._gobject.pyd"
  File "gtk.glade.pyd"
  File "gtk._gtk.pyd"
  File "gtksourceview2.pyd"
  File "intl.dll"
  File "KERNELBASE.dll"
  File "libatk-1.0-0.dll"
  File "libcairo-2.dll"
  File "libexpat-1.dll"
  File "libfontconfig-1.dll"
  File "libgdk-win32-2.0-0.dll"
  File "libgdk_pixbuf-2.0-0.dll"
  File "libgio-2.0-0.dll"
  File "libglade-2.0-0.dll"
  File "libglib-2.0-0.dll"
  File "libgmodule-2.0-0.dll"
  File "libgobject-2.0-0.dll"
  File "libgthread-2.0-0.dll"
  File "libgtk-win32-2.0-0.dll"
  File "libgtksourceview-2.0-0.dll"
  File "libpango-1.0-0.dll"
  File "libpangocairo-1.0-0.dll"
  File "libpangoft2-1.0-0.dll"
  File "libpangowin32-1.0-0.dll"
  File "libpng14-14.dll"
  File "library.zip"
  File "libxml2-2.dll"
  File "MSIMG32.DLL"
  File "NSI.dll"
  File "owl.ico"
  File "owl.png"
  File "owlide.exe"
  File "pango.pyd"
  File "pangocairo.pyd"
  File "projecttree.glade"
  File "pyexpat.pyd"
  File "python27.dll"
  File "select.pyd"
  File "unicodedata.pyd"
  File "USP10.DLL"
  File "w9xpopen.exe"
  File "zlib1.dll"
  File "_ctypes.pyd"
  File "_hashlib.pyd"
  File "_socket.pyd"
  File "_ssl.pyd" 
  File /r "lib"
  File /r "etc"
  File /r "share"

  ;Store installation folder
  WriteRegStr HKCU "Software\Owl" "" $INSTDIR
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    
    ;Create shortcuts
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Owl.lnk" "$INSTDIR\owlide.exe"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

;--------------------------------
;Installer Sections

Section "Driver" SecDriver

  SetOutPath "$WINDIR\Inf"
  
  File "owl.inf"

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecOwl ${LANG_ENGLISH} "Install the Owl IDE and all necessary tools."
  LangString DESC_SecDriver ${LANG_ENGLISH} "Install the driver for the Owl Serial Port."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecOwl} $(DESC_SecOwl)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDriver} $(DESC_SecDriver)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  RMDir /r "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\Owl"

SectionEnd
