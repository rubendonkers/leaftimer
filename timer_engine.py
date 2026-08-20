"""
Timer engine handling Windows shutdown execution, precise countdowns, and OS hooks.
"""

import os
import time
import subprocess
import threading
from datetime import datetime, timedelta
from typing import Callable, Optional

class ShutdownTimerEngine:
    ACTION_SHUTDOWN = "shutdown"
    ACTION_RESTART = "restart"
    ACTION_SLEEP = "sleep"

    def __init__(self):
        self._is_running = False
        self._total_seconds = 0
        self._remaining_seconds = 0
        self._end_time: Optional[datetime] = None
        self._timer_thread: Optional[threading.Thread] = None
        self._action_mode = self.ACTION_SHUTDOWN
        
        # Callbacks
        self.on_tick: Optional[Callable[[int, float, str], None]] = None  # (remaining_secs, progress_pct, formatted_time)
        self.on_finished: Optional[Callable[[], None]] = None
        self.on_cancelled: Optional[Callable[[], None]] = None

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def remaining_seconds(self) -> int:
        return self._remaining_seconds

    @property
    def total_seconds(self) -> int:
        return self._total_seconds

    @property
    def end_time(self) -> Optional[datetime]:
        return self._end_time

    def format_time(self, seconds: int) -> str:
        """Formats seconds into HH:MM:SS or MM:SS."""
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        if hrs > 0:
            return f"{hrs:02d}:{mins:02d}:{secs:02d}"
        return f"{mins:02d}:{secs:02d}"

    def start_timer(self, minutes: float, action: str = ACTION_SHUTDOWN) -> None:
        """Starts the countdown timer for the specified minutes."""
        if self._is_running:
            self.cancel_timer()

        self._action_mode = action
        self._total_seconds = int(max(1, round(minutes * 60)))
        self._remaining_seconds = self._total_seconds
        self._end_time = datetime.now() + timedelta(seconds=self._total_seconds)
        self._is_running = True

        self._timer_thread = threading.Thread(target=self._run_loop, daemon=True)
        self._timer_thread.start()

    def cancel_timer(self) -> None:
        """Stops the active timer and cancels any pending OS shutdown."""
        if not self._is_running and not self._timer_thread:
            # Still attempt OS abort just in case
            self._abort_os_shutdown()
            return

        self._is_running = False
        self._abort_os_shutdown()

        if self.on_cancelled:
            self.on_cancelled()

    def _run_loop(self) -> None:
        """Internal countdown loop running on a background thread."""
        while self._is_running and self._remaining_seconds > 0:
            # Calculate actual remaining based on wall clock to avoid drift
            now = datetime.now()
            if self._end_time:
                remaining = int((self._end_time - now).total_seconds())
                self._remaining_seconds = max(0, remaining)
            else:
                self._remaining_seconds -= 1

            progress = 1.0 - (self._remaining_seconds / self._total_seconds if self._total_seconds > 0 else 0)
            formatted = self.format_time(self._remaining_seconds)

            if self.on_tick:
                self.on_tick(self._remaining_seconds, progress, formatted)

            if self._remaining_seconds <= 0:
                break

            time.sleep(0.5)

        if self._is_running and self._remaining_seconds <= 0:
            self._is_running = False
            if self.on_finished:
                self.on_finished()
            self._execute_action()

    def _execute_action(self) -> None:
        """Executes the selected action on Windows."""
        try:
            if self._action_mode == self.ACTION_SHUTDOWN:
                # Initiate Windows shutdown with 0 second delay
                subprocess.run(
                    ["shutdown", "/s", "/t", "0", "/f"],
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                )
            elif self._action_mode == self.ACTION_RESTART:
                subprocess.run(
                    ["shutdown", "/r", "/t", "0", "/f"],
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                )
            elif self._action_mode == self.ACTION_SLEEP:
                subprocess.run(
                    ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                )
        except Exception as e:
            print(f"Error executing action: {e}")

    def _abort_os_shutdown(self) -> None:
        """Aborts any scheduled Windows shutdown command."""
        try:
            subprocess.run(
                ["shutdown", "/a"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
        except Exception:
            pass
