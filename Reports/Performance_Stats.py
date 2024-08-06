import streamlit as st
from streamlit_option_menu import option_menu
import hydralit_components as hc
import plotly.express as px
from turtle import home
import pandas as pd
import st_card_component as sc
import numpy as np
import plotly.graph_objects as go
from PIL import Image

def performance_stats(engine):

    z= "PERFORMANCE STATS 📉"
    st.markdown(f"<h2 style='text-align: center; color: #efcb68;'>{z}</h2>", unsafe_allow_html=True)

    df=pd.read_sql("select * from DAILY_HOST_SUMMARY",engine)
    st.dataframe(df)
    df['report_date']=pd.to_datetime(df['report_date'], format="%d-%m-%Y")
    #st.write(df_sam)

    #COMBINED WIP
    # fig = px.line(df, x='report_date', y='statements', markers=True, height=400, title= "Aggregated performance stats")
    # fig.update_xaxes(gridcolor='#2d545e')  # showticklabels=False,visible=False
    # fig.update_yaxes(gridcolor='#2d545e')
    # st.plotly_chart(fig, use_container_width=True)

    #Statement counts
    cpu_fig = px.line(df, x='report_date', y='statements',markers=True,height=400, title ="Statements executed over time")
    cpu_fig.update_xaxes(gridcolor='#2d545e') #showticklabels=False,visible=False
    cpu_fig.update_yaxes(gridcolor='#2d545e')
    st.plotly_chart(cpu_fig,use_container_width=True)

    #Table Scans
    io_fig = px.line(df, x='report_date', y='table_scans', markers=True, height=400, title ="Table scans over time")
    io_fig.update_xaxes(gridcolor='#2d545e')  # showticklabels=False,visible=False
    io_fig.update_yaxes(gridcolor='#2d545e')
    st.plotly_chart(io_fig, use_container_width=True)

    #TOTAL KB
    # bytes_fig = px.line(df, x='date', y='total_kb', markers=True, height=400, title ="Total KB of data processed over time")
    # bytes_fig.update_xaxes(gridcolor='#2d545e')  # showticklabels=False,visible=False
    # bytes_fig.update_yaxes(gridcolor='#2d545e')
    # st.plotly_chart(bytes_fig, use_container_width=True)

    # #QUERY COUNT
    # query_fig = px.line(df, x='date', y='query_count', markers=True, height=400, title ="Query count over time")
    # query_fig.update_xaxes(gridcolor='#2d545e')  # showticklabels=False,visible=False
    # query_fig.update_yaxes(gridcolor='#2d545e')
    # st.plotly_chart(query_fig, use_container_width=True)

#performance_stats()