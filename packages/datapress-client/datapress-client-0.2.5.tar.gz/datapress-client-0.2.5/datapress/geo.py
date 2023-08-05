import os
import pandas as pd

# datapress_client directory
DIRNAME = os.path.dirname(os.path.abspath(__file__))

"""
List the LSOAs in a given header region (as numpy array)
"""


def get_lsoas_in(place):
    filename = os.path.join(DIRNAME, 'static', 'lsoa_lookup.csv')
    frame = pd.read_csv(filename)
    frame = frame[frame['UTLA19NM'] == place]
    return frame['LSOA11CD'].unique()


"""
List the LADs in a given header region (as numpy array)
"""


def get_lads_in(place):
    filename = os.path.join(DIRNAME, 'static', 'lsoa_lookup.csv')
    frame = pd.read_csv(filename)
    frame = frame[frame['UTLA19NM'] == place]
    return frame['LAD19CD'].unique().tolist()


def get_geography_code(place):
    filename = os.path.join(DIRNAME, 'static', 'lsoa_lookup.csv')
    frame = pd.read_csv(filename)
    frame = frame[frame['UTLA19NM'] == place]
    return frame['UTLA19CD'].unique().tolist()
