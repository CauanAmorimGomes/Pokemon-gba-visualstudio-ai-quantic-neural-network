import os
import subprocess
import time

import pyautogui


class Emulator:
    def __init__(self, window_delay=0.15):
        self.window_delay = window_delay
        self.mgba_path = None
        self.rom_path = None
        self.process = None

    def configure(self, mgba_path, rom_path):
        self.mgba_path = mgba_path
        self.rom_path = rom_path

        if not os.path.isfile(self.mgba_path):
            raise FileNotFoundError(
                f"mGBA não encontrado:\n{self.mgba_path}"
            )

        if not os.path.isfile(self.rom_path):
            raise FileNotFoundError(
                f"ROM não encontrada:\n{self.rom_path}"
            )

    def connect(self):
        if self.mgba_path is None or self.rom_path is None:
            raise RuntimeError(
                "Execute configure() antes de connect()."
            )

        if self.process is not None and self.process.poll() is None:
            return

        print("Abrindo mGBA...")
        self.process = subprocess.Popen(
            [self.mgba_path, self.rom_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(2.5)

        if self.process.poll() is not None:
            raise RuntimeError(
                "O mGBA foi iniciado, mas fechou imediatamente."
            )

        print("mGBA conectado.")
        self.focus_game()

    def focus_game(self):
        try:
            windows = pyautogui.getWindowsWithTitle("mGBA")
            if windows:
                win = windows[0]
                if win.isMinimized:
                    win.restore()
                win.activate()
                time.sleep(0.3)
            else:
                print(
                    "Aviso: janela do mGBA não encontrada. "
                    "Clique nela manualmente antes de continuar."
                )
        except Exception:
            print(
                "Aviso: não foi possível focar a janela automaticamente. "
                "Clique nela manualmente antes de continuar."
            )

    def press_key(self, key, duration=None):
        if duration is None:
            duration = self.window_delay

        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)

        time.sleep(0.05)

    def execute_action(self, action, duration=None):
        key_map = {
            "LEFT": "left",
            "RIGHT": "right",
            "UP": "up",
            "DOWN": "down",
            "A": "x"
        }

        if action not in key_map:
            raise ValueError(
                f"Ação inválida: {action}"
            )

        self.press_key(
            key_map[action],
            duration
        )

    def test_controls(self):
        print()
        print("================================")
        print("TESTE REAL DOS CONTROLES")
        print("================================")
        print()
        print("LEFT")
        self.execute_action("LEFT")

        print("RIGHT")
        self.execute_action("RIGHT")

        print("UP")
        self.execute_action("UP")

        print("DOWN")
        self.execute_action("DOWN")

        print("A -> X")
        self.execute_action("A")

        print()
        print("Teste dos controles concluído.")

    def wait(self, seconds):
        time.sleep(seconds)

    def close(self):
        if self.process is not None:
            if self.process.poll() is None:
                print("Fechando mGBA...")
                self.process.terminate()

                try:
                    self.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.process.kill()

            self.process = None