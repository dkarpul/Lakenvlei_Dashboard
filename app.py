import pandas as pd  # pip install pandas openpyxl
import plotly.express as px
from pyparsing import Regex  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Lakenvlei Catch Report Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_csv():
    df = pd.read_csv('data/data.csv')
    return df

df = get_data_from_csv()

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
                           min_value=int(df['Size'].min()), 
                           max_value=int(df['Size'].max()),
                           value = (int(df['Size'].min()),int(df['Size'].max())))
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
