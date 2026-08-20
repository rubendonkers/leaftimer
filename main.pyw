"""
Windowless entry point for LeafTimer on Windows.
"""

from app import LeafTimerApp

if __name__ == "__main__":
    app = LeafTimerApp()
    app.mainloop()
