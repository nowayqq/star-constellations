from funs_parsing import get_data
from prep_data_for_other_groups import *
from prep_data_for_histograms import get_histograms
from get_dist_and_prob_matrixes import get_matrixes


# get_data(save=True)
with open('filenames.csv') as f:
    filenames = f.read().split(',')[:-1]


# get_histograms(filenames)
# get_matrixes(filenames)
# get_data_borodinov(filenames)
# get_data_bobrov(filenames)
# get_data_sidorov(filenames)
# get_data_moskovchenko(filenames)
