"""
Modern overlay UI for voice dictation - circular pulsing indicator
"""
import tkinter as tk
from tkinter import Canvas
import math
import threading


class VoiceOverlay:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.state = "idle"  # idle, listening, processing
        self.animation_running = False
        self.pulse_angle = 0

    def show(self):
        """Show the overlay window"""
        if self.root is None:
            self._create_window()
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)

    def hide(self):
        """Hide the overlay window"""
        if self.root:
            self.root.withdraw()

    def set_state(self, state):
        """Set the state: idle, listening, processing"""
        self.state = state
        if state == "listening":
            self.start_animation()
        else:
            self.stop_animation()
        self._redraw()

    def _create_window(self):
        """Create the overlay window"""
        self.root = tk.Tk()
        self.root.title("Voice Dictation")

        # Make window transparent and always on top
        self.root.attributes('-alpha', 0.9)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)  # Remove window decorations

        # Set window size and position (bottom right corner)
        size = 120
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - size - 40
        y = screen_height - size - 100

        self.root.geometry(f'{size}x{size}+{x}+{y}')
        self.root.configure(bg='#000000')

        # Create canvas
        self.canvas = Canvas(
            self.root,
            width=size,
            height=size,
            bg='#000000',
            highlightthickness=0
        )
        self.canvas.pack()

        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

        # Initial draw
        self._redraw()

        # Start in hidden state
        self.root.withdraw()

    def start_animation(self):
        """Start the pulsing animation"""
        if not self.animation_running:
            self.animation_running = True
            self._animate()

    def stop_animation(self):
        """Stop the pulsing animation"""
        self.animation_running = False

    def _animate(self):
        """Animate the pulsing effect"""
        if not self.animation_running or self.state != "listening":
            return

        self.pulse_angle = (self.pulse_angle + 10) % 360
        self._redraw()

        if self.root:
            self.root.after(50, self._animate)

    def _redraw(self):
        """Redraw the overlay based on current state"""
        if not self.canvas:
            return

        self.canvas.delete("all")
        size = 120
        center = size // 2

        if self.state == "idle":
            # Gray circle
            self._draw_circle(center, center, 35, fill='#404040', outline='#666666', width=2)
            self._draw_text(center, center, "💤", size=24)

        elif self.state == "listening":
            # Pulsing blue circle
            pulse = abs(math.sin(math.radians(self.pulse_angle)))
            radius = 35 + pulse * 8
            alpha_val = int(150 + pulse * 105)
            color = f'#{alpha_val:02x}00ff'

            self._draw_circle(center, center, radius, fill='#0066ff', outline=color, width=3)
            self._draw_text(center, center, "🎤", size=32)

        elif self.state == "processing":
            # Purple spinning circle
            self._draw_circle(center, center, 35, fill='#8800ff', outline='#aa44ff', width=2)
            self._draw_text(center, center, "⚙️", size=28)

    def _draw_circle(self, x, y, radius, **kwargs):
        """Draw a circle on the canvas"""
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            **kwargs
        )

    def _draw_text(self, x, y, text, size=24):
        """Draw text on the canvas"""
        self.canvas.create_text(
            x, y,
            text=text,
            fill='white',
            font=('Arial', size)
        )

    def run(self):
        """Run the tkinter main loop (blocking)"""
        if self.root:
            self.root.mainloop()


# Test the overlay
if __name__ == "__main__":
    import time

    overlay = VoiceOverlay()

    def test_states():
        time.sleep(1)
        overlay.show()
        overlay.set_state("idle")

        time.sleep(2)
        overlay.set_state("listening")

        time.sleep(3)
        overlay.set_state("processing")

        time.sleep(2)
        overlay.hide()

    threading.Thread(target=test_states, daemon=True).start()
    overlay.run()
