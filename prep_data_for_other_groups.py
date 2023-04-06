import os
import pandas as pd
from tqdm import tqdm
import scipy.stats as stats
from functions import make_it_beauty


def get_data_borodinov(filenames):
    try:
        os.makedirs('data/data_borodinov')
    except:
        pass
    pbar = tqdm(total=88)
    for name in filenames:
        pd.read_csv(f'data/{name}')[['Name', 'ra_degree', 'dec_degree']].to_csv(f'data/data_borodinov{name[4:]}', index=False)
        pbar.set_description(f'Processed {make_it_beauty(name[5:])}')
        pbar.update(1)
    pbar.set_description('Borodinov ready')
    pbar.close()


def get_data_bobrov(filenames):
    try:
        os.makedirs('data/data_bobrov')
    except:
        pass
    pbar = tqdm(total=88)
    for name in filenames:
        df = pd.read_csv(f'data/{name}')[['ra_degree', 'dec_degree', 'vis.mag.']]
        df.dropna().to_csv(f'data/data_bobrov{name[4:]}', index=False, header=False, sep='\t')
        pbar.set_description(f'Processed {make_it_beauty(name[5:])}')
        pbar.update(1)
    pbar.set_description('Bobrov ready')
    pbar.close()


def get_data_moskovchenko(filenames):
    try:
        os.makedirs('data/data_moskovchenko')
    except:
        pass
    pbar = tqdm(total=88)
    for name in filenames:
        df = pd.read_csv(f'data/{name}')[['Dist. (ly)', 'ra_degree', 'dec_degree']]
        Q1 = df['Dist. (ly)'].quantile(q=.25)
        Q3 = df['Dist. (ly)'].quantile(q=.75)
        IQR = df['Dist. (ly)'].apply(stats.iqr)
        df = df[~((df['Dist. (ly)'] < (Q1 - 1.5 * IQR)) | (df['Dist. (ly)'] > (Q3 + 1.5 * IQR)))]
        df.dropna().to_csv(f'data/data_moskovchenko{name[4:]}', index=False)
        pbar.set_description(f'Processed {make_it_beauty(name[5:])}')
        pbar.update(1)
    pbar.set_description('Moskovchenko ready')
    pbar.close()


def get_data_sidorov(filenames):
    try:
        os.makedirs('data/data_sidorov')
    except:
        pass
    pbar = tqdm(total=88)
    for name in filenames:
        df = pd.read_csv(f'data/{name}')
        df = df.drop(['Unnamed: 0'], axis=1)
        Q1 = df['vis.mag.'].quantile(q=.25)
        Q3 = df['vis.mag.'].quantile(q=.75)
        IQR = df['vis.mag.'].apply(stats.iqr)
        df = df[~((df['vis.mag.'] < (Q1 - 1.5 * IQR)) | (df['vis.mag.'] > (Q3 + 1.5 * IQR)))]
        df.to_csv(f'data/data_sidorov{name[4:]}', index=False)
        pbar.set_description(f'Processed {make_it_beauty(name[5:])}')
        pbar.update(1)
    pbar.set_description('Sidorov ready')
    pbar.close()
