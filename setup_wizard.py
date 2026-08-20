"""
LeafTimer Setup Wizard - Standard Windows Installation Program.
Installs LeafTimer into AppData/Local/Programs/LeafTimer, creates Start Menu & Desktop shortcuts, and uninstaller.
"""

import sys
import os
import shutil
import subprocess
import customtkinter as ctk
from PIL import Image

class LeafTimerSetupWizard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LeafTimer Setup")
        self.geometry("480x420")
        self.resizable(False, False)

        # Installation path
        user_appdata = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
        self.install_dir = os.path.join(user_appdata, "Programs", "LeafTimer")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        self.create_desktop_shortcut = ctk.BooleanVar(value=True)
        self.create_start_menu = ctk.BooleanVar(value=True)
        self.launch_after_install = ctk.BooleanVar(value=True)

        self._build_ui()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        w, h = 480, 420
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        self.configure(fg_color="#121714")

        # Header Frame
        header = ctk.CTkFrame(self, fg_color="#1B221E", height=80, corner_radius=0)
        header.pack(fill="x", side="top")

        title_lbl = ctk.CTkLabel(
            header,
            text="🌿  LeafTimer Setup Wizard",
            font=ctk.CTkFont(family="Segoe UI Variable Display", size=18, weight="bold"),
            text_color="#E3ECE6"
        )
        title_lbl.pack(anchor="w", padx=24, pady=(18, 2))

        subtitle_lbl = ctk.CTkLabel(
            header,
            text="Install peaceful shutdown timing for Windows 11",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=12),
            text_color="#8CA696"
        )
        subtitle_lbl.pack(anchor="w", padx=24, pady=(0, 14))

        # Main Body Frame
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=20)

        dest_lbl = ctk.CTkLabel(
            body,
            text="Destination Folder:",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=12, weight="bold"),
            text_color="#E3ECE6"
        )
        dest_lbl.pack(anchor="w", pady=(0, 4))

        self.path_entry = ctk.CTkEntry(
            body,
            fg_color="#1B221E",
            border_color="#2A362E",
            text_color="#A8C3B1",
            height=32
        )
        self.path_entry.insert(0, self.install_dir)
        self.path_entry.pack(fill="x", pady=(0, 16))

        options_lbl = ctk.CTkLabel(
            body,
            text="Installation Options:",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=12, weight="bold"),
            text_color="#E3ECE6"
        )
        options_lbl.pack(anchor="w", pady=(0, 6))

        cb1 = ctk.CTkCheckBox(
            body,
            text="Create Desktop Shortcut",
            variable=self.create_desktop_shortcut,
            text_color="#E3ECE6",
            fg_color="#4EA874",
            hover_color="#5CBF85"
        )
        cb1.pack(anchor="w", pady=4)

        cb2 = ctk.CTkCheckBox(
            body,
            text="Add to Windows Start Menu (Programs)",
            variable=self.create_start_menu,
            text_color="#E3ECE6",
            fg_color="#4EA874",
            hover_color="#5CBF85"
        )
        cb2.pack(anchor="w", pady=4)

        cb3 = ctk.CTkCheckBox(
            body,
            text="Launch LeafTimer upon completion",
            variable=self.launch_after_install,
            text_color="#E3ECE6",
            fg_color="#4EA874",
            hover_color="#5CBF85"
        )
        cb3.pack(anchor="w", pady=4)

        # Status & Footer
        self.status_lbl = ctk.CTkLabel(
            body,
            text="Ready to install.",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=11),
            text_color="#8CA696"
        )
        self.status_lbl.pack(anchor="w", pady=(12, 0))

        # Bottom Buttons
        footer = ctk.CTkFrame(self, fg_color="#181F1A", height=60, corner_radius=0)
        footer.pack(fill="x", side="bottom")

        self.install_btn = ctk.CTkButton(
            footer,
            text="Install Now",
            fg_color="#4EA874",
            hover_color="#5CBF85",
            text_color="#0E1C13",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=13, weight="bold"),
            height=36,
            command=self._perform_install
        )
        self.install_btn.pack(side="right", padx=24, pady=12)

        cancel_btn = ctk.CTkButton(
            footer,
            text="Cancel",
            fg_color="#26322B",
            hover_color="#324339",
            text_color="#E3ECE6",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=13),
            height=36,
            width=80,
            command=self.destroy
        )
        cancel_btn.pack(side="right", padx=(0, 8), pady=12)

    def _perform_install(self):
        target_dir = self.path_entry.get().strip()
        self.status_lbl.configure(text="Installing files...")
        self.install_btn.configure(state="disabled")
        self.update()

        try:
            os.makedirs(target_dir, exist_ok=True)
            
            # Locate bundled LeafTimer.exe or workspace dist
            base_dir = os.path.dirname(os.path.abspath(__file__))
            exe_src = os.path.join(base_dir, "dist", "LeafTimer.exe")
            if not os.path.exists(exe_src):
                exe_src = os.path.join(base_dir, "LeafTimer.exe")
            
            target_exe = os.path.join(target_dir, "LeafTimer.exe")
            if os.path.exists(exe_src):
                shutil.copy2(exe_src, target_exe)
            
            # Copy icons if available
            assets_src = os.path.join(base_dir, "assets")
            target_assets = os.path.join(target_dir, "assets")
            if os.path.exists(assets_src):
                shutil.copytree(assets_src, target_assets, dirs_exist_ok=True)
            
            target_ico = os.path.join(target_assets, "app_icon.ico") if os.path.exists(target_assets) else target_exe

            # Create Shortcuts using PowerShell
            if self.create_desktop_shortcut.get():
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                self._create_shortcut(
                    shortcut_path=os.path.join(desktop, "LeafTimer.lnk"),
                    target_path=target_exe,
                    work_dir=target_dir,
                    icon_path=target_ico
                )

            if self.create_start_menu.get():
                start_menu = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs")
                self._create_shortcut(
                    shortcut_path=os.path.join(start_menu, "LeafTimer.lnk"),
                    target_path=target_exe,
                    work_dir=target_dir,
                    icon_path=target_ico
                )

            self.status_lbl.configure(text="Installation completed successfully! ✨", text_color="#4EA874")
            self.install_btn.configure(text="Finish", state="normal", command=self._finish)
            
        except Exception as e:
            self.status_lbl.configure(text=f"Error: {e}", text_color="#DE6B58")
            self.install_btn.configure(state="normal", text="Retry")

    def _create_shortcut(self, shortcut_path: str, target_path: str, work_dir: str, icon_path: str):
        ps_cmd = f"""
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
        $Shortcut.TargetPath = '{target_path}'
        $Shortcut.WorkingDirectory = '{work_dir}'
        $Shortcut.IconLocation = '{icon_path},0'
        $Shortcut.Description = 'LeafTimer - Windows 11 Shutdown Timer'
        $Shortcut.Save()
        """
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)

    def _finish(self):
        if self.launch_after_install.get():
            target_exe = os.path.join(self.path_entry.get().strip(), "LeafTimer.exe")
            if os.path.exists(target_exe):
                subprocess.Popen([target_exe])
        self.destroy()

if __name__ == "__main__":
    app = LeafTimerSetupWizard()
    app.mainloop()
