import numpy as np
import csv
import os
import re
from os import listdir
from os.path import isfile, isdir, join
import pandas as pd
import datetime

# np.set_printoptions(threshold=np.inf)
pd.set_option("display.max_rows", None, "display.max_columns", None)
# set colormap for the graphs
step = 20

preconditioning_protocol = False
listed_data = {'Batches':{}, 'Unsorted Devices': {}};

# TODO: ADD working pixel selection based on dark JV
# TODO: extract shunt and series resistance from JV scan (light and dark or only light?)
# TODO: Add temperature and moisture extraction (during measurement)




# ---------------- Analysis functions --------------------------

"""
Inputs path, a list of file names, and the type of measurement (JV or MPP usually)
If the type is JV, the output is (Suns, dataset, sweep, head, scans, sweep_speeds, measurement_start_dates)
If the type is MPP, the output is (Suns, dataset, head, scans, measurement_start_dates)

"""
def import_file(path, files, type):
    """ Import the specified file. Returns light condition, JVdata.
        Returns the output in seconds, volts, milliamps"""
    # Initialize variables
    info = {}
    measurement_type = 'type:	Perform parallel JV' if type == 'JV' else 'type:	Stressing' if type == 'MPP' else None
    Suns, dataset, sweep, head, scans, sweep_speeds, measurement_start_dates = [
    ], [], [], [], [], [], []
    all_light_scans = {}
    match = re.search(r'(.+) - (.+)\[([0-8])\]_', files[0])
    name = match.group(1)
    var = match.group(2)
    pixel = match.group(3)
    info['Type'] = type
    info['Name'] = name
    info['Var']= var
    info['Pixel']= pixel
    info['Measurements'] = []
    # Begin analysis
    for measurement in files:
        meas_info = {}
        filepath = join(path, measurement)
        with open(filepath) as f:
            lines = list(f)
        if measurement_type not in lines[1]:
            pass
            # parts data from descriptors (which specify what column is what
        else:
            flag_normalize = False
            data = []
            for line in lines:
                try:
                    data.append([float(item.split(']')[0]) for item in line.split(',')])
                    # if lines[1] == 'type:	MPP tracking':
                    #     print(line)
                except ValueError as e:
                    if 'Light intensity' in line:
                        sun = float(line.split(',')[1].split(']')[0])
                        meas_info['Light Intensity'] = sun
                    elif 'Sample area' in line:
                        Area = float(re.search(r'\d+\.\d+', line).group())
                        if Area == 0:
                            Area = .0625
                        meas_info['Pixel Area'] = Area
                    elif '(mA)' in line:
                        flag_normalize = True
                    elif 'direction' in line:
                        d = int(re.search(r'(\d+)\.\d+', line).group(1))
                        swp = ['Fw'] if d == 0 else ['Rv'] if d == 1 else [
                            'Fw', 'Rv'] if d == 2 else ['Rv', 'Fw']

                        meas_info['Sweep'] = {}
                        if d==0:
                            meas_info['Sweep']['Fw']=[]
                        elif d==1:
                            meas_info['Sweep']['Rv']=[]
                        else:
                            meas_info['Sweep']['Fw']=[]
                            meas_info['Sweep']['Rv']=[]

                    elif 'sweep_speed' in line:
                        speed = float(
                            re.search(r'\d+\.\d+', line).group())
                        meas_info['Speed'] = speed
                    elif 'start_time' in line:
                        line = line.replace('#start_time:\t', '')
                        line = line.replace('\n', '')
                        start_date = datetime.datetime.strptime(
                            line, '%m/%d/%Y %H:%M:%S %p')
                        discard = datetime.timedelta(minutes=start_date.minute,
                                                     seconds=start_date.second)
                        start_date -= discard
                        if discard >= datetime.timedelta(minutes=30):
                            start_date += datetime.timedelta(hours=1)

                        meas_info['Start Date']= start_date
                    else:
                        pass

            data = np.array(data)
            # counter for the number of same scans performed on a device
            if any(sun == x for x in all_light_scans):
                all_light_scans[sun] += 1
            if all(sun != x for x in all_light_scans):
                all_light_scans[sun] = 0
            if type == 'MPP' and 'type:	Stressing' in lines[1]:
                if flag_normalize:
                    data[:, 2] /= Area
                else:
                    data[:, 2] *= 1000 * 1000
                Suns.append(sun)
                dataset.append(data)
                meas_info['Data']=data
                head.append('{}__{}__pixel{}__{}__scan{}'.format(match.group(1), match.group(2), match.group(3),
                                                             str(sun / 100) + 'Sun', all_light_scans[sun]))

                scans.append(all_light_scans[sun])
                measurement_start_dates.append(start_date)
            elif type == 'JV' and 'type:	Perform parallel JV' in lines[1]:
                if flag_normalize:
                    data[:, 1] /= Area
                else:
                    data[:, 1] *= 1000
                if swp == ['Fw'] or swp == ['Rv']:
                    Suns.append(sun)
                    dataset.append(data)
                    sweep.append(swp[0])
                    meas_info['Sweep'][swp[0]] = data
                    head.append('{}__{}__pixel{}__{}__{}__scan{}'.format(match.group(1), match.group(2), match.group(3),
                                                                     'Dark' if sun == 0 else str(sun / 100) + 'Sun', swp[0], all_light_scans[sun]))

                    scans.append(all_light_scans[sun])
                    sweep_speeds.append(speed)
                    measurement_start_dates.append(start_date)
                elif swp == ['Fw', 'Rv'] or swp == ['Rv', 'Fw']:
                    Suns.append(sun)
                    Suns.append(sun)
                    n = next(i for i, x in enumerate(
                        data[:, 0]) if np.isnan(x))
                    dataset.append(data[:n, :])
                    dataset.append(data[n + 1:-1, :])

                    if swp==['Fw', 'Rv']:
                        meas_info['Sweep']['Fw'] = data[:n, :]
                        meas_info['Sweep']['Rv'] = data[n + 1:-1, :]
                    elif swp==['Rv', 'Fw']:
                        meas_info['Sweep']['Rv'] = data[:n, :]
                        meas_info['Sweep']['Fw'] = data[n + 1:-1, :]
                    else:
                        print('Something went wrong in the data info saving')
                    sweep.append(swp[0])
                    sweep.append(swp[1])
                    head.append('{}__{}__pixel{}__{}__{}__scan{}'.format(match.group(1), match.group(2), match.group(3),
                                                                     'Dark' if sun == 0 else str(sun / 100) + 'Sun', swp[0], all_light_scans[sun]))
                    head.append('{}__{}__pixel{}__{}__{}__scan{}'.format(match.group(1), match.group(2), match.group(3),
                                                                     'Dark' if sun == 0 else str(sun / 100) + 'Sun', swp[1], all_light_scans[sun]))

                    scans.append(all_light_scans[sun])
                    scans.append(all_light_scans[sun])
                    sweep_speeds.append(speed)
                    sweep_speeds.append(speed)
                    measurement_start_dates.append(start_date)
                    measurement_start_dates.append(start_date)

            info['Measurements'].append(meas_info)

    return (Suns, dataset, head, scans, measurement_start_dates, info) if type == 'MPP' else (Suns, dataset, sweep, head, scans, sweep_speeds, measurement_start_dates, info) if type == 'JV' else []





