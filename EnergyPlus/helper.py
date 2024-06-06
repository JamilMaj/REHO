import pandas as pd

def parse_energyplus_datetime_string(st, year=2021):
    st = st.strip()
    month = int(st[0:2])
    day = int(st[3:5])
    hour = int(st[7:9])
    minute = int(st[10:12])
    second = (st[13:15])
    if not hour == 24:
        dt = pd.Timestamp(year, month, day, hour, minute)
    else:
        hour = 0
        dt = pd.Timestamp(year, month, day, hour, minute)
        dt += pd.Timedelta('1 day')
    return dt


def extract_U_factor(results_path=r'output_data\idf1_tbl.htm'):
    # read EPlus results as html
    df = pd.read_html(results_path, header=0)
    # detect indices where "U-Factor" appears
    indices = []
    numerator = 0
    denominator = 0
    for idx, tables in enumerate(df):
        # Check if "U-factor" appears in the column names
        if any(isinstance(col, str) and 'U-Factor' in col for col in tables.columns):
            # If found, save the table index
            indices.append(idx)
    # extract summary table related to CELLS walls

    # !!! Hardcoded
    df_ufactor = pd.DataFrame(df[32])

    # recompute averaged U-factor
    numerator = numerator + ((df_ufactor['U-Factor with Film [W/m2-K]'] * df_ufactor['Gross Area [m2]']).sum())
    denominator = denominator + df_ufactor['Gross Area [m2]'].sum()
    U_factor = numerator / denominator
    # convert to W -> kW
    return U_factor / 1000, indices


def modify_setpoint(idf, new_setpoint, name_SIA, modified_hours=list(range(9, 18)), verbose='q'):
    for entity in idf.idfobjects:
        for field in idf.idfobjects[entity]:
            if 'Name' in field.objls:  # check field with names only
                if name_SIA in field.Name:  # modify fields where modified SIA file appears
                    for hours in modified_hours:
                        # if hours in modified_hours:
                        # Replace the value with new setpoint
                        setattr(field, f"Value_{hours}", new_setpoint)
                    if verbose != 'q':
                        print(field)


def modify_capacity(new_capacity):
    print(new_capacity)