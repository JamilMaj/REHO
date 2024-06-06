from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy.results import readhtml
import pandas as pd
import matplotlib.pyplot as plt

def read_idf(idf_file_path, idd_file_path):
    # Set the path to the IDD file
    IDF.setiddname(idd_file_path)

    # Create an IDF object and load the IDF file
    idf = IDF(idf_file_path)

    # Print the number of objects in the IDF file
    print("Number of objects in IDF file:", len(idf.idfobjects))

    idf.printidf()

def modify_idf(idf_file_path, idd_file_path):
    IDF.setiddname(idd_file_path)

    # Create an IDF object and load the IDF file
    idf = IDF(idf_file_path)

    # Add Output:Table:SummaryReports object
    idf.newidfobject('Output:Table:SummaryReports',Report_1_Name='AllSummary')
    idf.newidfobject('OutputControl:Table:Style', Column_Separator='Comma')

    # Save the modified IDF file
    idf.save('.\input_data\dsb_input_file_modified.idf')
    #return '.\input_data\dsb_input_file_modified.idf'

def run_simulation(idf_file_path, idd_file_path, weather_file_path):
    IDF.setiddname(idd_file_path)
    idf = IDF(idf_file_path, weather_file_path)
    idf.run(readvars=True,output_directory='.\output_data', annual=True)

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

def plot_results(results_file_path):
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


    df = pd.read_csv(results_file_path, parse_dates=[0], index_col=[0], date_parser=parse_energyplus_datetime_string)

    column = rooms[1] + keys[11]
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df[column][48:], color='grey', linewidth=0.75)
    ax.set_xlabel('Date')
    ax.set_ylabel('Air temperature (${^o}C$)')
    plt.show()

if __name__ == "__main__":
    # Specify path to the IDF file
    idf_file_path = ".\input_data\dsb_input_file.idf"

    # Specify path to the IDD file
    idd_file_path = r".\input_data\Energy+.idd" #  Energy+ v9.4 IDD

    # Specify path to the weather file
    weather_file_path = ".\input_data\-_FRIBOURG_MN7.epw"

    #idf_file_path_modified = modify_idf(idf_file_path, idd_file_path)

    run_simulation(idf_file_path, idd_file_path, weather_file_path)

    #results_file_path = r"C:\Users\jamil\Documents\GitHub\REHO\EnergyPlus\eplustbl.htm"  # the html file you want to read
    #filehandle = open(results_file_path, 'r').read()

    #htables = readhtml.titletable(filehandle)  # reads the tables with their titles

    # Specify path to the csv results file
    results_file_path = r".\output_data\eplusout.csv"

    plot_results(results_file_path)


