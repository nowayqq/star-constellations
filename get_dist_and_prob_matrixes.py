import os
from tqdm import tqdm
from functions import *


def get_matrixes(filenames):

    for i in range(len(filenames)):
        filenames[i] = filenames[i][5:]
    pi = 3.14159265

    try:
        os.makedirs('data/result_borodinov/distance')
    except FileExistsError:
        pass

    try:
        os.makedirs('data/result_borodinov/probability')
    except FileExistsError:
        pass

    pbar = tqdm(total=88)
    for file in filenames:
        df = pd.read_csv(f'data/data_borodinov/{file}')
        df['ra_radian'] = df[['ra_degree']] * pi / 180
        df['dec_radian'] = df[['dec_degree']] * pi / 180
        df.drop(['ra_degree', 'dec_degree'], axis=1)
        matrix = df[['ra_radian', 'dec_radian']].to_numpy()
        np.savetxt(f"data/result_borodinov/distance/Distance_{file.lower()}", Distance(matrix),
                   delimiter=",", fmt=" %.6f ")
        np.savetxt(f"data/result_borodinov/probability/Probability_{file.lower()}", Probability(Distance(matrix)),
                   delimiter=",", fmt=" %.6f ")
        pbar.set_description(f'Processed {make_it_beauty(file[5:])}')
        pbar.update(1)
    pbar.set_description('All matrixes processed')
    pbar.close()
