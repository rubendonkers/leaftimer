"""
LeafTimer - Simplistic, modern Windows 11 shutdown timer with a touch of nature.
"""

import sys
import os
import math
from datetime import datetime, timedelta
from typing import List

import customtkinter as ctk
from PIL import Image

from theme import NatureTheme
from timer_engine import ShutdownTimerEngine
from assets import get_asset_path, ensure_assets

class LeafTimerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ensure assets exist
        png_icon, ico_icon = ensure_assets()

        # Window Configuration
        self.title("LeafTimer")
        self.geometry("440x620")
        self.resizable(False, False)
        
        # Windows App ID and Icons
        try:
            if sys.platform == "win32":
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("LeafTimer.NatureShutdown.1.0")
                self.iconbitmap(ico_icon)
        except Exception:
            pass

        # Set default appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        # State Variables
        self.timer_engine = ShutdownTimerEngine()
        self.timer_engine.on_tick = self._on_timer_tick
        self.timer_engine.on_finished = self._on_timer_finished
        self.timer_engine.on_cancelled = self._on_timer_cancelled

        self.selected_minutes = ctk.IntVar(value=45)
        self.action_type = ctk.StringVar(value=ShutdownTimerEngine.ACTION_SHUTDOWN)
        self.is_dark_mode = True

        # Quick preset values
        self.presets = [15, 30, 45, 60, 90, 120]
        self.preset_buttons: List[ctk.CTkButton] = []

        # Setup UI
        self._build_ui(png_icon)
        self._center_window()
        self._update_target_time_display()

    def _center_window(self):
        """Centers window on the user's primary monitor."""
        self.update_idletasks()
        width = 440
        height = 620
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2) - 40
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self, icon_path: str):
        # Configure main background
        self.configure(fg_color=NatureTheme.BG_MAIN)

        # Header Frame
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=24, pady=(20, 12))

        # Leaf icon & title
        try:
            leaf_img = ctk.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),
                size=(28, 28)
            )
            icon_label = ctk.CTkLabel(header_frame, image=leaf_img, text="")
            icon_label.pack(side="left", padx=(0, 10))
        except Exception:
            pass

        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(side="left")

        title_lbl = ctk.CTkLabel(
            title_container,
            text="LeafTimer",
            font=ctk.CTkFont(family="Segoe UI Variable Display", size=20, weight="bold"),
            text_color=NatureTheme.TEXT_PRIMARY
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = ctk.CTkLabel(
            title_container,
            text="Peaceful PC Shutdown",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=12),
            text_color=NatureTheme.TEXT_MUTED
        )
        subtitle_lbl.pack(anchor="w")

        # Theme toggle button
        self.theme_btn = ctk.CTkButton(
            header_frame,
            text="🌙",
            width=36,
            height=36,
            corner_radius=18,
            fg_color=NatureTheme.PILL_BG,
            text_color=NatureTheme.PILL_TEXT,
            hover_color=NatureTheme.PILL_HOVER,
            font=ctk.CTkFont(size=14),
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="right")

        # Main Card
        self.card = ctk.CTkFrame(
            self,
            fg_color=NatureTheme.BG_CARD,
            corner_radius=20,
            border_width=1,
            border_color=NatureTheme.BORDER_COLOR
        )
        self.card.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        # 1. Countdown & Display Area
        display_frame = ctk.CTkFrame(self.card, fg_color=NatureTheme.BG_CARD_SECONDARY, corner_radius=16)
        display_frame.pack(fill="x", padx=16, pady=16)

        self.time_display_lbl = ctk.CTkLabel(
            display_frame,
            text="00:45:00",
            font=ctk.CTkFont(family="Segoe UI Variable Display", size=38, weight="bold"),
            text_color=NatureTheme.PRIMARY
        )
        self.time_display_lbl.pack(pady=(16, 2))

        self.target_time_lbl = ctk.CTkLabel(
            display_frame,
            text="PC will turn off at --:--",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=13),
            text_color=NatureTheme.TEXT_SECONDARY
        )
        self.target_time_lbl.pack(pady=(0, 12))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            display_frame,
            height=6,
            corner_radius=3,
            fg_color=NatureTheme.BORDER_COLOR,
            progress_color=NatureTheme.PRIMARY
        )
        self.progress_bar.set(0.0)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 16))

        # 2. Minutes Setting Section
        self.settings_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.settings_frame.pack(fill="x", padx=16, pady=(4, 8))

        setting_header = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        setting_header.pack(fill="x", pady=(0, 6))

        setting_title = ctk.CTkLabel(
            setting_header,
            text="Set Duration",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=14, weight="bold"),
            text_color=NatureTheme.TEXT_PRIMARY
        )
        setting_title.pack(side="left")

        self.duration_badge = ctk.CTkLabel(
            setting_header,
            text="45 min",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=13, weight="bold"),
            text_color=NatureTheme.PRIMARY,
            fg_color=NatureTheme.PILL_BG,
            corner_radius=8,
            padx=10,
            pady=2
        )
        self.duration_badge.pack(side="right")

        # Slider
        self.slider = ctk.CTkSlider(
            self.settings_frame,
            from_=1,
            to=180,
            number_of_steps=179,
            variable=self.selected_minutes,
            command=self._on_slider_change,
            button_color=NatureTheme.PRIMARY,
            button_hover_color=NatureTheme.PRIMARY_HOVER,
            progress_color=NatureTheme.PRIMARY
        )
        self.slider.pack(fill="x", pady=(6, 12))

        # Preset Buttons Grid
        presets_label = ctk.CTkLabel(
            self.settings_frame,
            text="Quick Presets",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=12),
            text_color=NatureTheme.TEXT_MUTED
        )
        presets_label.pack(anchor="w", pady=(0, 6))

        preset_grid = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        preset_grid.pack(fill="x", pady=(0, 8))

        # 2 rows of 3 presets
        for idx, mins in enumerate(self.presets):
            row = idx // 3
            col = idx % 3
            preset_text = f"{mins}m" if mins < 60 else f"{mins//60}h" if mins % 60 == 0 else f"{mins}m"
            
            btn = ctk.CTkButton(
                preset_grid,
                text=preset_text,
                height=32,
                corner_radius=10,
                fg_color=NatureTheme.PILL_BG,
                text_color=NatureTheme.PILL_TEXT,
                hover_color=NatureTheme.PILL_HOVER,
                font=ctk.CTkFont(family="Segoe UI Variable Text", size=12, weight="bold"),
                command=lambda m=mins: self._select_preset(m)
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
            preset_grid.grid_columnconfigure(col, weight=1)
            self.preset_buttons.append(btn)

        # Fine-tune +/- controls
        stepper_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        stepper_frame.pack(fill="x", pady=(4, 8))

        for text, delta in [("-15m", -15), ("-5m", -5), ("+5m", 5), ("+15m", 15)]:
            step_btn = ctk.CTkButton(
                stepper_frame,
                text=text,
                height=26,
                corner_radius=8,
                fg_color=NatureTheme.PILL_BG,
                text_color=NatureTheme.PILL_TEXT,
                hover_color=NatureTheme.PILL_HOVER,
                font=ctk.CTkFont(family="Segoe UI Variable Text", size=11),
                command=lambda d=delta: self._adjust_minutes(d)
            )
            step_btn.pack(side="left", expand=True, fill="x", padx=2)

        # 3. Action Mode Selector (Shutdown / Restart / Sleep)
        self.action_segment = ctk.CTkSegmentedButton(
            self.card,
            values=["Shutdown", "Restart", "Sleep"],
            command=self._on_action_change,
            selected_color=NatureTheme.PRIMARY,
            selected_hover_color=NatureTheme.PRIMARY_HOVER,
            corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=12, weight="bold")
        )
        self.action_segment.set("Shutdown")
        self.action_segment.pack(fill="x", padx=16, pady=(4, 16))

        # 4. Primary Action Button
        self.main_action_btn = ctk.CTkButton(
            self.card,
            text="🌿  Start Shutdown Timer",
            height=46,
            corner_radius=14,
            fg_color=NatureTheme.PRIMARY,
            hover_color=NatureTheme.PRIMARY_HOVER,
            text_color=NatureTheme.PRIMARY_TEXT,
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=15, weight="bold"),
            command=self._toggle_timer
        )
        self.main_action_btn.pack(fill="x", padx=16, pady=(0, 16))

        # Initial preset highlight
        self._highlight_active_preset(self.selected_minutes.get())

    def _adjust_minutes(self, delta: int):
        if self.timer_engine.is_running:
            return
        curr = self.selected_minutes.get()
        new_val = max(1, min(180, curr + delta))
        self.selected_minutes.set(new_val)
        self._on_slider_change(new_val)

    def _select_preset(self, minutes: int):
        if self.timer_engine.is_running:
            return
        self.selected_minutes.set(minutes)
        self._on_slider_change(minutes)

    def _highlight_active_preset(self, current_mins: int):
        for btn, mins in zip(self.preset_buttons, self.presets):
            if mins == current_mins:
                btn.configure(fg_color=NatureTheme.PILL_ACTIVE_BG, text_color=NatureTheme.PILL_ACTIVE_TEXT)
            else:
                btn.configure(fg_color=NatureTheme.PILL_BG, text_color=NatureTheme.PILL_TEXT)

    def _on_slider_change(self, value):
        mins = int(round(value))
        self.duration_badge.configure(text=f"{mins} min")
        self._highlight_active_preset(mins)
        if not self.timer_engine.is_running:
            hrs = mins // 60
            remaining_mins = mins % 60
            self.time_display_lbl.configure(text=f"{hrs:02d}:{remaining_mins:02d}:00")
            self._update_target_time_display(mins)

    def _on_action_change(self, value):
        mode_map = {
            "Shutdown": ShutdownTimerEngine.ACTION_SHUTDOWN,
            "Restart": ShutdownTimerEngine.ACTION_RESTART,
            "Sleep": ShutdownTimerEngine.ACTION_SLEEP
        }
        self.action_type.set(mode_map.get(value, ShutdownTimerEngine.ACTION_SHUTDOWN))
        if not self.timer_engine.is_running:
            self._update_target_time_display(self.selected_minutes.get())

    def _update_target_time_display(self, minutes: int = None):
        if minutes is None:
            minutes = self.selected_minutes.get()
        
        target = datetime.now() + timedelta(minutes=minutes)
        action_name = self.action_segment.get()
        self.target_time_lbl.configure(
            text=f"PC will {action_name.lower()} at {target.strftime('%H:%M:%S')}"
        )

    def _toggle_timer(self):
        if self.timer_engine.is_running:
            # Cancel timer
            self.timer_engine.cancel_timer()
        else:
            # Start timer
            mins = self.selected_minutes.get()
            action = self.action_type.get()
            self.timer_engine.start_timer(mins, action)
            self._set_ui_running_state(True)

    def _set_ui_running_state(self, running: bool):
        if running:
            self.slider.configure(state="disabled")
            self.action_segment.configure(state="disabled")
            for btn in self.preset_buttons:
                btn.configure(state="disabled")
            
            # Change action button to Cancel button
            self.main_action_btn.configure(
                text="✕  Cancel Shutdown",
                fg_color=NatureTheme.CANCEL,
                hover_color=NatureTheme.CANCEL_HOVER,
                text_color=NatureTheme.CANCEL_TEXT
            )
            self.time_display_lbl.configure(text_color=NatureTheme.CANCEL)
            self.progress_bar.configure(progress_color=NatureTheme.CANCEL)
        else:
            self.slider.configure(state="normal")
            self.action_segment.configure(state="normal")
            for btn in self.preset_buttons:
                btn.configure(state="normal")

            self.main_action_btn.configure(
                text=f"🌿  Start {self.action_segment.get()} Timer",
                fg_color=NatureTheme.PRIMARY,
                hover_color=NatureTheme.PRIMARY_HOVER,
                text_color=NatureTheme.PRIMARY_TEXT
            )
            self.time_display_lbl.configure(text_color=NatureTheme.PRIMARY)
            self.progress_bar.configure(progress_color=NatureTheme.PRIMARY)
            self.progress_bar.set(0.0)
            self._on_slider_change(self.selected_minutes.get())

    def _on_timer_tick(self, remaining_secs: int, progress: float, formatted: str):
        # Called on background thread -> safely schedule on main loop
        self.after(0, self._apply_tick_update, remaining_secs, progress, formatted)

    def _apply_tick_update(self, remaining_secs: int, progress: float, formatted: str):
        if not self.timer_engine.is_running:
            return
        self.time_display_lbl.configure(text=formatted)
        self.progress_bar.set(progress)
        if self.timer_engine.end_time:
            action_name = self.action_segment.get()
            self.target_time_lbl.configure(
                text=f"PC will {action_name.lower()} at {self.timer_engine.end_time.strftime('%H:%M:%S')}"
            )

    def _on_timer_finished(self):
        self.after(0, self._apply_finished)

    def _apply_finished(self):
        self.time_display_lbl.configure(text="00:00:00")
        self.target_time_lbl.configure(text="Action executing now...")
        self._set_ui_running_state(False)

    def _on_timer_cancelled(self):
        self.after(0, self._apply_cancelled)

    def _apply_cancelled(self):
        self._set_ui_running_state(False)
        self.target_time_lbl.configure(text="Shutdown cancelled. Ready.")

    def _toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            ctk.set_appearance_mode("Dark")
            self.theme_btn.configure(text="🌙")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_btn.configure(text="☀️")

if __name__ == "__main__":
    app = LeafTimerApp()
    app.mainloop()
