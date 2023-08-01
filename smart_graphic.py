import sys
# import re
import math
import random
import numpy as np
from datetime import datetime
# import subprocess
# import json
import matplotlib.pyplot as plt
import matplotlib as mpl

# plt.rcParams['toolbar'] = 'None' # Remove tool bar (upper)

def create_dict(existing_struct, name):
    try:
        existing_struct[name]
    except (KeyError, IndexError) as e: # For dict, list|tuple
        existing_struct[name] = dict()
    
def create_list(existing_struct, name):
    try:
        existing_struct[name]
    except (KeyError, IndexError) as e: # For dict, list|tuple
        existing_struct[name] = list()
    
def seek_for_pattern(fp, pattern):
    try:
        while pattern not in next(fp):
            pass

    except StopIteration:
        print('\tERROR: pattern not found: ', pattern)
        print('\tERROR: file is ill formatted')
        fp.close()
        sys.exit()

def parse_START_OF_INFORMATION_SECTION(fp, smart_infos):
    seek_for_pattern(fp, '=== START OF INFORMATION SECTION ===')

    # === START OF INFORMATION SECTION ===
    # Model Family:     Western Digital Green
    # Device Model:     WDC WD20EZRX-00D8PB0
    # Serial Number:    WD-WCD9UN4TC4RH
    # ...
    # Local Time is:    Sat Jul 29 11:19:39 2023 CEST
    # ...
    Model_Family = 'unknown'
    Device_Model = 'unknown'
    Device_Is    = 'unknown'

    for line_with_CRLF in fp:
        line = line_with_CRLF.rstrip()

        if len(line) < 1:
            # TODO: sanity check to ensure Serial_Number and Date has been found
            break

        name, value = line.partition(":")[::2]
        stripped_name  = name.strip()
        stripped_value = value.strip()

        if   stripped_name == 'Device is':
            Device_Is    = stripped_value

        elif stripped_name == 'Model Family':
            Model_Family = stripped_value

        elif stripped_name == 'Device Model':
            Device_Model = stripped_value

        elif stripped_name == 'Serial Number':
            Serial_Number = stripped_value

            create_dict(smart_infos, Serial_Number)

            # TODO: shall not assume that these variables are already defined

            smart_infos[Serial_Number]['Model Family'] = Model_Family
            smart_infos[Serial_Number]['Device Model'] = Device_Model
            smart_infos[Serial_Number]['Device_Is'   ] = Device_Is

        elif stripped_name == 'Local Time is':
            # Example:
            #     Local Time is:    Mon Jul 31 11:54:59 2023 CEST
            #
            # We need to convert to: 2023-07-31_11:54

            #### First method
            # splitted_date = stripped_value.split(' ')
            # YYYY = splitted_date[4]
            # MM   = splitted_date[1]   # Jan Feb Mar Apr May Jun ...
            # DD   = splitted_date[2]
            # YYYY_MM_DD = YYYY + ' ' + MM + ' ' + DD

            # %Y     year
            # %b     locale's abbreviated month name (e.g., Jan)
            # %d     day of month (e.g., 01)

            # date = datetime.strptime(YYYY_MM_DD, '%Y %b %d')

            #### Second method
            # first we need to remove leading CEST or whatever
            #     Local Time is:    Mon Jul 31 11:54:59 2023 CEST
            #                                                ^^^^
            date_noTZ = ' '.join(stripped_value.split()[:5])

            # %c     locale's date and time (e.g., Thu Mar  3 23:05:25 2005)

            Date = datetime.strptime(date_noTZ, '%c').strftime('%Y-%m-%d_%H:%M')
            print('\tdate and time is: ', Date)

            #### Third method
            # cmd  = 'LC_TIME="en_US.UTF-8"  date'
            # arg1 = '-d' + stripped_value
            # arg2 = '-u'
            # arg3 = '+%Y-%m-%d_%H:%M'                   # '--rfc-3339=seconds'
            # result = subprocess.run([cmd, arg1, arg2, arg3], stdout=subprocess.PIPE)
            # Date = result.stdout.decode('utf-8').strip()
            # print('\tUTC date and time is: ', Date)

            create_list(smart_infos[Serial_Number], 'date')

            smart_infos[Serial_Number]['date'].append(Date)

    return smart_infos[Serial_Number]

SMART_DATA_HEADERS_str = \
 'ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE'
