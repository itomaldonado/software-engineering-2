import click
import csv
import logging
import numpy as np

logger = logging.getLogger(__name__)

# Random ranges and seed
LOW = -1
HIGH = 1


class MNN:
    def __init__(self, input_layers=2, hidden_layers=2, output_layers=1):
        self.network = []
        self.input_size = input_layers
        self.hidden_size = hidden_layers
        self.output_size = output_layers

        # Create hidden layers first: (input x hidden) weight matrix from input to hidden layer
        self.hidden = (
            np.random.uniform(low=LOW, high=HIGH, size=(self.input_size, self.hidden_size)))

        # Create output layers: (hidden x output) weight matrix from hidden to output layer
        self.output = (
            np.random.uniform(low=LOW, high=HIGH, size=(self.hidden_size, self.output_size)))

    def activate(self, activation):
        return 1.0 / (1.0 + np.exp(-activation))

    def activate_derivative(self, activation):
        return activation * (1 - activation)

    def forward_propagate(self, training_inputs):

        # dot product of training_inputs and the hidden layers
        self.z = np.dot(training_inputs, self.hidden)

        # activation function of first putput
        self.z2 = self.activate(self.z)

        # dot product of hidden layers and output layers
        self.z3 = np.dot(self.z2, self.output)

        # final activation function last output
        return self.activate(self.z3)

    def backward_propagate_error(self, training_inputs, training_ouputs, outputs, learning_rate):
        """ backward propgate through the network"""

        # error in output
        self.outputs_error = training_ouputs - outputs

        # applying derivative of sigmoid to error
        self.outputs_delta = self.outputs_error * self.activate_derivative(outputs)

        # how much the hidden layers weights contributed to the output error
        self.z2_error = self.outputs_delta.dot(self.output.T)

        # applying activation derivative to z2 error
        self.z2_delta = self.z2_error*self.activate_derivative(self.z2)

        # updates weights for the hidden layers
        self.hidden += self.update_weights(
            training_inputs, self.hidden, self.z2_delta, learning_rate)

        # updates weights for the output layers
        self.output += self.update_weights(
            self.z2, self.output, self.outputs_delta, learning_rate)

    def update_weights(self, inputs, layer, delta, learning_rate):
        return inputs.T.dot(delta) * learning_rate

    def train_network(self, training_inputs, training_ouputs, learning_rate):
        o = self.forward_propagate(training_inputs)
        self.backward_propagate_error(training_inputs, training_ouputs, o, learning_rate)

    def predict(self, inputs):
        outputs = self.forward_propagate(inputs)
        return outputs


def setup_logging(debug):
    """ Setup server logging"""
    fmt = '%(message)s'
    loglevel = logging.INFO
    if debug:
        loglevel = logging.DEBUG
    logging.basicConfig(format=fmt, level=loglevel)


def load_csv_data(filename):
    """ Load CSV data from file"""
    data = list()
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:

            # ingore empty rows
            if not row:
                continue

            data.append(row)
    return data


@click.command()
@click.option(
    '--debug', is_flag=True, help="Show debug data")
@click.option(
    '--hidden', default=2, help='Number of hidden layers', type=int, show_default=True)
@click.option(
    '--error', '-e', default=0.02, help='Target error', type=float, show_default=True)
@click.option(
    '--learning-rate', '-l', default=0.5, help='Learning rate', type=float, show_default=True)
@click.option(
    '--epochs', '-r', default=10000,
    help='Max number of epochs for learning', type=int, show_default=True)
@click.argument('training_data', type=click.Path(exists=True))
def run_mnn_xor(
        debug,
        hidden,
        learning_rate,
        error,
        epochs,
        training_data):
    """ Run MNN with the provided test data and inputs/outputs """

    # setup logging
    setup_logging(debug)

    # read input data row format:
    # input_1, input2, expected_putput
    #     int,    int,             int
    data = load_csv_data(training_data)
    data = np.array(data, dtype=float)
    input_data = data[:, [0, 1]]
    output_data = data[:, [2]]
    mnn = MNN(input_layers=2, hidden_layers=hidden, output_layers=1)
    logger.info(f'----------- Start -----------')
    logger.info(f'Initial layer weights')
    logger.info(f'Hidden Layers: \n{mnn.hidden}')
    logger.info(f'Output Layers: \n{mnn.output}')
    logger.info(f'-----------------------------')

    # while we have reached the target error or max epochs
    it = 0
    first_error = 0
    calculated_error = error + 1
    while (calculated_error > error) and (it < epochs):
        logger.debug(f'Input: \n{str(input_data)}')
        logger.debug(f'Actual Output: \n{str(output_data)}')

        # test network
        o = mnn.forward_propagate(input_data)
        logger.debug(f'Predicted Output: \n{str(o)}')

        # calculate mean sum squared error
        calculated_error = np.mean(np.square(output_data - o))
        logger.debug(f'Error for epoch {it}: {str(calculated_error)}')

        # keep the first error around
        if it == 0:
            first_error = calculated_error

        # re-train network
        mnn.train_network(input_data, output_data, learning_rate)

        # increase current iteration number
        it += 1

    # print stats
    logger.info('')
    logger.info(f'--------- Results -----------')
    logger.info(f'First batch error: {first_error}')
    logger.info(f'Last batch error: {calculated_error}')
    logger.info(f'Total number of batches: {it}')
    logger.info(f'Final layer weights')
    logger.info(f'Hidden Layers: \n{mnn.hidden}')
    logger.info(f'Output Layers: \n{mnn.output}')
    logger.info(f'-----------------------------')


if __name__ == '__main__':
    run_mnn_xor()
