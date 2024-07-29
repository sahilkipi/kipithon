import streamlit as st
from streamlit_option_menu import option_menu
import hydralit_components as hc
import plotly.express as px
from turtle import home
import pandas as pd
import st_card_component as sc
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from annotated_text import annotated_text

'''
st.set_page_config(
    page_title="Summary Report",
    page_icon="👋", layout='wide'
)
'''

def summary_report(engine):
    # creating engine for snowflake
    # heading
    #z = "SUMMARY REPORT 📑"
    #st.markdown(f"<h2 style='text-align: center; color: #efcb68;'>{z}</h2>", unsafe_allow_html=True)
    st.write('###')
    # database information
    d = "DATABASE DETAILS"
    st.markdown(f"<h3 style='text-align: center; color: #efcb68;'>{d}</h3>", unsafe_allow_html=True)
    #st.markdown("<h3 style='text-align: center; color: white;'>" + str(annotated_text(('Database details','','#12343b'))) + "</h3>",unsafe_allow_html=True)
    inv_df = pd.read_csv('Schema_object_overview.csv', header=1)
    ver = str("MySQL Standard Edition 8.0.38")
    Us = '500'  #float(inv_df['Used_Space(MB)'])
    fs = '700'  #float(inv_df["Free_Space(MB)"])

    st.write("##")

    placeholder = st.empty()
    with placeholder.container():
        zeroth_column,first_column, sec_column, thr_column, fourth_column, five_column, six_column = st.columns(
            (0.6, 0.6, 1.4, 0.6, 1.4, 0.6, 1.4))

        # database image
        with first_column:
            image=Image.open('Dashboard_icons\database-blue.png')
            st.image(image, caption=None, width=100, use_column_width=True, clamp=False, channels="RGB",
                     output_format="auto")

        # database version details
        with sec_column:
            st.subheader("Version ")
            # st.subheader(f"{ver}")
            st.markdown(f"<h5 style='text-align: left; color: #C0DD81;'>{ver}</h5>", unsafe_allow_html=True)

        # used space image
        with thr_column:
            image=Image.open('Dashboard_icons\pie-chart.png')
            st.image(image, caption=None, width=120, use_column_width=True, clamp=False, channels="RGB",
                     output_format="auto")

        # used space details
        with fourth_column:
            st.subheader("Used Space ")
            # st.subheader(f"{Us}")
            st.markdown(f"<h5 style='text-align: left; color: #C0DD81;'> MB: {Us}</h5>", unsafe_allow_html=True)

        ##free space image
        with five_column:
            image=Image.open('Dashboard_icons\pie-chart-2.png')
            st.image(image,caption=None, width=120, use_column_width=True, clamp=False, channels="RGB",
                     output_format="auto")

        # free space details
        with six_column:
            st.subheader("Free Space ")
            # st.subheader(f"{fs}")
            st.markdown(f"<h5 style='text-align: left; color: #C0DD81;'> MB: {fs}</h5>", unsafe_allow_html=True)
        st.write("---")

        # objects information
        z = "OBJECT DETAILS"
        st.markdown(f"<h3 style='text-align: center; color: #efcb68;'>{z}</h3>", unsafe_allow_html=True)
        st.write("###")
        kpi0, kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns((0.6, 0.6, 1.4, 0.6, 1.4, 0.6, 1.4))

        inv_df_obj = pd.read_sql("select * from db_object_overview",engine)

        # st.dataframe(inv_df_obj)
        #st.write(inv_df_obj.columns)
        # storing count
        inv_df_tbc = inv_df_obj.loc[inv_df_obj['object_type'] == 'BASE TABLE', 'count'].sum()
        inv_df_v = inv_df_obj.loc[inv_df_obj['object_type'] == 'VIEW', 'count'].sum()
        inv_df_p = inv_df_obj.loc[inv_df_obj['object_type'] == 'PROCEDURE', 'count'].sum()

        # table image
        with kpi1:
            image=Image.open(r"Dashboard_icons\future_state_table.png")
            st.image(image, caption=None, width=120, use_column_width=True, clamp=False, channels="RGB",
                     output_format="auto")

        # table count
        with kpi2:
            # hc.info_card(title='Total Table Count ⬇', content=a, bar_value=12)
            st.subheader("Tables ")
            # st.subheader(f"{inv_df_tbc}")
            st.markdown(f"<h5 style='text-align: left; color: #87CEEB;'> Count: {inv_df_tbc}</h5>", unsafe_allow_html=True)

        # view image
        with kpi3:
            image=Image.open(r'Dashboard_icons\visualization.png')
            st.image(image, caption=None, width=120, use_column_width=True, clamp=False, channels="RGB",
                     output_format="auto")

        # view count
        with kpi4:
            st.subheader("Views ")
            # st.subheader(f"{inv_df_v}")
            st.markdown(f"<h5 style='text-align: left; color: #87CEEB;'> Count: {inv_df_v}</h5>", unsafe_allow_html=True)

        # procedure image
        with kpi5:
            image=Image.open('Dashboard_icons\db_sp.png')
            st.image(image, caption=None, width=120, use_column_width=None, clamp=False, channels="RGB",
                     output_format="auto")

            # procedure count
        with kpi6:
            st.subheader("Procedures ")
            # st.subheader(f"{inv_df_p}")
            st.markdown(f"<h5 style='text-align: left; color: #87CEEB;'> Count: {inv_df_p}</h5>", unsafe_allow_html=True)

        st.write('##')

        kpi0, kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns((0.6, 0.6, 1.4, 0.6, 1.4, 0.6, 1.4))
        # storing count
        inv_df_f = inv_df_obj.loc[inv_df_obj['object_type'] == 'FUNCTION', 'count'].sum()
        inv_df_s = inv_df_obj.loc[inv_df_obj['object_type'] == 'SEQUENCE', 'count'].sum()
        inv_df_i = inv_df_obj.loc[inv_df_obj['object_type'] == 'INDEX', 'count'].sum()

        # function image
        with kpi1:
            image=Image.open(r'Dashboard_icons\fx.png')
            st.image(image, caption=None, width=120, use_column_width=True, clamp=False, channels="RGB",
                     output_format="auto")

        # function count
        with kpi2:
            st.subheader("Fuctions ")
            # st.subheader(f"{inv_df_f}")
            st.markdown(f"<h5 style='text-align: left; color: #87CEEB;'> Count: {inv_df_f}</h5>", unsafe_allow_html=True)

        # sequence image
        with kpi3:
            image=Image.open('Dashboard_icons\db_seq.png')
            st.image(image, caption=None, width=100, use_column_width=True, clamp=False, channels="RGB",
                     output_format="auto")

        # sequence count
        with kpi4:
            st.subheader("Sequences ")
            # st.subheader(f"{inv_df_s}")
            st.markdown(f"<h5 style='text-align: left; color: #87CEEB;'> Count: {inv_df_s}</h5>", unsafe_allow_html=True)

        # index image
        with kpi5:
            image=Image.open(r'Dashboard_icons\future_state_idx.png')
            st.image(image, caption=None, width=120, use_column_width=True, clamp=False, channels="RGB",
                     output_format="auto")

        # index count
        with kpi6:
            st.subheader("Indexes ")
            # st.subheader(f"{inv_df_i}")
            st.markdown(f"<h5 style='text-align: left; color: #87CEEB;'>Count: {inv_df_i}</h5>", unsafe_allow_html=True)


#summary()