"""
Keyboard input injection using pynput
"""
from pynput.keyboard import Controller, Key
import time


class InputInjector:
    def __init__(self, delay=0.01):
        """
        Initialize input injector

        Args:
            delay: Delay between keystrokes (seconds)
        """
        self.keyboard = Controller()
        self.delay = delay

    def type_text(self, text):
        """
        Type text into the active window

        Args:
            text: Text to type
        """
        if not text:
            return

        print(f"⌨️  Typing: {text}")

        # Small delay to ensure focus is correct
        time.sleep(0.1)

        # Type each character
        for char in text:
            self.keyboard.type(char)
            time.sleep(self.delay)

    def press_key(self, key):
        """
        Press a special key

        Args:
            key: Key to press (use pynput.keyboard.Key constants)
        """
        self.keyboard.press(key)
        self.keyboard.release(key)

    def execute_command(self, command_type, *args):
        """
        Execute terminal navigation commands

        Args:
            command_type: Type of command (e.g., "move_left", "move_right", "delete", "enter")
            args: Command arguments
        """
        if command_type == "move_left":
            count = args[0] if args else 1
            for _ in range(count):
                self.press_key(Key.left)
                time.sleep(0.05)

        elif command_type == "move_right":
            count = args[0] if args else 1
            for _ in range(count):
                self.press_key(Key.right)
                time.sleep(0.05)

        elif command_type == "move_to_start":
            # Ctrl+A moves to start of line in terminals (bash/zsh)
            self.keyboard.press(Key.ctrl)
            self.keyboard.press('a')
            self.keyboard.release('a')
            self.keyboard.release(Key.ctrl)

        elif command_type == "move_to_end":
            # Ctrl+E moves to end of line in terminals (bash/zsh)
            self.keyboard.press(Key.ctrl)
            self.keyboard.press('e')
            self.keyboard.release('e')
            self.keyboard.release(Key.ctrl)

        elif command_type == "delete_word":
            # Option+Delete on macOS deletes word
            self.keyboard.press(Key.alt)
            self.press_key(Key.backspace)
            self.keyboard.release(Key.alt)

        elif command_type == "delete_char":
            count = args[0] if args else 1
            for _ in range(count):
                self.press_key(Key.backspace)
                time.sleep(0.05)

        elif command_type == "delete_line":
            # Ctrl+U deletes to start of line in terminals (bash/zsh)
            self.keyboard.press(Key.ctrl)
            self.keyboard.press('u')
            self.keyboard.release('u')
            self.keyboard.release(Key.ctrl)

        elif command_type == "enter":
            self.press_key(Key.enter)

        elif command_type == "tab":
            self.press_key(Key.tab)

        elif command_type == "shift_tab":
            # Shift+Tab for switching modes (edit <-> plan)
            self.keyboard.press(Key.shift)
            self.press_key(Key.tab)
            self.keyboard.release(Key.shift)

        elif command_type == "escape":
            self.press_key(Key.esc)

        else:
            print(f"⚠️  Unknown command: {command_type}")

    def _is_mac(self):
        """Check if running on macOS"""
        import platform
        return platform.system() == "Darwin"


# Test the input injector
if __name__ == "__main__":
    import sys

    print("\n" + "="*60)
    print("Input Injector Test")
    print("="*60 + "\n")
    print("⚠️  This will type text into your active window!")
    print("You have 3 seconds to focus your terminal...\n")

    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)

    print("\n🚀 Starting test...\n")

    injector = InputInjector()

    # Test 1: Type simple text
    print("Test 1: Typing text")
    injector.type_text("Hello from voice dictation!")
    time.sleep(1)

    # Test 2: Navigation
    print("\nTest 2: Navigation commands")
    injector.execute_command("move_to_start")
    time.sleep(0.5)
    injector.execute_command("move_right", 6)
    time.sleep(0.5)

    # Test 3: Delete word
    print("\nTest 3: Delete commands")
    injector.execute_command("delete_word")
    time.sleep(0.5)

    # Test 4: Move to end and add text
    print("\nTest 4: Move to end and add text")
    injector.execute_command("move_to_end")
    injector.type_text(" - Testing complete!")
    time.sleep(0.5)

    # Test 5: Press Enter
    print("\nTest 5: Press Enter")
    injector.execute_command("enter")

    print("\n✅ Test complete!\n")
