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


def temperature_analysis(engine):
    z = "TEMPERATURE ANALYSIS 🌡️"
    st.markdown(f"<h2 style='text-align: center; color: #efcb68;'>{z}</h2>", unsafe_allow_html=True)
    st.write('##')
    query = """select db_name as database_name, table_name, count(table_name) as table_count, sum(exec_count) as access_count from SAMPLE_DB.REPORTING.ACCESS_COUNT_TBL where table_type = 'BASE TABLE' group by 1, 2 order by 4 desc"""
    df = pd.read_sql(query, engine)
    # st.dataframe(df)
    #dim_dba_tables table is replaced with table_types_in_mysql
    #table_types_in_mysql it should be in transform layer
    tables_df=pd.read_sql("""select * from table_types_in_mysql where table_type='BASE TABLE'""",engine)
    # KPI's
    with st.container():
        c0, c1, c2, c3, c4, c5, c6 = st.columns((0.4, 0.4, 1, 0.4, 1, 0.4, 1))
        # kpi1
        kpi1_df = df.nlargest(1, 'access_count').reset_index()
        most_accessed_table = kpi1_df['table_name'][0]
        most_access_count = kpi1_df['access_count'][0]
        kpi2_df = df.nsmallest(1,'access_count').reset_index()
        least_accessed_table = kpi2_df['table_name'][0]
        least_access_count = kpi2_df['access_count'][0]
        accessed_tables_count=df.shape[0]
        total_tables_count=tables_df.shape[0]

        with c1:
            st.image(Image.open('Dashboard_icons/hot_table.png'),use_column_width=True)
        with c2:
            st.write('#####')
            st.metric('Most Accessed Table', most_accessed_table, int(most_access_count))
        with c3:
            st.image(Image.open('Dashboard_icons/cold_table.png'),use_column_width=True)
        with c4:
            st.write('#####')
            st.metric('Least Accessed Table', least_accessed_table, int(least_access_count))
        with c5:
            st.image(Image.open('Dashboard_icons/accessed_tables.png'),
                use_column_width=True)
        with c6:
            st.write('#####')
            st.metric('Total Accessed tables', str(accessed_tables_count)+ '/' + str(total_tables_count), int(total_tables_count)-int(accessed_tables_count))

    st.write('##')

    with st.expander('Click here to show/hide filters'):
        with st.container():
            with st.spinner('Updating Report...'):
                # left_column, right_column = st.columns((1.5, 1.5))

                # filter for database
                # with left_column:
                db_option = df["database_name"].unique().tolist()
                db_option.insert(0, 'ALL')
                selected_db = st.multiselect('Select a database name', db_option, default='adventureworks2014')

                # filter for schema
                # with right_column:
                #     schema_option = df['schema_name'].unique().tolist()
                #     schema_option.insert(0, 'ALL')
                #     selected_schema = st.multiselect('Select a schema name', schema_option, default='ALL')

                if selected_db == ['ALL']:
                    df_filtered = df
                elif selected_db != ['ALL']:
                    df_filtered = df[df['database_name'].isin(selected_db)]

        with st.container():
            l1, l2, r1, r2 = st.columns(4)
            with l1:
                hot_limit = st.number_input('Enter the limit for hot tables', value=2000, step=100, format='%i')
            with l2:
                warm_limit = st.number_input('Enter the limit for warm tables', value=1000, step=100, format='%i')
            with r1:
                cold_limit = st.number_input('Enter the limit for cold tables', value=200, step=100, format='%i')
            with r2:
                top_n = st.number_input('Enter the value for N', value=10, step=1, format='%i')


    st.write('##')

    with st.container():
        g1, g2, g3 = st.columns((1, 1, 1))

        # hot table
        with g1:
            hot_df = df_filtered[df_filtered['access_count'] >= hot_limit].nlargest(int(top_n),'access_count')
            z = "Top {} Hot Tables".format(int(top_n))
            st.markdown(f"<h4 style='text-align: center; color: white;'>{z}</h4>", unsafe_allow_html=True)

            hot_fig = px.bar(hot_df, x='table_name', y='access_count', width=800, height=500,
                         hover_data=['database_name','table_name','access_count'])
            hot_fig.update_traces(marker_color='#E93030')
            hot_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
            hot_fig.update_xaxes(gridcolor='#2d545e', showticklabels=False)
            hot_fig.update_yaxes(gridcolor='#2d545e')
            #fig.update_layout(xaxis=go.layout.XAxis(tickangle=90))
            hot_fig.update_layout(title_x=0, margin=dict(l=0, r=10, b=10, t=30), yaxis_title="ACCESS COUNT",xaxis_title="TABLE NAME",
                                  title="Bar Chart for Hot Tables")
            #st.dataframe(hot_df)
            st.plotly_chart(hot_fig,use_container_width=True)

        with g2:
            warm_df = df_filtered[(df_filtered['access_count'] >= warm_limit) & (df_filtered['access_count'] < hot_limit)].nlargest(int(top_n),'access_count')
            z = "Top {} Warm Tables".format(int(top_n))
            st.markdown(f"<h4 style='text-align: center; color: white;'>{z}</h4>", unsafe_allow_html=True)

            warm_fig = px.bar(warm_df, x='table_name', y='access_count', width=800, height=500,
                         hover_data=['database_name', 'table_name', 'access_count'])
            warm_fig.update_traces(marker_color='#E99930')
            warm_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
            warm_fig.update_xaxes(gridcolor='#2d545e', showticklabels=False)
            warm_fig.update_yaxes(gridcolor='#2d545e')
            # fig.update_layout(xaxis=go.layout.XAxis(tickangle=90))
            warm_fig.update_layout(title_x=0, margin=dict(l=0, r=10, b=10, t=30), yaxis_title="ACCESS COUNT",
                              xaxis_title="TABLE NAME", title="Bar Chart for Warm Tables")
            # st.dataframe(hot_df)
            st.plotly_chart(warm_fig, use_container_width=True)

        with g3:
            cold_df= df_filtered[(df_filtered['access_count'] >= cold_limit) & (df_filtered['access_count'] < warm_limit)].nlargest(int(top_n),'access_count')
            z = "Top {} Cold Tables".format(int(top_n))
            st.markdown(f"<h4 style='text-align: center; color: white;'>{z}</h4>", unsafe_allow_html=True)

            cold_fig = px.bar(cold_df, x='table_name', y='access_count', width=800, height=500,
                         hover_data=['database_name', 'table_name', 'access_count'],
                         color_continuous_scale=px.colors.sequential.Teal)
            #fig.update_traces(marker_color='#d9dbf1')
            cold_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
            cold_fig.update_xaxes(gridcolor='#2d545e', showticklabels=False)
            cold_fig.update_yaxes(gridcolor='#2d545e')
            # fig.update_layout(xaxis=go.layout.XAxis(tickangle=90))
            cold_fig.update_layout(title_x=0, margin=dict(l=0, r=10, b=10, t=30), yaxis_title="ACCESS COUNT",
                              xaxis_title="TABLE NAME", title="Bar Chart for Cold Tables")
            # st.dataframe(hot_df)
            st.plotly_chart(cold_fig, use_container_width=True)

    with st.expander('Click here to view/download top priority tables for migration'):
        with st.container():
            top_priority = pd.read_sql("""select db_name as database_name, table_name, count(table_name) as table_count, sum(exec_count) as access_count from ACCESS_COUNT_TBL where table_type = 'BASE TABLE' group by 1, 2 order by 4 desc limit 20""", engine)
            with st.container():
                with st.container():
                    c1, c2, c3, c4 = st.columns((1.2, 0.7, 1, 1))
                    with c1:
                        st.subheader('List of top priority tables(Top 20)')
                    with c2:
                        st.download_button(
                            label="Download data as CSV",
                            data=top_priority.to_csv(index=False).encode('utf-8'),
                            file_name='./Top_priority_tables.csv',
                            mime='text/csv'
                        )

                top_priority.columns = ['DATABASE_NAME', 'TABLE_NAME', 'TABLE_COUNT', 'ACCESS_COUNT']
                fig = go.Figure(data=[go.Table(
                    columnorder=[1, 2, 3, 4],
                    columnwidth=[70, 60, 50, 70],
                    header=dict(
                        values=['<b>DATABASE_NAME<b>', '<b>TABLE_NAME<b>', '<b>TABLE_COUNT<b>', '<b>ACCESS_COUNT<b>'],
                        font=dict(size=15, color='black'),
                        fill_color='#94B49F',
                        line_color='#2d545e',
                        align='left',
                        height=25
                    ),
                    cells=dict(values=top_priority.transpose().values.tolist(),
                               font=dict(family='century gothic', size=15, color='black'),
                               fill_color='#CEE5D0',
                               line_color='#2d545e',
                               align='left',
                               height=30)
                )
                ])
                fig.update_layout(title_x=0, margin=dict(l=0, r=0, b=0, t=30), width=220, height=700, title="")
                st.plotly_chart(fig, use_container_width=True)


#temperature()