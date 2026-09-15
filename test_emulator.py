from emulator import Emulator


emulator = Emulator(
    window_delay=0.15
)


emulator.configure(
    r"C:\Program Files\mGBA\mGBA.exe",
    r"C:\Users\User\Downloads\Pokemon - Fire Red Version [a1] (U) (Squirrels) (1)\1636 - Pokemon Fire Red (U)(Squirrels).gba"
)


try:

    emulator.connect()

    input(
        "Pressione ENTER para testar os controles..."
    )

    emulator.test_controls()

    input(
        "Pressione ENTER para fechar..."
    )

finally:

    emulator.close()