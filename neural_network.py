import math
import random


class NeuralNetwork:

    def __init__(self, input_size, hidden_size, output_size):

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.input_hidden = [
            [
                random.uniform(-1.0, 1.0)
                for _ in range(input_size)
            ]
            for _ in range(hidden_size)
        ]

        self.hidden_output = [
            [
                random.uniform(-1.0, 1.0)
                for _ in range(hidden_size)
            ]
            for _ in range(output_size)
        ]

        self.hidden_bias = [
            random.uniform(-1.0, 1.0)
            for _ in range(hidden_size)
        ]

        self.output_bias = [
            random.uniform(-1.0, 1.0)
            for _ in range(output_size)
        ]

    def activation(self, value):

        return math.tanh(value)

    def predict(self, step, total_steps):

        normalized_step = (
            step / max(1, total_steps - 1)
        )

        progress_remaining = (
            1.0 - normalized_step
        )

        inputs = [
            normalized_step,
            progress_remaining,
            math.sin(
                normalized_step * math.pi
            ),
            math.cos(
                normalized_step * math.pi
            ),
            normalized_step * normalized_step,
            math.sqrt(normalized_step)
        ]

        hidden_values = []

        for neuron in range(self.hidden_size):

            value = self.hidden_bias[neuron]

            for i in range(self.input_size):

                value += (
                    self.input_hidden[neuron][i]
                    * inputs[i]
                )

            hidden_values.append(
                self.activation(value)
            )

        output_values = []

        for output in range(self.output_size):

            value = self.output_bias[output]

            for neuron in range(self.hidden_size):

                value += (
                    self.hidden_output[output][neuron]
                    * hidden_values[neuron]
                )

            output_values.append(value)

        return output_values.index(
            max(output_values)
        )

    def clone(self):

        child = NeuralNetwork(
            self.input_size,
            self.hidden_size,
            self.output_size
        )

        child.input_hidden = [
            row.copy()
            for row in self.input_hidden
        ]

        child.hidden_output = [
            row.copy()
            for row in self.hidden_output
        ]

        child.hidden_bias = self.hidden_bias.copy()
        child.output_bias = self.output_bias.copy()

        return child

    def mutate(self, mutation_rate, mutation_strength):

        child = self.clone()

        for i in range(self.hidden_size):

            for j in range(self.input_size):

                if random.random() < mutation_rate:

                    child.input_hidden[i][j] += (
                        random.gauss(
                            0,
                            mutation_strength
                        )
                    )

        for i in range(self.output_size):

            for j in range(self.hidden_size):

                if random.random() < mutation_rate:

                    child.hidden_output[i][j] += (
                        random.gauss(
                            0,
                            mutation_strength
                        )
                    )

        for i in range(self.hidden_size):

            if random.random() < mutation_rate:

                child.hidden_bias[i] += (
                    random.gauss(
                        0,
                        mutation_strength
                    )
                )

        for i in range(self.output_size):

            if random.random() < mutation_rate:

                child.output_bias[i] += (
                    random.gauss(
                        0,
                        mutation_strength
                    )
                )

        return child