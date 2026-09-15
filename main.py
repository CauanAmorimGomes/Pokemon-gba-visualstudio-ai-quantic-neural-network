from emulator import Emulator

MGBA_PATH = r"C:\Program Files\mGBA\mGBA.exe"

ROM_PATH = (
    r"C:\Users\User\Downloads"
    r"\Pokemon - Fire Red Version [a1] (U) (Squirrels) (1)"
    r"\1636 - Pokemon Fire Red (U)(Squirrels).gba"
)

TOTAL_X = 140
X_ANTES_DO_DOWN = 110
QUANTIDADE_DOWN = 2

TOQUE_CURTO = 0.15


def build_initial_sequence():

    sequence = []

    for _ in range(X_ANTES_DO_DOWN):
        sequence.append(("A", TOQUE_CURTO))

    for _ in range(QUANTIDADE_DOWN):
        sequence.append(("DOWN", TOQUE_CURTO))

    x_restantes = TOTAL_X - X_ANTES_DO_DOWN

    for _ in range(x_restantes):
        sequence.append(("A", TOQUE_CURTO))

    return sequence


def build_navigation_sequence():

    sequence = []

    sequence.append(("LEFT", 6))
    sequence.append(("UP", 3))
    sequence.append(("LEFT", 3))
    sequence.append(("UP", 2))

    for _ in range(8):
        sequence.append(("A", TOQUE_CURTO))

    for _ in range(2):
        sequence.append(("DOWN", TOQUE_CURTO))

    sequence.append(("A", TOQUE_CURTO))

    for _ in range(2):
        sequence.append(("DOWN", TOQUE_CURTO))

    sequence.append(("A", TOQUE_CURTO))

    sequence.append(("RIGHT", 7))
    sequence.append(("DOWN", 4))
    sequence.append(("RIGHT", 5))
    sequence.append(("UP", 3))
    sequence.append(("LEFT", 3))
    sequence.append(("DOWN", 8))
    sequence.append(("LEFT", 6))

    return sequence


ACTION_SEQUENCE = (
    build_initial_sequence()
    + build_navigation_sequence()
)


def format_label(action, duration):

    tecla_exibida = (
        "X" if action == "A" else action
    )

    if duration == TOQUE_CURTO:
        return tecla_exibida

    return f"{tecla_exibida} ({duration}s)"


def main():

    total_comandos = len(ACTION_SEQUENCE)

    print("================================")
    print("POKEMON FIRE RED - SEQUÊNCIA")
    print("================================")
    print()

    print("mGBA:")
    print(MGBA_PATH)
    print()

    print("ROM:")
    print(ROM_PATH)
    print()

    print(
        f"Total de comandos: {total_comandos}"
    )
    print()

    emulator = Emulator(
        window_delay=0.15
    )

    emulator.configure(
        MGBA_PATH,
        ROM_PATH
    )

    try:

        emulator.connect()

        print()
        print("O mGBA foi aberto.")
        print("Deixe o FireRed visível.")
        print()

        input(
            f"Pressione ENTER para enviar os {total_comandos} comandos..."
        )

        print()
        print("Enviando comandos...")
        print("================================")

        for i, (action, duration) in enumerate(
            ACTION_SEQUENCE
        ):

            print(
                f"{i + 1:03d}/{total_comandos} | "
                f"{format_label(action, duration)}"
            )

            emulator.execute_action(
                action,
                duration=duration
            )

            emulator.wait(
                0.05
            )

        print()
        print("================================")
        print(f"{total_comandos} COMANDOS ENVIADOS")
        print("================================")
        print()

        input(
            "Pressione ENTER para fechar o mGBA..."
        )

    except KeyboardInterrupt:

        print()
        print("Execução interrompida pelo usuário.")

    finally:

        emulator.close()


if __name__ == "__main__":
    main()