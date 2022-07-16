import pandas as pd  # pip install pandas openpyxl
import plotly.express as px
from pyparsing import Regex  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Lakenvlei Catch Report Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
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

@st.cache
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

@st.cache
def get_youth_nats(session):
    df = pd.read_excel(
            io='Data/Session' + str(session) + ' copy.xlsx',
            engine="openpyxl",
            sheet_name="Scores"
        )
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

@st.cache
def get_data_from_excel():
    WPFFA_2022 = get_wp_trials_data("Data/WPFFA Trial Results 2022-2023 V1.xlsx","WP Trials 2022")
    WPFFA_2021 = get_wp_trials_data("Data/WPFFA Trial Results 2021-2022 V4.xlsx","WP Trials 2021")
    Youth_Nats =  get_youth_nats_all()
    BOL_2022 = get_bol_trials_data()
    df = pd.concat([WPFFA_2022,WPFFA_2021,Youth_Nats,BOL_2022])
    df['Size'] = df['Size'].astype(float)
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
chosen_events = st.sidebar.multiselect(
    "Select Events:",
    options=df["Event"].unique(),
    default=df["Event"].unique()
)
normalisation = st.sidebar.radio(
     "Normalisation:",
     ('Count', 'Percent'))

if normalisation == 'Count':
    normmode = None
else:
    normmode = 'percent'
stack = st.sidebar.radio(
     "Stack Results?",
     ('Stack', 'Group'))
df_events = df.query(
    "Event == @chosen_events"
)
if stack == 'Stack':
    barmode = 'stack'
else:
    barmode = 'group'
# ---- MAINPAGE ----
st.title(":bar_chart: Lakenvlei Catch Reports")
st.markdown("###")
size_selection = st.sidebar.slider('Size:',
                           min_value=(df['Size'].min()), 
                           max_value=df['Size'].max(),
                           value = (df['Size'].min(),df['Size'].max()))
st.markdown("###")
mask = df_events['Size'].between(*size_selection)
fig_projections = px.histogram(
    df_events[mask],
    x="Size",
    orientation="v",
    color="Event",
    template="plotly_white",
    barmode=barmode,
    histnorm = normmode,
    color_discrete_sequence =px.colors.qualitative.D3
)
#fig_projections.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
fig_projections.update_xaxes(dtick = 20)
st.plotly_chart(fig_projections, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