"""
The input is the JV data, and the power into the pixel
The output is the Voc, Jsc, FF, and PCE

"""
def JV_parameters(JV, Pin):
    # JV_smooth = signal.savgol_filter(JV[:,1], 5,3)
    # I actually removed the smoothing to avoid problems with changes in FF, Jsc,Voc....
    JV_smooth = JV[:, 1]
    # the filter is at the line before, if we want to reintroduce it. Overall it was not super effective.
    try:
        # np.around approximate to .2 digits
        Jsc = np.around(JV_smooth[np.nanargmin(np.abs(JV[:, 0]))], 2)
        # np.nanargmin return position in the array whwere | V | is minimum
    except ValueError:
        return [np.nan, np.nan, np.nan, np.nan]
    Voc = np.around(JV[np.nanargmin(np.abs(JV_smooth)), 0], 2)
    JV_smoothed = np.hstack(
        [JV[:, 0][:, np.newaxis], JV_smooth[:, np.newaxis]])
    try:
        Pout = np.nanmax(JV_smoothed[:, 0] * JV_smoothed[:, 1])
        PCE = np.around(Pout / Pin * 100, 2)
        FF = np.around(Pout * 100 / (Voc * Jsc), 2)
    except RuntimeWarning:
        return [np.nan, np.nan, np.nan, np.nan]
        # condition over which collected parameters are not considered trustable.
    if Voc > 0.01 and Jsc > .01 and PCE > .01 and FF < 150:
        return [Voc, Jsc, FF, PCE]
    else:
        return [np.nan, np.nan, np.nan, np.nan]


# NOTE: here i need a class to be able return the input values. If I insert a function to create a child window
# I will have no way to store the data I saved (except by creating a global variable)



