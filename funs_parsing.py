import os
import re
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm


def make_it_beauty(s):

    while len(s) < 36:
        s += ' '
    return s


def parse_url(lst):

    prefix = 'https://en.wikipedia.org/wiki/'
    urls = [prefix + re.findall('a href=\"/wiki/(.*)\" title=.*', item)[0] for item in lst]
    return urls


def get_urls(url, save=False):

    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    indiatable = soup.find('table', {'class': "multicol"})
    if save:
        filenames = []
        urls = parse_url(str(indiatable).split('<li>')[1:])
        for url in urls:
            filenames.append(f'data/{url[30:]}.csv')

        with open('filenames.csv', 'w+') as f:
            for name in filenames:
                f.write(name + ',')
        return urls
    return parse_url(str(indiatable).split('<li>')[1:])


def ra_parser(ra):

    try:
        h = int(re.findall('(\d*)h', ra)[0])
        m = int(re.findall('(\d*)m', ra)[0])
        s = float(re.findall('(\d*\.*\d*)s', ra)[0])
        return h * 15 + m * (0.15 / 9) + s * (0.002500005 / 9)
    except:
        return None


def dec_parser(dec):

    try:
        flag = False
        deg = re.findall('(−*\d*)°', dec)[0]
        if deg[0] == '−':
            deg = int(deg[1:]) * -1
            flag = True
        else:
            deg = int(deg)
        m = int(re.findall('(\d*)′', dec)[0])
        s = float(re.findall('(\d*\.*\d*)″', dec)[0])
        if not flag:
            return deg + m * (0.15 / 9) + s * (0.002500005 / 9)
        else:
            return deg - m * (0.15 / 9) - s * (0.002500005 / 9)
    except:
        return None


def abs_mag_converter(abs_mag):

    abs_mag = str(abs_mag)
    tmp = re.findall('−+\d*\.*\d*', abs_mag)
    if len(tmp) > 0:
        abs_mag = tmp[0]
    try:
        if abs_mag[0] == '−':
            return float(abs_mag[1:]) * -1
        else:
            return float(abs_mag)
    except:
        try:
            return float(abs_mag)
        except:
            return abs_mag


def vis_mag_converter(vis_mag):

    vis_mag = str(vis_mag)
    tmp = re.findall('−+\d*\.*\d*', vis_mag)
    if len(tmp) > 0:
        try:
            vis_mag = re.findall('\d+\.\d+', vis_mag)[0]
        except:
            vis_mag = tmp[0]
    try:
        if vis_mag[0] == '−':
            return float(vis_mag[1:]) * -1
        else:
            return float(vis_mag)
    except:
        try:
            return float(vis_mag)
        except:
            try:
                return re.findall('\d+\.\d+', vis_mag)[0]
            except:
                return None


def dist_ly_converter(dist_ly):

    dist_ly = str(dist_ly)
    try:
        return float(re.findall('~?(\d*)', dist_ly)[0])
    except:
        return None


def get_data(ur='https://en.wikipedia.org/wiki/Lists_of_stars_by_constellation', save=False):

    urls = get_urls(ur, save)

    try:
        os.makedirs('data/data')
    except FileExistsError:
        pass

    pbar = tqdm(total=88)
    for url in urls:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        indiatable = soup.find('table', {'class': "wikitable"})
        df = pd.read_html(str(indiatable))
        df = pd.DataFrame(df[0]).drop(['Notes'], axis=1)
        try:
            df = df.drop(['Unnamed: 13'], axis=1)
            df = df.drop(['Unnamed: 12'], axis=1)
        except:
            try:
                df = df.drop(['Unnamed: 12'], axis=1)
                df = df.drop(['Unnamed: 13'], axis=1)
            except:
                pass
        df = df.iloc[:-2]
        ra_deg = [ra_parser(item) for item in df['RA']]
        dec_deg = [dec_parser(item) for item in df['Dec']]
        abs_mag = [abs_mag_converter(item) for item in df['abs.mag.']]
        vis_mag = [vis_mag_converter(item) for item in df['vis.mag.']]
        dist_ly = [dist_ly_converter(item) for item in df['Dist. (ly)']]

        df['ra_degree'] = ra_deg
        df['dec_degree'] = dec_deg
        df['abs.mag.'] = abs_mag
        df['vis.mag.'] = vis_mag
        df['Dist. (ly)'] = dist_ly
        df.to_csv(f'data/data/{url[29:]}.csv')
        pbar.set_description(f'Processed {make_it_beauty(url[30:])}')
        pbar.update(1)
    pbar.set_description('All data parsed')
    pbar.close()
