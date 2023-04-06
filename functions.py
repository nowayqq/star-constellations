import math

import numpy as np
import pandas as pd


def make_it_beauty(s):
    while len(s) < 36:
        s += ' '
    return s


def generate_data(size):
    thetas = np.random.randint(0, 360, size)
    phis = np.random.randint(-90, 91, size)
    rs = np.random.randint(40, 1000, size)

    thetas = np.radians(thetas)
    phis = np.radians(phis)

    return thetas, phis, rs


def read_constellation_data(constellation_name):
    constellation_data = pd.read_csv(f'data/data/{constellation_name}')
    constellation_data = constellation_data.dropna(subset=['Dist. (ly)'])
    constellation_data = constellation_data.loc[constellation_data['Dist. (ly)'] <= 1500]
    thetas = constellation_data.loc[:, 'dec_degree']
    phis = constellation_data.loc[:, 'ra_degree']
    rs = constellation_data.loc[:, 'Dist. (ly)']

    thetas = thetas.to_numpy()
    thetas = thetas + 90
    phis = phis.to_numpy()
    rs = rs.to_numpy()

    thetas = np.radians(thetas)
    phis = np.radians(phis)

    return thetas, phis, rs


def calculate_distance(theta1, theta2, phi1, phi2, r1, r2):
    x1 = r1 * math.sin(theta1) * math.cos(phi1)
    y1 = r1 * math.sin(theta1) * math.sin(phi1)
    z1 = r1 * math.cos(theta1)

    x2 = r2 * math.sin(theta2) * math.cos(phi2)
    y2 = r2 * math.sin(theta2) * math.sin(phi2)
    z2 = r2 * math.cos(theta2)

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    l = math.sqrt(dx * dx + dy * dy + dz * dz)
    return l


def distance_to_prob(distance_matrix, size):
    prob_matrix = np.zeros((size, size))
    row_sums = np.sum(distance_matrix, axis=1)
    for i in range(0, size):
        for j in range(0, size):
            prob_matrix[i, j] = distance_matrix[i, j] / row_sums[i]
    return prob_matrix
