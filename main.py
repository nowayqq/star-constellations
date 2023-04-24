from funs_parsing import get_data
from prep_data_for_other_groups import *
from prep_data_for_histograms import get_histograms_dek, get_histograms_sph
from get_dist_and_prob_matrixes import get_matrixes


# get_data(save=True)

with open('filenames.csv') as f:
    filenames = f.read().split(',')[:-1]

# get_data_borodinov(filenames.copy())
# get_data_bobrov(filenames.copy())
# get_data_sidorov(filenames.copy())
# get_data_moskovchenko(filenames.copy())
# get_matrixes(filenames.copy())
get_histograms_dek(filenames.copy())
get_histograms_sph(filenames.copy())
