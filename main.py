import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import altair as alt
from supabase import create_client, Client
from utils import *
from plot_data import *

st.set_page_config(layout="wide",
                   page_title='KPI Dashboard 📈',
                   page_icon='📊',
                   initial_sidebar_state='collapsed')
st.markdown("""
            <style>
            .big-font {
                font-size:85px !important;
            }
            </style>
            """, unsafe_allow_html=True)
st.markdown("""
            <style>
            .small-font {
                font-size:25px !important;
            }
            </style>
            """, unsafe_allow_html=True)
st.markdown("""
            <style>
            .med-green-font {
                color:Green;
                font-size:30px !important;
            }
            </style>
            """, unsafe_allow_html=True)
st.markdown("""
            <style>
            .med-red-font {
                color:Red;
                font-size:30px !important;
            }
            </style>
            """, unsafe_allow_html=True)


def select_circle():
    circles = pd.DataFrame(query_circle().data)
    circle = st.sidebar.selectbox(label = "Choose a circle",
                          options = circles['Name'])
    
    id = circles.loc[circles['Name']==circle]['id'].unique()[0]

    return id


def dashboard(circle_id):
    st.header("Time series of chosen KPIs")
    kpis_ori = query_kpi(circle_id).data
    names = [kpi['Name'] for kpi in kpis_ori]

    chosen = st.multiselect("Choose KPIs for line chart", 
                            names, default=names)
    kpis = []

    for kpi in kpis_ori:
        if kpi["Name"] in chosen:
            kpis.append(kpi)

    data = generate_linechart(kpis[0]["id"], (2023,1), (2023,8), alltime=True)

    start = st.selectbox(label = "time from",
                          options = data["Time"])
    ind = data.index[data["Time"] == start]
    end = st.selectbox(label = "time to",
                          options = data[data.index > ind[0]]["Time"])
    
    show_table = st.checkbox("Show table")
    
    cols = st.columns(len(kpis))
    
    for k, kpi in enumerate(kpis):
        with cols[k]:
            st.subheader(kpi["Name"])

            curr_val, curr_growth = key_stats(kpi["id"])

            subcol1, subcol2 = st.columns(2)

            with subcol1:
                st.markdown(f"""<p class="small-font">Current value</p>""", 
                            unsafe_allow_html=True)
                st.markdown(f"""<p class="big-font">{curr_val}</p>""", 
                            unsafe_allow_html=True)
            
            with subcol2:
                st.markdown(f"""<p class="med-red-font"> </p>""", 
                            unsafe_allow_html=True)
                st.markdown(f"""<p class="small-font"> </p>""", 
                            unsafe_allow_html=True)
                st.write("Current growth rate")
                if curr_growth > 0:
                    growth_str = str(round(curr_growth, 1)) + "%"
                    st.markdown(f"""<p class="med-green-font">&#10506;{growth_str}</p>""", 
                                unsafe_allow_html=True)
                else:
                    growth_str = str(round(abs(curr_growth), 1)) + "%"
                    st.markdown(f"""<p class="med-red-font">&#10507;{growth_str}</p>""", 
                                unsafe_allow_html=True)
            

            data = generate_linechart(kpi["id"], 
                                    timefrom=invert_xlabel(start), 
                                    timeto=invert_xlabel(end))
            
            options = {
            "xAxis": {
            "type": "category",
            "data": list(data["Time"]),
            },
            "yAxis": {"type": "value"},
            "series": [
                {"data": list(data["Value"]), "type": "line"}
                ],
            }
            st_echarts(options=options)
        
            if show_table:
                st.dataframe(data.loc[:, ["Time", "Value"]], hide_index=True)


    st.divider()
    st.header("Current growth rate of all KPIs")

    bar = generate_barchart(kpis_ori)
    st.bar_chart(bar, x="KPI", y="growth rate")


    st.divider()
    st.header("Annual growth rate of all KPIs")
    st.write("to be implemented")
    # years = st.multiselect("Choose years", [2022, 2023], default=[2022, 2023])
    # multibar = generate_multibarchart(kpis, years=years)
    # st.bar_chart(multibar, x="KPI", y="annual growth", color="years")


cid = select_circle()
dashboard(cid)

