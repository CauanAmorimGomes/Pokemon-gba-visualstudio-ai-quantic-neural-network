import random

from neural_network import NeuralNetwork


POPULATION_SIZE = 200
GENERATIONS = 2000
SURVIVORS = 20

MUTATION_RATE = 0.10
MUTATION_STRENGTH = 0.25

INPUT_SIZE = 6
HIDDEN_SIZE = 12
OUTPUT_SIZE = 5

INITIAL_A_COUNT = 4
ADDITIONAL_A_COUNT = 114


ACTIONS = [
    "LEFT",
    "RIGHT",
    "UP",
    "DOWN",
    "A"
]


PC_KEY = {
    "LEFT": "LEFT",
    "RIGHT": "RIGHT",
    "UP": "UP",
    "DOWN": "DOWN",
    "A": "X"
}


def create_target_sequence():

    sequence = []

    for _ in range(INITIAL_A_COUNT):
        sequence.append(4)

    for _ in range(ADDITIONAL_A_COUNT):
        sequence.append(4)

    for _ in range(5):
        sequence.append(0)

    for _ in range(2):
        sequence.append(2)

    for _ in range(5):
        sequence.append(0)

    for _ in range(2):
        sequence.append(2)

    for _ in range(12):
        sequence.append(4)

    for _ in range(2):
        sequence.append(3)

    for _ in range(2):
        sequence.append(3)

    sequence.append(4)

    for _ in range(5):
        sequence.append(1)

    for _ in range(3):
        sequence.append(3)

    for _ in range(4):
        sequence.append(1)

    for _ in range(3):
        sequence.append(2)

    sequence.append(0)

    for _ in range(5):
        sequence.append(3)

    for _ in range(5):
        sequence.append(0)

    for _ in range(4):
        sequence.append(3)

    for _ in range(5):
        sequence.append(1)

    for _ in range(6):
        sequence.append(2)

    for _ in range(60):
        sequence.append(4)

    return sequence


TARGET_SEQUENCE = create_target_sequence()


def evaluate(network):

    correct = 0
    errors = 0

    total_steps = len(TARGET_SEQUENCE)

    for step, expected in enumerate(
        TARGET_SEQUENCE
    ):

        prediction = network.predict(
            step,
            total_steps
        )

        if prediction == expected:
            correct += 1
        else:
            errors += 1

    fitness = (
        correct * 100
        - errors * 50
    )

    return fitness, correct, errors


def create_population():

    return [
        NeuralNetwork(
            INPUT_SIZE,
            HIDDEN_SIZE,
            OUTPUT_SIZE
        )
        for _ in range(POPULATION_SIZE)
    ]


def evolve():

    population = create_population()

    best_network = None
    best_fitness = float("-inf")

    for generation in range(GENERATIONS):

        results = []

        for neural_network in population:

            fitness, correct, errors = (
                evaluate(neural_network)
            )

            results.append(
                (
                    fitness,
                    correct,
                    errors,
                    neural_network
                )
            )

        results.sort(
            key=lambda item: item[0],
            reverse=True
        )

        generation_best = results[0]

        generation_fitness = (
            generation_best[0]
        )

        generation_correct = (
            generation_best[1]
        )

        generation_errors = (
            generation_best[2]
        )

        generation_network = (
            generation_best[3]
        )

        if generation_fitness > best_fitness:

            best_fitness = generation_fitness
            best_network = generation_network

        if generation % 10 == 0:

            print(
                f"Geração {generation:4d} | "
                f"Acertos: "
                f"{generation_correct}/"
                f"{len(TARGET_SEQUENCE)} | "
                f"Erros: "
                f"{generation_errors:3d} | "
                f"Fitness: "
                f"{generation_fitness:8.0f}"
            )

        if generation_correct == len(
            TARGET_SEQUENCE
        ):

            print()
            print("================================")
            print("OBJETIVO ALCANÇADO")
            print("================================")

            print(
                f"Geração: {generation}"
            )

            print(
                f"Acertos: "
                f"{generation_correct}/"
                f"{len(TARGET_SEQUENCE)}"
            )

            print("Erros: 0")

            return generation_network

        survivors = [
            item[3]
            for item in results[:SURVIVORS]
        ]

        new_population = []

        for _ in range(POPULATION_SIZE):

            parent = random.choice(
                survivors
            )

            child = parent.mutate(
                MUTATION_RATE,
                MUTATION_STRENGTH
            )

            new_population.append(child)

        population = new_population

    print()
    print("================================")
    print(
        f"{GENERATIONS} GERAÇÕES FINALIZADAS"
    )
    print("================================")

    return best_network


