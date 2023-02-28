import pytplot
from pyspedas import sosmag_load

trange = ['2023-02-23 00:00:00', '2023-02-23 23:59:00']
file_name = 'testSOSMAG_20230223_' 
save_to_dir = '/path/to/data/directory'

# tplot_ascii() taken from pytplot;
# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot
def tplot_ascii(tvar, filename=None, extension='.csv'):
    # grab data, prepend index column
    if filename == None:
        filename = tvar
    # save data
    pytplot.data_quants[tvar].to_pandas().to_csv(filename + extension)
    # only try to save spec_bins (y-values in spectrograms) if we're sure they exist
    if 'spec_bins' in pytplot.data_quants[tvar].coords.keys():
        pytplot.data_quants[tvar].coords['spec_bins'].to_pandas().to_csv(filename + '_v' + extension)


# load data with the given time range
sosmag_load(trange=trange, datatype='1m')

user_input = input("Select variable to save as CSV. Enter 'gse', 'hpen', or 'pos': ")
if user_input.lower() == 'hpen':
    tplot_ascii(tvar='sosmag_1m_b_hpen', filename=(save_to_dir+file_name+'hpen'))
elif user_input.lower() == 'gse':
    tplot_ascii(tvar='sosmag_1m_b_gse', filename=(save_to_dir+file_name+'gse'))
elif user_input.lower() == 'pos':
    tplot_ascii(tvar='sosmag_1m_position', filename=(save_to_dir+file_name+'pos'))
else:
    print("SOSMAG data not saved to local directory.")