SMART_DATA_HEADERS = SMART_DATA_HEADERS_str.split()
print(SMART_DATA_HEADERS)
# === START OF READ SMART DATA SECTION ===
# 
# ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
#   1 Raw_Read_Error_Rate     0x000f   118   082   006    Pre-fail  Always       -       187813757
#   3 Spin_Up_Time            0x0003   094   093   000    Pre-fail  Always       -       0
#   4 Start_Stop_Count        0x0032   095   095   020    Old_age   Always       -       6110
#   5 Reallocated_Sector_Ct   0x0033   100   100   036    Pre-fail  Always       -       0
#   7 Seek_Error_Rate         0x000f   089   060   030    Pre-fail  Always       -       856529937
#   9 Power_On_Hours          0x0032   060   060   000    Old_age   Always       -       35549
#  10 Spin_Retry_Count        0x0013   100   100   097    Pre-fail  Always       -       0
#  12 Power_Cycle_Count       0x0032   097   097   020    Old_age   Always       -       3910
# 187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0
# 189 High_Fly_Writes         0x003a   100   100   000    Old_age   Always       -       0
# 190 Airflow_Temperature_Cel 0x0022   076   048   045    Old_age   Always       -       24 (Min/Max 24/24)
# 194 Temperature_Celsius     0x0022   024   052   000    Old_age   Always       -       24 (0 17 0 0 0)
# 195 Hardware_ECC_Recovered  0x001a   078   045   000    Old_age   Always       -       221892027
# 197 Current_Pending_Sector  0x0012   100   100   000    Old_age   Always       -       0
# 198 Offline_Uncorrectable   0x0010   100   100   000    Old_age   Offline      -       0
# 199 UDMA_CRC_Error_Count    0x003e   200   200   000    Old_age   Always       -       0
# 200 Multi_Zone_Error_Rate   0x0000   100   253   000    Old_age   Offline      -       0
# 202 Data_Address_Mark_Errs  0x0032   100   253   000    Old_age   Always       -       0
pattern_for_slicing_SMART_DATA = \
 'xxx xxxxxxxxxxxxxxxxxxxxxxx xxxxxx   xxx   xxx   xxx    xxxxxxxxx xxxxxxxx xxxxxxxxxxx xxxxxxxxxxxxxx '
#           1         2         3         4         5         6         7         8         9
# 01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890

def SMART_DATA_Slices(string):
    i = j = 0
    while i < len(string):
        while string[i] == ' ':
            i += 1
        j = i+1
        while string[j] != ' ':
            j += 1
        yield i,j
        i = j+1

SMART_DATA_SLICES = [ij for ij in SMART_DATA_Slices(pattern_for_slicing_SMART_DATA)]

def SMART_DATA_Headers_and_Values(line):
    for col_name,ij in zip(SMART_DATA_HEADERS, SMART_DATA_SLICES):
        i,j = ij
        value = line[i:j]

        yield col_name, value.split()[0]

def parse_START_OF_READ_SMART_DATA_SECTION(fp, smart_data):
    seek_for_pattern(fp, '=== START OF READ SMART DATA SECTION ===')

    # === START OF READ SMART DATA SECTION ===
    # SMART Attributes Data Structure revision number: 1
    # Vendor Specific SMART Attributes with Thresholds:
    # ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
    #   5 Reallocated_Sector_Ct   0x0033   100   100   010    Pre-fail  Always       -       0
    #   9 Power_On_Hours          0x0032   099   099   000    Old_age   Always       -       543
    # ...
    seek_for_pattern(fp, SMART_DATA_HEADERS_str)

    # line_with_CRLF will be now the next line after the one that contains 'ID# ATTRIBUTE_NAME ...'

    for line_with_CRLF in fp:
        line = line_with_CRLF.rstrip()

        if len(line) < 1:
            break

        # line = line.lstrip()
        # splitted_line = re.split(' +', line)
        # print(splitted_line)

        # for i,j in SMART_DATA_Slices(pattern_for_slicing_SMART_DATA):
        #     # print(i,j)
        #     # print('<' + line[i:j] + '>', end=' ')
        for col_name, value in SMART_DATA_Headers_and_Values(line):
            # print(col_name, value, end=' ')
            # print(value, end=' ')

            #============================================================
            create_list(smart_data, 'all columns')

            if col_name not in smart_data['all columns']:
                smart_data['all columns'].append(col_name)
            #============================================================
            if   col_name == 'ID#':
                attribute_id = value

            elif col_name in ['ATTRIBUTE_NAME', 'FLAG', 'TYPE']:
                create_dict(smart_data, col_name)

                smart_data[col_name][attribute_id] = value

            # TODO: to add function for processing WHEN_FAILED column
            # elif col_name in ['VALUE','WORST','THRESH','WHEN_FAILED','RAW_VALUE']:
            elif col_name in ['VALUE','WORST','THRESH','RAW_VALUE']:
                create_dict(smart_data, col_name)

                create_list(smart_data[col_name], attribute_id)

                smart_data[col_name][attribute_id].append(int(value))
                #========================================================
                create_list(smart_data, 'picked columns')

                if col_name not in smart_data['picked columns']:
                    smart_data['picked columns'].append(col_name)
            #============================================================
        # print()

