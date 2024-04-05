import subprocess
import pandas as pd
import matplotlib.pyplot as plt
def parse_energyplus_datetime_string(st, year=2021):
    st = st.strip()
    month = int(st[0:2])
    day = int(st[3:5])
    hour = int(st[7:9])
    minute = int(st[10:12])
    if not hour == 24:
        dt = pd.Timestamp(year,month,day,hour,minute)
    else:
        hour = 0
        dt = pd.Timestamp(year,month,day,hour,minute)
        dt += pd.Timedelta('1 day')
    return dt

if __name__ == '__main__':

    energyplus_install_dir = r'C:\EnergyPlusV9-4-0'
    idf_relative_filepath = 'CELL.idf'
    epw_relative_filepath =  'CHE_Geneva.epw'  #
    output_relative_directory = 'output'

    cl_st = (f'"{energyplus_install_dir}\\EnergyPlus" '
             + '--readvars '  # included to create a .csv file of the results
             + f'--output-directory "{output_relative_directory}" '
             + f'--weather "{epw_relative_filepath}" '
             + f'"{idf_relative_filepath}"'
             )

    result = subprocess.run(cl_st, capture_output=True)
    print('---ARGS---\n',result.args)
    print('---RETURNCODE---\n',result.returncode, '(SUCCESS)' if result.returncode==0 else '(FAIL)')
    print('---STDOUT---\n',result.stdout.decode())
    print('---STDERR---\n',result.stderr.decode())

    rooms = {1: "CELLS:ROOMX1", 2: "CELLS:ENTRANCE", 3: "CELLS:ROOMX2"}

    keys = {1: ":Zone Total Internal Latent Gain Energy [J](Hourly)",
            2: ":Zone People Sensible Heating Rate [W](Hourly)",
            3: " GENERAL LIGHTING:Lights Total Heating Rate [W](Hourly)",
            4: ":Zone Windows Total Transmitted Solar Radiation Rate [W](Hourly)",
            5: ":Zone Mean Radiant Temperature [C](Hourly:ON)",
            6: ":Zone Mean Air Temperature [C](Hourly:ON)",
            7: ":Zone Operative Temperature [C](Hourly:ON)",
            8: ":Zone Infiltration Sensible Heat Loss Energy [J](Hourly)",
            9: ":Zone Infiltration Sensible Heat Gain Energy [J](Hourly)",
            10: ":Zone Infiltration Air Change Rate [ach](Hourly)",
            11: ":Zone Air System Sensible Heating Rate [W](Hourly)",
            12: ":Zone Air System Sensible Cooling Rate [W](Hourly)"
             }

    environments = ["Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)",
                   "Environment:Site Diffuse Solar Radiation Rate per Area [W/m2](Hourly)",
                   "Environment:Site Direct Solar Radiation Rate per Area [W/m2](Hourly)",
                   "Whole Building:Facility Total Produced Electricity Energy [J](Hourly)",
                   "VRF OUTDOOR UNIT:VRF Heat Pump Heating Electricity Rate [W](Hourly)",
                   "VRF OUTDOOR UNIT:VRF Heat Pump Cooling Electricity Rate [W](Hourly)",
                   "VRF OUTDOOR UNIT:VRF Heat Pump COP [](Hourly)"]


    df = pd.read_csv(output_relative_directory+r'\eplusout.csv', parse_dates=[0], index_col=[0], date_parser=parse_energyplus_datetime_string)

    column = rooms[1] + keys[11]
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df[column][48:], color='grey', linewidth=0.75)
    ax.set_xlabel('Date')
    ax.set_ylabel('Air temperature (${^o}C$)')
    plt.show()
