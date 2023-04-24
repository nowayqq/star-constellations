import os
from tqdm import tqdm
import matplotlib.pyplot as plt
from functions import *


def get_bins(l):
    return math.floor(1 + 3.322 * math.log10(l))


def get_histograms_dek(filenames):

    for i in range(len(filenames)):
        filenames[i] = filenames[i][5:]

    try:
        os.makedirs('data/result_danilkin/')
    except FileExistsError:
        pass
    try:
        os.makedirs('data/result_moskovchenko/distance')
    except FileExistsError:
        pass
    try:
        os.makedirs('data/result_moskovchenko/probability')
    except FileExistsError:
        pass

    pbar = tqdm(total=88)
    for name in filenames:
        thetas, phis, rs = read_constellation_data(name)
        matrix_size = thetas.size
        distance_matrix = np.zeros((matrix_size, matrix_size))
        for i in range(0, matrix_size):
            for j in range(0, matrix_size):
                distance_matrix[i, j] = calculate_distance(thetas[i], thetas[j], phis[i], phis[j], rs[i], rs[j])
        prob_matrix = distance_to_prob(distance_matrix, matrix_size)
        np.savetxt('data/result_moskovchenko/distance/' + name, distance_matrix, delimiter=',')
        np.savetxt('data/result_moskovchenko/probability/' + name, prob_matrix, delimiter=',')
        pbar.set_description(f'Processed {make_it_beauty(name[:-4])}')
        pbar.update(1)
    pbar.set_description('All moskovchenko results created')
    pbar.close()

    os.chdir(os.getcwd() + '\\data\\result_danilkin')
    pbar = tqdm(total=88)
    for name in filenames:
        distance = np.loadtxt(f"../result_moskovchenko/distance/{name}", delimiter=",")

        number = distance.shape[0]
        final_size = number * number
        distance = np.reshape(distance, final_size)

        plt.hist(distance, bins=get_bins(number), range=[0, 1500])
        plt.xlabel('Расстояние')
        plt.ylabel('Количество')
        plt.title('Гистограмма попарных расстояний в декартовых координатах', fontweight="bold")

        plt.savefig(f'{name[:-4]}.png', transparent=True, dpi=200)
        plt.close()
        pbar.set_description(f'Processed {make_it_beauty(name[:-4])}')
        pbar.update(1)
    pbar.set_description('All histograms created')
    pbar.close()
    os.chdir(os.getcwd() + '\\..\\..')


def get_histograms_sph(filenames):

    for i in range(len(filenames)):
        filenames[i] = filenames[i][5:]

    try:
        os.makedirs('data/result_thinh/')
    except FileExistsError:
        pass

    os.chdir(os.getcwd() + '\\data\\result_thinh')
    pbar = tqdm(total=88)
    for name in filenames:
        data = pd.read_csv(f'../result_borodinov/distance/Distance_{name.lower()}', header=None)

        plt.hist(data.values.flatten(), bins=get_bins(len(data.values)))
        plt.xlabel('Расстояние')
        plt.ylabel('Количество')
        plt.title('Гистограмма попарных расстояний в сферических координатах', fontweight="bold")

        plt.savefig(f'{name[:-4]}.png', transparent=True, dpi=200)
        plt.close()
        pbar.set_description(f'Processed {make_it_beauty(name[:-4])}')
        pbar.update(1)
    pbar.set_description('All histograms created')
    pbar.close()
