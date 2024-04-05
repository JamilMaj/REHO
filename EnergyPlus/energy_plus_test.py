import os


def run_energyplus(idf_file_path, weather_file_path):
    # Check if IDF and weather file paths exist
    if not os.path.isfile(idf_file_path):
        print(f"IDF file '{idf_file_path}' not found.")
        return
    if not os.path.isfile(weather_file_path):
        print(f"Weather file '{weather_file_path}' not found.")
        return

    # Run EnergyPlus simulation
    idf_file_name = os.path.basename(idf_file_path)
    weather_file_name = os.path.basename(weather_file_path)

    energyplus_exe = r"C:\EnergyPlusV23-2-0\energyplus.exe"  # Adjust the path if necessary
    if not os.path.isfile(energyplus_exe):
        print("EnergyPlus executable not found. Please make sure EnergyPlus is installed and accessible.")
        return

    command = f"{energyplus_exe} -r -w \"{weather_file_name}\" \"{idf_file_name}\""
    print(f"Running EnergyPlus simulation: {command}")

    os.system(command)


if __name__ == "__main__":
    # Specify paths to IDF and weather files
    idf_file_path = r"C:\EnergyPlusV23-2-0\ExampleFiles\BasicsFiles\Exercise1A.idf"
    weather_file_path = r"C:\EnergyPlusV23-2-0\WeatherData\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"

    # Call function to run EnergyPlus simulation
    run_energyplus(idf_file_path, weather_file_path)