def plot_VALUE_WORST_THRESH_data(ax, date_data, smart_data, attribute_id):
    value_data  = smart_data['VALUE'    ][attribute_id]
    worst_data  = smart_data['WORST'    ][attribute_id]
    thresh_data = smart_data['THRESH'   ][attribute_id]

    ax.set_ylim(0, 210)
    ax.grid()

    attribute_name = smart_data['ATTRIBUTE_NAME'][attribute_id]
    attribute_type = smart_data['TYPE'          ][attribute_id]

    plot_title = f'ID# {attribute_id}: {attribute_name} ({attribute_type})'

    ax.set_title(plot_title)

    # blue, green, red, cyan, magenta, yellow, black, and white
    l1, = ax.plot(date_data, value_data, label='VALUE' , color='blue' , linestyle='solid')
    l2, = ax.plot(date_data, worst_data, label='WORST' , color='red'  , linestyle='dotted')
    l3, = ax.plot(date_data,thresh_data, label='THRESH', color='green', linestyle='dashdot')
    raw_data    = smart_data['RAW_VALUE'][attribute_id]
    twin_ax = ax.twinx()

    l4, = twin_ax.plot(date_data, raw_data, label='RAW_VALUE', color='blue', linestyle='dotted', marker='+')

    return l1,l2,l3,l4

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d_%H:%M")
    d2 = datetime.strptime(d2, "%Y-%m-%d_%H:%M")

    delta_seconds = (d2-d1).days*24*3600 + (d2 - d1).seconds
    delta_days = round(delta_seconds / (24*3600), 2)

    return delta_days

def plot_SMART_DATA(smart_infos, disk_SN):
    smart_data = smart_infos[disk_SN]

    start_date = smart_data['date'][0]
    print(start_date)
    day_axis = []
    for current_date in smart_data['date']:
        delta_days = days_between(start_date, current_date)
        day_axis.append(delta_days)

    print(day_axis)

    nb_attributes = len(smart_data['ATTRIBUTE_NAME'])

    ncols = 3
    nrows = math.ceil(nb_attributes / ncols)

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20.48,11.52), layout='constrained')
    fig.canvas.manager.full_screen_toggle() # toggle fullscreen mode

    Model_Family = smart_data['Model Family']
    Device_Model = smart_data['Device Model']

    disk_SN = ''.join(random.sample(disk_SN,len(disk_SN)))
    fig_title = f'Model Family: {Model_Family}, Device Model: {Device_Model}, Serial Number: {disk_SN}'
    fig.suptitle(fig_title)

    # Data for plotting

    for index, attribute_id in enumerate(smart_data['ATTRIBUTE_NAME']):
        # attribute_name = smart_data['ATTRIBUTE_NAME'][attribute_id]
        # print(index, attribute_id, attribute_name)

        row = index %  nrows
        col = index // nrows
        # print(row, col)
        ls = plot_VALUE_WORST_THRESH_data(axs[row,col], day_axis, smart_data, attribute_id)

        if (row,col == 0,0):
            fig.legend(ls, ('VALUE', 'WORST', 'THRESH', 'RAW_VALUE'), loc='upper left')

    fig.savefig(disk_SN + '.png', bbox_inches='tight', dpi=100)
    # plt.tight_layout()
    plt.show()

def plot_SMART_INFOS(smart_infos):
    for disk_SN in smart_infos:
        print(disk_SN)
        plot_SMART_DATA(smart_infos, disk_SN)

def main():
    smart_infos = dict()
    for filename in sys.argv[1:]:
        print(filename)
        
        with open(filename, 'r') as fp:
            smart_data  = parse_START_OF_INFORMATION_SECTION    (fp, smart_infos)

            ret_status  = parse_START_OF_READ_SMART_DATA_SECTION(fp, smart_data)

    # print(json.dumps(smart_infos, indent=4))

    plot_SMART_INFOS(smart_infos)

if __name__ == '__main__':
    if __debug__:
        print("DEBUG mode is enabled. Use -O flag to disable it")
        print()
        print('Useful information can be found in https://www.linuxjournal.com/article/6983')
        print()

    main()
