# -*- coding: utf-8 -*-

"""
Bayesian Curve Fitting:

p(t | x, x, t) = N(t | m(x), s^2(x))

where the mean and variance are:

m(x) = β (Φ(x)^T) (S) (sum n=1..N: Φ(xn)tn)
s^2(x) = (1/β) + (Φ(x)^T) (S) (Φ(x))

β represents the precision or (1 / variance):
β = (1/σ^2)

S is given by:
S^-1 = αI + β (sum n=1..N: Φ(xn)Φ(xn)^T)

where I is the unit matrix, and the vector φ(x) is defined as:
Φ(x) = (Φ0(x) ... ΦM(x))^T --> (x^0 x^1 x^2 ... x^M)^T
"""

import click
import csv
import logging
import math
import numpy


def get_phi(x, m):
    """Generates Φ(x) with polynomial M"""
    phi = numpy.zeros((m, 1), float)
    for i in range(m):
        phi[i][0] = math.pow(x, float(i))
    return phi


def generate(n):
    """Generates random data array of N entries"""
    return numpy.random.rand(n)


def read_data(filename):
    """Read in a csv file"""
    x = []
    t = []
    with open(filename, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            x.append(float(row[0]))
            t.append(float(row[1]))
    return x, t


def _setup_logging(debug):
    fmt = '%(message)s'
    loglevel = logging.INFO
    if debug:
        loglevel = logging.DEBUG
    logging.basicConfig(format=fmt, level=loglevel)


@click.command()
@click.option('--debug', is_flag=True, help="Show debug data")
@click.option(
    '--alpha', '-a', default=0.005, help='Alpha.', type=float, show_default=True)
@click.option(
    '--beta', '-b', default=11.100, help='Precision, (1/variance).', type=float, show_default=True)
@click.option(
    '--mth', '-m', default=6, help='M. The Mth order polynomial.', type=int, show_default=True)
@click.option(
    '--N', '-n', default=None,
    help='N. The number of input data to use from the data.csv. If empty, use the full data set',
    type=int)
@click.argument('data', type=click.Path(exists=True))
def predict(debug, alpha, beta, mth, n, data):
    _setup_logging(debug)
    logging.debug(f'Parameters - α:{alpha}, β:{beta}, Data: {data}, Mth:{mth}')
    x, t = read_data(data)
    N = n if n else len(t)

    # prediction is the next X
    predict = N + 1
    polynomial = mth + 1
    logging.debug(f'Infered Parameters - N:{N}, Polynomial:{polynomial}, x: {x}, t:{t}')

    # Calculate sums (Φ(x).t) and (φ(x).φ(x)^T)
    phi_sum = numpy.zeros((polynomial, 1), float)
    phi_sum_t = numpy.zeros((polynomial, 1), float)
    for i in range(N):
        phi = get_phi(x[i], polynomial)
        phi_sum = numpy.add(phi_sum, phi)
        phi_sum_t = numpy.add(phi_sum_t, (phi * t[i]))

    logging.debug(f'Phi Sum: {phi_sum}')
    logging.debug(f'Phi Sum T: {phi_sum_t}')

    # Get phi for 'prediction'
    phi = get_phi(predict, polynomial)
    logging.debug(f'Phi: {phi}')

    # Calculate the variance / standard deviation
    S = alpha * numpy.identity(polynomial) + beta * numpy.dot(phi_sum, phi.T)
    S = numpy.linalg.inv(S)
    variance = (float(1.0 / beta) + numpy.dot(numpy.dot(phi.T, S), phi))[0][0]

    # Calculate the mean
    mean = (beta * numpy.dot(phi.T, numpy.dot(S, phi_sum_t)))[0][0]

    # Print prediction values
    logging.debug(f'Data mean: {numpy.mean(t[:N])}')
    logging.info(f'Mean: {round(mean, 3)}')
    logging.info(f'Variance: {round(variance, 3)}')
    logging.info(
        f'The predicted range: [${round(mean - 3 * variance, 2)}'
        f' - ${round(mean + 3 * variance, 2)}]'
    )


if __name__ == '__main__':
    predict()
