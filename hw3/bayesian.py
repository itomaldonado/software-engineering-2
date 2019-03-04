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


@click.command()
@click.option(
    '--alpha', '-a', default=0.005, help='Alpha.', type=float, show_default=True)
@click.option(
    '--beta', '-b', default=11.100, help='Precision, (1/variance).', type=float, show_default=True)
@click.option(
    '--mth', '-m', default=9, help='M. The Mth order polynomial.', type=int, show_default=True)
@click.argument('data', type=click.Path(exists=True))
@click.argument('predict', type=float)
def predict(alpha, beta, mth, data, predict):
    print(f'Parameters - α:{alpha}, β:{beta}, Data: {data}, Mth:{mth}, prediction:{predict}')
    x, t = read_data(data)
    N = len(t)
    polynomial = mth + 1

    # Calculate sums (Φ(x).t) and (φ(x).φ(x)^T)
    phi_sum = numpy.zeros((polynomial, polynomial), float)
    phi_sum_t = numpy.zeros((polynomial, 1), float)
    for i in range(N):
        phi = get_phi(x[i], polynomial)
        phi_sum = phi_sum + numpy.multiply(phi, phi.T)
        phi_sum_t = phi_sum_t + (t[i] * phi)

    # Get phi for 'prediction'
    phi = get_phi(predict, polynomial)

    # Calculate the variance / standard deviation
    S = numpy.linalg.inv((alpha * numpy.identity(polynomial)) + (beta * phi_sum))
    variance = (float(1.0 / beta) + numpy.dot(numpy.dot(phi.T, S), phi))[0][0]

    # Calculate the mean
    mean = ((beta * phi.T) * S * phi_sum_t)[0][0]

    # Print prediction values
    print(f'Variance: {variance}')
    print(f'Mean: {mean}')


if __name__ == '__main__':
    predict()