def Importer(analysis_path):

    os.chdir(analysis_path)
    devices_data = join(analysis_path, 'devices')
    root = os.path.abspath(join(analysis_path, os.pardir))
    experiment = os.path.basename(analysis_path)
    # all paios files are stored in different folders, this adds all folders as paths and explore them
    folders = [f for f in os.listdir(devices_data) if isdir(
        join(devices_data, f)) and f != 'Analysis']
    # RETRIEVE NAME for each device of the experiment
    names = set([re.sub('\[[1-8]\]$', '', f) for f in folders])
    # stores in this folder the elaborated data

    print(
        f'---------------------------------{experiment} Analysis Begun---------------------------------')

    # mW/cm2 - I assume AM1.5 impinging intensity. To be updated once the impinging power is known and calibrated.
    Pin = 100
    JVLog, MPPTLog = [], []
    for name in names:
        print('{}    --Started--'.format(name))


        device = [f for f in folders if re.sub('\[[1-8]\]$', '', f) == name]

        # device_dir = create_folder(result_dir, name)
        # loop iterates over all pixels and measurements done on a device.
        Illuminations, JVs, scan_directions, header, scan_number, sweep_speed, measurement_start_date = [
        ], [], [], [], [], [], []
        Light_mppt, P_mppt, head_mppt, scan_number_mppt = [], [], [], []
        stabilized_mpp, time, measurement_start_date_MPP = [], [], []
        working_JV, working_mpp = [], []
        for pixel in device:
            path = join(devices_data, pixel)
            files = [f for f in listdir(
                path) if re.search('0.csv$', f) != None]
            # type:	Perform parallel JV
            # keeps track of program progress
            # JV
            I, J, s, h, sc, sp, msd, info = import_file(path, files, 'JV')

            var = info['Var']
            name = info['Name']
            if var not in listed_data['Batches']:
                listed_data['Batches'][var]={}

            if name not in listed_data['Batches'][var]:
                listed_data['Batches'][var][name]={}

            listed_data['Batches'][var][name][f"pixel{info['Pixel']}"] = {}
            listed_data['Batches'][var][name][f"pixel{info['Pixel']}"]['Jv Data'] = info






            Illuminations.extend(I)
            JVs.extend(J)
            scan_directions.extend(s)
            header.extend(h)
            scan_number.extend(sc)
            sweep_speed.extend(sp)
            measurement_start_date.extend(msd)
            # MPPT Plotting
            L, mppt, H, sc_mppt, msd_mppt, info = import_file(path, files, 'MPP')
            listed_data['Batches'][var][name][f"pixel{info['Pixel']}"]['MPP Data'] = info
            Light_mppt.extend(L)
            P_mppt.extend(mppt)
            head_mppt.extend(H)
            scan_number_mppt.extend(sc_mppt)
            measurement_start_date_MPP.extend(msd_mppt)
            # print(mppt)
            # print(mppt[0][-5:, 0])
            time.extend([np.mean(x[-5:, 0]) for x in mppt])
            stabilized_mpp.extend(
                [np.mean(x[-5:, 1] * x[-5:, 2]) if np.mean(x[-5:, 1] * x[-5:, 2]) > 0 else 0 for x in mppt])
        # print('step 0')
        # print(len(Illuminations), len(JVs), len(
        #     scan_directions), len(header), len(scan_number))
        # print(len(Light_mppt), len(P_mppt), len(
        #     head_mppt), len(scan_number_mppt), len(time), len(stabilized_mpp))
        # print(H)
        MPPTLog.extend([np.append([item for k, item in enumerate(head_mppt[w].split('__')) if k != 3 and k != 4],
                                  [scan_number_mppt[w], Light_mppt[w], time[w], stabilized_mpp[w], measurement_start_date_MPP[w]]) for w in range(len(head_mppt))])
        lights = set(Illuminations)
        Illuminations = np.array(Illuminations)
        for light in lights:
            hed0 = [header[i]
                    for i, x in enumerate(Illuminations) if x == light]
            JV0 = [JVs[i] for i, x in enumerate(Illuminations) if x == light]
            # JV = JVs)
            sp0 = [scan_directions[i]
                   for i, x in enumerate(Illuminations) if x == light]
            sc_num0 = [scan_number[i]
                       for i, x in enumerate(Illuminations) if x == light]
            swp_spd0 = [sweep_speed[i]
                        for i, x in enumerate(Illuminations) if x == light]
            ms_st_date0 = [measurement_start_date[i]
                           for i, x in enumerate(Illuminations) if x == light]
            # triplicate headers for mppt
            PCE_mppt0 = [P_mppt[i]
                         for i, x in enumerate(Light_mppt) if x == light]
            head_mpp0 = [head_mppt[i]
                         for i, x in enumerate(Light_mppt) if x == light]
            sc_num_mpp = [scan_number_mppt[i]
                          for i, x in enumerate(Light_mppt) if x == light]
            # print('step 1')
            # print(len(hed0), len(JV0), len(
            #     sp0))
            # print(len(PCE_mppt0), len(head_mpp0), len(sc_num_mpp))
            for scan in set(scan_number):
                hed = [hed0[i]
                       for i, x in enumerate(sc_num0) if x == scan for _ in (0, 1)]

                JV = [JV0[i] for i, x in enumerate(sc_num0) if x == scan]
                # JV = JVs
                try:
                    short = min([len(x) for x in JV])
                except ValueError:
                    pass
                JV = [i[:short, :] for i in JV]
                sp = [sp0[i]
                      for i, x in enumerate(sc_num0) if x == scan]
                swp_spd = [swp_spd0[i]
                           for i, x in enumerate(sc_num0) if x == scan]
                ms_st_date = [ms_st_date0[i]
                              for i, x in enumerate(sc_num0) if x == scan]
                # triplicate headers for mppt
                PCE_mppt = [PCE_mppt0[i]
                            for i, x in enumerate(sc_num_mpp) if x == scan]
                hed_mpp = [head_mpp0[i]
                           for i, x in enumerate(sc_num_mpp) if x == scan for _ in (0, 1, 2)]
                # print('step 2')
                # print(len(hed), len(JV), len(
                #     sp))
                # print(len(PCE_mppt), len(hed_mpp), len(sc_num_mpp))
                # print(np.array(Illuminations) == light)
                # duplicates headers to account for V and J columns in JV scan




                if light != 0:
                    # ------------------------------------
                    #   MPPT plotting & stab_mpp extraction
                    # ------------------------------------



                    # ------------------------------------
                    #         JV_Log.txt creation
                    # ------------------------------------
                    for i in range(len(sp)):
                        measurement_parameters = np.append([re.search(r'^(.+?)_', hed[2 * i]).group(1),
                                                            'pixel{}'.format(re.search(r'_pixel([0-8])_',
                                                                                   hed[2 * i]).group(1)), sp[i], scan,
                                                            re.search(r'.+ - (.+)\[[0-8]\]',
                                                                      device[-1]).group(1), '{:.2f}'.format(light)],
                                                           JV_parameters(JV[i], light))
                        measurement_parameters = np.append(
                            measurement_parameters, [swp_spd[i], ms_st_date[i]])
                        JVLog.append(measurement_parameters)

        print('{}    --Completed--'.format(name))


