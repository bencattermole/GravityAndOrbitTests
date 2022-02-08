import math
import random

#binary weights:

all_possible_weights = [[-1,-1,-1],
                        [-1,-1,1],
                        [-1,1,-1],
                        [-1,1,1],
                        [1,-1,-1],
                        [1,-1,1],
                        [1,1,-1],
                        [1,1,1]]


class Neuron:
    def __init__(self, num_of_inputs):
        self.weights = self.gen_rand_weights(num_of_inputs)
        self.learning_constant = 0.1

    @staticmethod
    def gen_rand_weights(n_to_gen):
        list_of_val = []
        for n in range(n_to_gen):
            list_of_val.append(random.uniform(-1, 1))

        return list_of_val

    @staticmethod
    def activate(val):
        if val > 0:
            return 1
        else:
            return -1

    def feed_forward(self, inputs):

        sum = 0

        for i in range(len(inputs)):
            sum += inputs[i] * self.weights[i]

        return self.activate(sum)

    def train(self, inputs_had, desired):
        guess = self.feed_forward(inputs_had)
        error = desired - guess
        for weight in range(len(self.weights)):
            self.weights[weight] += self.learning_constant * error * inputs_had[weight]


class Predictor:
    def __init__(self, num_of_inputs):
        self.weights = self.gen_rand_weights(num_of_inputs)
        self.learning_constant = 0.1

    @staticmethod
    def gen_rand_weights(n_to_gen):
        list_of_val = []
        for n in range(n_to_gen):
            list_of_val.append(random.uniform(-100, 100))

        return list_of_val

    def feed_forward(self, inputs):

        sum = 0

        for i in range(len(inputs)):
            sum += inputs[i] * self.weights[i]

        return sum

    def train(self, inputs_had, desired):
        guess = self.feed_forward(inputs_had)
        error = desired - guess
        for weight in range(len(self.weights)):
            self.weights[weight] += self.learning_constant * error * inputs_had[weight]


class Network:
    def __init__(self, list_of_neurons, predictor):
        self.neurons = list_of_neurons
        self.predictor = predictor
        self.current_prediction = 0
        self.last_four_pulses = []

    # gonna write this out without any fancyness for simplicity
    def alert_pulse(self, pulse_x):
        if len(self.last_four_pulses) < 3:
            self.last_four_pulses.append(pulse_x)
        elif len(self.last_four_pulses) == 3:
            self.last_four_pulses.append(pulse_x)
            predict = self.input_to_network(self.last_four_pulses)
            self.current_prediction = predict
        else:
            self.last_four_pulses.pop(0)
            self.last_four_pulses.append(pulse_x)
            self.error_correction(pulse_x)
            predict = self.input_to_network(self.last_four_pulses)
            self.current_prediction = predict

    def input_to_network(self, input_data):
        n_one = self.neurons[0].feed_forward([input_data[0], input_data[1]])
        n_two = self.neurons[1].feed_forward([input_data[1], input_data[2]])
        n_three = self.neurons[2].feed_forward([input_data[2], input_data[3]])

        out_to_predict = [n_one, n_two, n_three]

        prediction_for_next_pulse = self.predictor.feed_forward(out_to_predict)
        return prediction_for_next_pulse

    def error_correction(self, x_val_new):
        new_data = x_val_new - self.last_four_pulses[-2]
        n_one = self.neurons[0].feed_forward([self.last_four_pulses[0], self.last_four_pulses[1]])
        n_two = self.neurons[1].feed_forward([self.last_four_pulses[1], self.last_four_pulses[2]])
        n_three = self.neurons[2].feed_forward([self.last_four_pulses[2], self.last_four_pulses[3]])

        out_to_predict = [n_one, n_two, n_three]

        what_was_predict_for_pulse = self.predictor.feed_forward(out_to_predict)

        weights_from_predictor = []

        for weight in self.predictor.weights:
            weights_from_predictor.append(weight)

        # find best combo for one, two and three
        current_best = new_data - what_was_predict_for_pulse
        combo_num = 0
        count = 0
        for combo in all_possible_weights:
            what_would_be_predict = weights_from_predictor[0]*combo[0] + weights_from_predictor[1]*combo[1] + weights_from_predictor[2]*combo[2]
            if abs(current_best) > (new_data - what_would_be_predict):
                current_best = new_data - what_would_be_predict
                combo_num = count
            else:
                pass

            count += 1

        had_the_best = False
        if current_best == (new_data - what_was_predict_for_pulse):
            had_the_best = True
        else:
            self.neurons[0].train([self.last_four_pulses[0], self.last_four_pulses[1]], all_possible_weights[combo_num][0])
            self.neurons[1].train([self.last_four_pulses[1], self.last_four_pulses[2]], all_possible_weights[combo_num][1])
            self.neurons[2].train([self.last_four_pulses[2], self.last_four_pulses[3]], all_possible_weights[combo_num][2])

        if had_the_best:
            self.predictor.train(out_to_predict, new_data)
        else:
            self.predictor.train(all_possible_weights[combo_num], new_data)