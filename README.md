Useful information can be found in https://www.linuxjournal.com/article/6983

SMART_GRAPHIC it is a set of two tools:
    1) smart_logger:        one for recording SMART data
    2) smart_graphic.py:    one for graphically displaying these data


smart_logger
    This shell script shall be run periodically, daily, or no less than once a week
    Typically it can be installed in /etc/cron.daily/

    it grabs SMART data of all disks then store them in /var/log/smart/<disk_Serial_Number>/

    Here below is a typical recording content
        # === START OF INFORMATION SECTION ===
        # Model Family:     Western Digital Green
        # Device Model:     WDC WD20EZRX-00D8PB0
        # Serial Number:    WD-WCD9UN4TC4RH
        # ...
        # Local Time is:    Sat Jul 29 11:19:39 2023 CEST
        # ...

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


smart_graphic.py
    This python script can be manually run at any time.
    Arguments shall be the list of recorded files
        python smart_graphic.py /var/log/smart/<disk_Serial_Number>/2023-*.txt