def test_network(neural_network):

    print()
    print("TESTE FINAL")
    print("================================")

    errors = 0

    total_steps = len(TARGET_SEQUENCE)

    for step, expected in enumerate(
        TARGET_SEQUENCE
    ):

        prediction = (
            neural_network.predict(
                step,
                total_steps
            )
        )

        expected_action = (
            ACTIONS[expected]
        )

        predicted_action = (
            ACTIONS[prediction]
        )

        predicted_key = PC_KEY[
            predicted_action
        ]

        if prediction == expected:

            print(
                f"{step + 1:03d}/"
                f"{len(TARGET_SEQUENCE)} | "
                f"{predicted_action:5s} | "
                f"Tecla PC: "
                f"{predicted_key} | ✓"
            )

        else:

            print(
                f"{step + 1:03d}/"
                f"{len(TARGET_SEQUENCE)} | "
                f"{predicted_action:5s} | "
                f"Tecla PC: "
                f"{predicted_key} | "
                f"ERRO - esperado "
                f"{expected_action}"
            )

            errors += 1

    print()
    print("================================")
    print("RESULTADO")
    print("================================")

    print(
        f"Ações corretas: "
        f"{len(TARGET_SEQUENCE) - errors}/"
        f"{len(TARGET_SEQUENCE)}"
    )

    print(
        f"Erros: {errors}"
    )

    if errors == 0:

        print()
        print("PERFEITO!")

        print(
            "A rede executou todas "
            "as ações sem erros."
        )


def show_target_sequence():

    print()
    print("SEQUÊNCIA DE TREINAMENTO")
    print("================================")

    for index, action_index in enumerate(
        TARGET_SEQUENCE
    ):

        action = ACTIONS[action_index]

        key = PC_KEY[action]

        print(
            f"{index + 1:03d}/"
            f"{len(TARGET_SEQUENCE)} | "
            f"{action:5s} | "
            f"PC: {key}"
        )


def show_network_structure(
    neural_network
):

    print()
    print("ESTRUTURA DA REDE")
    print("================================")

    print(
        f"Entradas: {INPUT_SIZE}"
    )

    print(
        f"Neurônios ocultos: "
        f"{HIDDEN_SIZE}"
    )

    print(
        f"Saídas: {OUTPUT_SIZE}"
    )

    print()

    print("ENTRADA → OCULTA")

    for index, weights in enumerate(
        neural_network.input_hidden
    ):

        print(
            f"Neurônio oculto "
            f"{index + 1:02d} -> "
            f"{[round(value, 6) for value in weights]} "
            f"| Bias: "
            f"{round(neural_network.hidden_bias[index], 6)}"
        )

    print()

    print("OCULTA → SAÍDA")

    for index, weights in enumerate(
        neural_network.hidden_output
    ):

        action = ACTIONS[index]

        print(
            f"{action:5s} -> "
            f"{[round(value, 6) for value in weights]} "
            f"| Bias: "
            f"{round(neural_network.output_bias[index], 6)}"
        )


def main():

    print("================================")
    print("REDE NEURAL EVOLUTIVA")
    print("================================")

    print()

    print(
        f"População: "
        f"{POPULATION_SIZE}"
    )

    print(
        f"Gerações: "
        f"{GENERATIONS}"
    )

    print(
        f"Sobreviventes: "
        f"{SURVIVORS}"
    )

    print(
        f"Entradas: "
        f"{INPUT_SIZE}"
    )

    print(
        f"Neurônios ocultos: "
        f"{HIDDEN_SIZE}"
    )

    print(
        f"Saídas: "
        f"{OUTPUT_SIZE}"
    )

    print(
        f"Ações totais: "
        f"{len(TARGET_SEQUENCE)}"
    )

    print()

    print("Ações disponíveis:")

    print("LEFT  -> LEFT")
    print("RIGHT -> RIGHT")
    print("UP    -> UP")
    print("DOWN  -> DOWN")
    print("A     -> X")

    print()

    show_target_sequence()

    print()
    print("INICIANDO EVOLUÇÃO...")
    print()

    neural_network = evolve()

    if neural_network is None:

        print(
            "Nenhuma rede neural foi criada."
        )

        return

    show_network_structure(
        neural_network
    )

    test_network(
        neural_network
    )


if __name__ == "__main__":
    main()