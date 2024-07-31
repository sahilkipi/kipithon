import streamlit as st
from streamlit_option_menu import option_menu
import hydralit_components as hc
import plotly.express as px
from turtle import home
import pandas as pd
import st_card_component as sc
import config
import numpy as np
from PIL import Image
import plotly.graph_objects as go

def volumetric_analysis(engine):
    st.write('###')
    z = "VOLUMETRIC ANALYSIS 📊️"
    st.markdown(f"<h2 style='text-align: center; color: #efcb68;'>{z}</h2>", unsafe_allow_html=True)
    c1_df = pd.read_sql("select * from DB_SIZE_TBL",engine)
    # st.dataframe(c1_df)
    c2_df = pd.read_sql("select * from TBL_NAME_SIZE_TBL", engine)
    # st.write(dfv)
    #st.markdown('<div style="text-align: justify;">➦ The Volumetric analysis dashboard is used to visualize schema wise large objects. The user has the flexibility to select schema name and object type.</div>',unsafe_allow_html=True)
    st.write('##')
    with st.container():
        c1,c2,c3,c4,c5,c6 =st.columns((0.4,1,0.4,1,0.4,1))
        # largest schema kpi value
        kpi1_df = c1_df.nlargest(1, 'object_size').reset_index()
        # st.dataframe(kpi1_df)
        kpi1_schema = kpi1_df['object_type'][0]
        kpi1_size=kpi1_df['object_size'][0]
        # largest table
        kpi2_df=c2_df[c2_df['object_type']=='TABLE']
        kpi2_df=kpi2_df.nlargest(1,'object_size').reset_index()
        kpi2_table = kpi2_df['object_name'][0]
        kpi2_size = kpi2_df['object_size'][0]
        # largest index
        kpi3_df = c2_df[c2_df['object_type'] == 'INDEX']
        kpi3_df = kpi3_df.nlargest(1, 'object_size').reset_index()
        kpi3_table = kpi3_df['object_name'][0]
        kpi3_size = kpi3_df['object_size'][0]
        with c1:
            st.image(Image.open('Dashboard_icons/scheme.png'),use_column_width=True)
        with c2:
            st.write('#####')
            st.metric('Largest Schema',kpi1_schema,int(kpi1_size))

        with c3:
            st.image(Image.open('Dashboard_icons/future_state_table.png'), use_column_width=True)
        with c4:
            st.write('#####')
            st.metric('Largest Table',kpi2_table,int(kpi2_size))

        with c5:
            st.image(Image.open('Dashboard_icons/future_state_idx.png'), use_column_width=True)
        with c6:
            st.write('#####')
            st.metric('Largest Index',kpi3_table,int(kpi3_size))




    st.write('##')
    with st.container():
        with st.spinner('Updating Report...'):
            with st.expander('Click here to show/hide the filters'):
                left_column, right_column = st.columns((1.5, 1.5))

                # schema filter
                with left_column:
                    sc_option = c1_df["object_type"].unique().tolist()
                    sc_option.insert(0, 'ALL')
                    sc_select = st.multiselect('Select a schema name', sc_option, default='ALL')
                    # df_sc= dfv[dfv["schema_name"]==sc_select]

                # object type filter
                with right_column:
                    obj_option = c2_df['object_type'].unique().tolist()
                    obj_option.insert(0, 'ALL')
                    # schema_option.insert(0,'ALL')
                    obj_select = st.multiselect('Select Object type', obj_option, default='ALL')

            left_column, right_column = st.columns((1.5, 1.5))
            # schema name with size
            with left_column:
                if sc_select == ['ALL']:
                    df_sc=c1_df
                else:
                    df_sc = c1_df[c1_df["object_name"].isin(sc_select)]
                    #st.dataframe(df_sc)
                z = "Top large schemas"
                st.markdown(f"<h4 style='text-align: center; color: #efcb68;'>{z}</h4>", unsafe_allow_html=True)
                fig = px.bar(df_sc, x='object_type',y='object_size', width=800, height=500, orientation='v')
                fig.update_traces(marker_color='#d9dbf1')
                fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                fig.update_xaxes(gridcolor='#2d545e')
                fig.update_yaxes(gridcolor='#2d545e')
                fig.update_layout(title_x=0, margin=dict(l=0, r=10, b=10, t=30), yaxis_title="SCHEMA SIZE",
                                  xaxis_title="SCHEMA NAME", title="")
                st.plotly_chart(fig, use_container_width=True)

            # object name with size
            with right_column:
                if sc_select ==['ALL'] and obj_select==['ALL']:
                    df_obj=c2_df
                elif sc_select==['ALL'] and obj_select!=['ALL']:
                    df_obj = c2_df[c2_df["object_type"].isin(obj_select)]
                elif sc_select!=['ALL'] and obj_select==['ALL']:
                    df_obj = c2_df[c2_df["schema_name"].isin(sc_select)]
                else:
                    df_obj=c2_df[c2_df["schema_name"].isin(sc_select) & c2_df["object_type"].isin(obj_select)]

                z = "Top Large Objects "
                st.markdown(f"<h4 style='text-align: center; color: #efcb68;'>{z}</h4>", unsafe_allow_html=True)
                df_obj = df_obj.sort_values(by=['object_size'], ascending=False)
                fig = px.bar(df_obj, x='object_name', y='object_size', width=800, height=500, orientation='v',
                             hover_data=['object_name','object_type','object_size'])
                fig.update_traces(marker_color='#d9dbf1') #22EEF1
                fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                fig.update_xaxes(gridcolor='#2d545e',showticklabels=False)
                fig.update_yaxes(gridcolor='#2d545e')
                #fig.update_layout(xaxis_tickangle=30)
                fig.update_layout(title_x=0, margin=dict(l=0, r=10, b=10, t=30), yaxis_title="OBJECT SIZE",
                                  xaxis_title="OBJECT NAME", title="")
                st.plotly_chart(fig, use_container_width=True)


#volumetric()

