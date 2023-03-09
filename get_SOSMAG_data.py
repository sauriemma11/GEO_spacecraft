import pytplot
from pyspedas import sosmag_load
from datetime import datetime, timedelta

start_date_str = '2022-12-07 00:00:00'
end_date_str = '2022-12-14 23:59:00'
start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
delta = timedelta(days=1)

save_to_dir = 'path/to/directory'

def tplot_ascii(tvar, filename=None, extension='.csv'):
    # tplot_ascii() taken from pytplot;
    # Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
    # Released under the MIT license.
    # This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
    # Verify current version before use at: https://github.com/MAVENSDC/Pytplot
    
    # grab data, prepend index column
    if filename == None:
        filename = tvar
    # save data
    pytplot.data_quants[tvar].to_pandas().to_csv(filename + extension)
    # only try to save spec_bins (y-values in spectrograms) if we're sure they exist
    if 'spec_bins' in pytplot.data_quants[tvar].coords.keys():
        pytplot.data_quants[tvar].coords['spec_bins'].to_pandas().to_csv(filename + '_v' + extension)
    print(f"File {filename+extension} saved successfully.")

user_input = input("Select variable to save as CSV. Enter 'gse', 'hpen', or 'pos': ")
while start_date <= end_date:
    trange = [start_date.strftime('%Y-%m-%d %H:%M:%S'), (start_date + delta).strftime('%Y-%m-%d %H:%M:%S')]
    file_name = 'SOSMAG_' + start_date.strftime('%Y%m%d') + '_'
    sosmag_load(trange=trange, datatype='1m')
    if user_input.lower() == 'hpen':
        tvar = 'sosmag_1m_b_hpen'
        filename = (save_to_dir+file_name+'hpen')
    elif user_input.lower() == 'gse':
        tvar = 'sosmag_1m_b_gse'
        filename = (save_to_dir+file_name+'gse')
    elif user_input.lower() == 'pos':
        tvar = 'sosmag_1m_position'
        filename = (save_to_dir+file_name+'pos')
    else:
        print("SOSMAG data not saved to local directory.")
        continue
    tplot_ascii(tvar=tvar, filename=filename)
    start_date += delta
