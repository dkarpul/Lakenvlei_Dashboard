import pandas as pd  # pip install pandas openpyxl
def get_wp_trials_data(fname,Event):
    df = pd.read_excel(
            io=fname,
            engine="openpyxl",
            sheet_name="Stillwater"
        )
    df = df.filter(regex = r'^(Angler|Fish).*')
    df = pd.melt(df, id_vars = ['Angler'],var_name = 'Fish No', value_name='Size')
    df = df.dropna(subset=['Size'])
    df = df.dropna(subset=['Angler'])
    df['Event'] = Event
    return df

def get_bol_trials_data():
    df = pd.read_excel(
            io="Data/Boland_trials_2022.xlsx",
            engine="openpyxl",
            sheet_name="Sheet1"
        )
    df = df.dropna(subset=['Size'])
    df = df.drop(columns=['Dataset','Year'])
    df['Size'] = df['Size']*10
    df['Event'] = 'BOL Trials 2022'
    return df

def get_youth_nats(session):
    df = pd.read_excel(
            io='Data/Session' + str(session) + ' copy.xlsx',
            engine="openpyxl",
            sheet_name="Scores"
        )
    df = df[df['Sector']==1]
    df = df.filter(regex = r'^(Team|Fish).*')
    df = pd.melt(df, id_vars = ['Team'],var_name = 'Fish No', value_name='Size')
    df = df.dropna(subset=['Size'])
    df = df.dropna(subset=['Team'])
    df['Angler'] = df['Team']
    df = df.drop(columns=['Team'])
    df['Event'] = 'Youth Nationals 2021'
    return df

def get_youth_nats_all():
    df = pd.DataFrame()
    for x in range(5):
        df = pd.concat([df,get_youth_nats(x+1)])
    return df

def get_data_from_excel():
    WPFFA_2022 = get_wp_trials_data("Data/WPFFA Trial Results 2022-2023 V1.xlsx","WP Trials 2022")
    WPFFA_2021 = get_wp_trials_data("Data/WPFFA Trial Results 2021-2022 V4.xlsx","WP Trials 2021")
    Youth_Nats =  get_youth_nats_all()
    BOL_2022 = get_bol_trials_data()
    df = pd.concat([WPFFA_2022,WPFFA_2021,Youth_Nats,BOL_2022])
    df['Size'] = df['Size'].astype(float)
    return df

df = get_data_from_excel()
df.to_csv('data/data.csv')