# --------------------------
# Dataframe creation
# ADDED v.2.7 - Sweep speed and measurement start date parameters
# --------------------------

    col_names = ['Device', 'Pixel', 'Sweep Direction', 'Scan number', 'Variable', 'Pin[mW/cm2]',
                 'Voc[V]', 'Jsc[mA/cm2]', 'FF[%]', 'PCE[%]', 'Sweep Speed', 'Measurement Start Date']
    df0 = pd.DataFrame(JVLog, columns=col_names)
    # df0.sort_values(['Variable', 'Device'], inplace=True)

    df0 = df0.astype(
        {'Scan number': 'int64', 'Pin[mW/cm2]': 'float64', 'Voc[V]': 'float64', 'Jsc[mA/cm2]': 'float64', 'FF[%]': 'float64', 'PCE[%]': 'float64'})

# ------------------------------------
# ADDED v2.5 - request user to input device structures
# ADDED v2.6 - variable in device name and widened stack field
# ------------------------------------


    list_of_devices = df0[['Device', 'Variable']
                          ].drop_duplicates(subset='Device')

    # print(batch_params.architectures)
    # print(batch_params.stack_df)
# ------------------------------------
#         Boxplots and Yield
# ------------------------------------

    df = df0.copy()
    # Error!!! the line below takes the max of Fw and Rv, but they can be max in different lines!
    df.loc[:, 'maxpce'] = df[['Device', 'Pixel', 'Sweep Direction',  'Pin[mW/cm2]', 'PCE[%]']].groupby(
        ['Device', 'Pixel', 'Sweep Direction', 'Pin[mW/cm2]'])['PCE[%]'].transform(max)
    df = df[df['PCE[%]'] == df['maxpce']]
    del df['maxpce']
    # del df['maxpce']
    df.sort_values(['Variable', 'Device'], inplace=True)

    # df = df0.loc[pd.to_numeric(df0['PCE[%]'], errors='coerce').notnull(), :]
    variable_yeld = df.groupby('Variable').size().div(
        df0[df0['Scan number'] == 0].groupby('Variable').size()).mul(100)
    device_yeld = df.groupby('Device').size().div(
        df0[df0['Scan number'] == 0].groupby('Device').size()).mul(100)




    directions = df['Sweep Direction'].unique()
    # print(directions)
    if directions.size > 0:
        df.loc[:, 'Device+Variable'] = df.loc[:, ['Variable', 'Device']
                                              ].agg(' -- '.join, axis=1)  # to correct

        del df['Device+Variable']
        df_Rv = df0[df0['Sweep Direction'] == 'Rv'].reset_index()
        df_Fw = df0[df0['Sweep Direction'] == 'Fw'].reset_index()
        del df_Rv['Sweep Direction']
        del df_Fw['Sweep Direction']
        df_JV = df_Rv.merge(df_Fw, how='outer', on=[
            'Device', 'Pixel', 'Scan number', 'Variable', 'Pin[mW/cm2]', 'Sweep Speed', 'Measurement Start Date'], suffixes=[' Rv', ' Fw'])
        del df_JV['index Fw']
        del df_JV['index Rv']
        df_JV = df_JV.astype(
            {'Pin[mW/cm2]': 'float64', 'Scan number': 'int64'})

        df_mpp = pd.DataFrame(MPPTLog,
                              columns=['Device', 'Variable', 'Pixel', 'Scan number',  'Pin[mW/cm2]', 'Time_MPP [s]', 'Stabilized_MPP [%]', 'Measurement Start Date'])

        df_mpp[['Pin[mW/cm2]', 'Scan number', 'Stabilized_MPP [%]']] = df_mpp[['Pin[mW/cm2]', 'Scan number', 'Stabilized_MPP [%]']].astype(
            {'Pin[mW/cm2]': 'float64', 'Scan number': 'float64', 'Stabilized_MPP [%]': 'float64'}, copy=False)
        df_mpp['Scan number'] = df_mpp['Scan number'].astype(
            {'Scan number': 'int64'}, copy=False)

        dff = df_JV.merge(df_mpp, how='outer', on=[
            'Device', 'Pixel', 'Scan number', 'Variable', 'Pin[mW/cm2]', 'Measurement Start Date'])
        dff.insert(0, 'Batch', experiment)


        dff.insert(17, 'Preconditioning Protocol', preconditioning_protocol)
        dff.sort_values(['Variable', 'Device', 'Pixel',
                         'Scan number'], inplace=True)
        # print(dff)
        dff = dff[['Batch', 'Device', 'Pixel', 'Variable',  'Scan number',
                   'Pin[mW/cm2]', 'Voc[V] Rv', 'Jsc[mA/cm2] Rv', 'FF[%] Rv', 'PCE[%] Rv', 'Voc[V] Fw',
                   'Jsc[mA/cm2] Fw', 'FF[%] Fw', 'PCE[%] Fw', 'Time_MPP [s]', 'Stabilized_MPP [%]', 'Preconditioning Protocol', 'Sweep Speed', 'Measurement Start Date']]



        for i, res in dff.iterrows():

            res_data = res[['Scan number','Pin[mW/cm2]', 'Voc[V] Rv', 'Jsc[mA/cm2] Rv', 'FF[%] Rv', 'PCE[%] Rv', 'Voc[V] Fw',
                            'Jsc[mA/cm2] Fw', 'FF[%] Fw', 'PCE[%] Fw', 'Time_MPP [s]', 'Stabilized_MPP [%]', 'Preconditioning Protocol', 'Sweep Speed', 'Measurement Start Date']]

            for ax in list(res_data.axes[0]):

                listed_data['Batches'][res['Variable']][res['Device']][res['Pixel']][ax] = res_data[ax]
            #listed_data['Batches'][batch]
        #dff.to_csv(join(result_dir, f'{experiment}_Log.csv'), index=False)



    else:
        return 'Sorry, no working device in this batch.....boxplots skipped'
    print(f'{experiment} Analysis Completed')
    return listed_data



if __name__ == '__main__':
    path = "C:\\Users\\Daniel\\Documents\\College\\Georgia Tech\\Research\\Experiment Rounds\\Two-Step\\Decreasing PbI2\\xported\\xported"
    Importer(path)
