import streamlit as st
import hashlib
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import hydralit_components as hc
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import time
from Reports.Summary_Report import summary_report
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from email.message import EmailMessage
import smtplib

connection_parameters = {
 "user": st.secrets['DB_USER'],
 "password": st.secrets['DB_PASSWORD'],
 "account": st.secrets['DB_ACCOUNT'],
 "role": st.secrets['DB_ROLE'],
 "warehouse": st.secrets['DB_WAREHOUSE'],
 "database": st.secrets['DB_NAME'],
 "schema": st.secrets['DB_SCHEMA'],
 } 

def lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

homepage_lt = lottie_url('https://assets4.lottiefiles.com/packages/lf20_qp1q7mct.json')
use_case_3 = lottie_url('https://assets1.lottiefiles.com/packages/lf20_ko8ud57v.json')
inv_col= lottie_url('https://assets5.lottiefiles.com/packages/lf20_kpoaosqz.json')

# Create a Snowflake session
session = Session.builder.configs(connection_parameters).create()

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load credentials from Snowflake
def load_credentials():
    credentials_df = session.table("credentials").collect()
    credentials = {row['USERNAME']: {
                        "name": row['NAME'], 
                        "password": row['PASSWORD'], 
                        "email": row['EMAIL']
                        } for row in credentials_df}
    return credentials

# Function to check if user exists
def user_exists(username):
    return session.table("credentials").filter(col("USERNAME") == username).count() > 0

# Function to save a new user to Snowflake
def save_user(username, name, password, email):
    try:
        hashed_password = hash_password(password)
        session.sql(f"""
                INSERT INTO credentials (USERNAME, NAME, PASSWORD, EMAIL)
                VALUES ('{username}', '{name}', '{hashed_password}', '{email}')
        """).collect()
    except Exception as e:
        st.warning(f"Error: {str(e)}")

# Function to update user password in Snowflake
def update_password(username, new_password):
    hashed_password = hash_password(new_password)
    session.sql(f"""
        UPDATE credentials
        SET PASSWORD = '{hashed_password}'
        WHERE USERNAME = '{username}'
    """).collect()

def main():
    st.set_page_config(
        page_title="Pre-Migration Assistant",
        page_icon=":wave:", layout='wide'
    )

    # Load credentials
    credentials = load_credentials()

    # Streamlit UI
    st.title("Kipithon - Database Pre-migration Assistant 🤖")
    

    # Session state to keep track of login status
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'reset_user' not in st.session_state:
        st.session_state.reset_user = None
        

    if st.session_state.logged_in:
        with hc.HyLoader('Loading Application...',hc.Loaders.standard_loaders,index=5):
            time.sleep(5)

        time.sleep(5)
        menu_data = [
                {'icon': "bi bi-house-fill", 'label': "Home"},
                {'icon': "far fa-chart-bar", 'label': "Analysis"},
                {'icon': "bi bi-journals", 'label': "Services"},
                {'icon': "email", 'label':"Feedback Form"}
            ]
        over_theme = {'txc_inactive': '#FFFFFF'}
        menu_id = hc.option_bar(option_definition=menu_data,override_theme=over_theme,horizontal_orientation=True)

        if menu_id == 'Home':
                #Intro section
                with st.container():
                    st.subheader('Welcome to Pre Migration Assistant 👋')
                    left_column, right_column = st.columns((2, 1))
                    with left_column:
                        st.write("""In today's world, With the advent of cloud, organizations are now migrating their data and workloads to cloud. Data Warehouses and associated analytics are large, complex and dynamic. Gartner indicates that most data warehouse cloud migrations are not well executed, resulting in costly delays, unexpected problems, and disappointed business customers. Before you migrate to the cloud it’s critical to know the profile of your data warehouse usage and identify the migration inhibitors common in legacy data warehouses. Our solution aims at the following""")
                        st.write('➦  Automate the process of inventory collection using a metadata driven approach')
                        st.write('➦  Cleanup the data landscape by identifying scarcely used tables through a metadata based approach.')
                        st.write('➦  Derive table usage pattern and prioritize tables for migration based on their access count.')
                    with right_column:
                        st_lottie(homepage_lt, height=200, key='Intro-1')

                st.write('---')
                #Our approach - Inventory collection
                with st.container():
                    left,right=st.columns((1,2))
                    with left:
                        st.header('Our approach ✅')
                        st.subheader('1) Inventory collection')
                        st.markdown('<div style="text-align: justify;">➦ Pre migartion assistant interrogates metadata and development code which has accumulated over the years in the Legacy databases. This interrogation enables PMA to produce detailed multi-tabbed reports in Excel with all the necessary inventory details that are needed to plan for the migration. Additionally, PMA also produces a summary of code complexity for stored procs and functions. In which it breaks down the code into Low, Medium and Complex buckets based on number of lines of code.</div>',unsafe_allow_html=True)
                        st.write('###')
                        st.markdown('<div style="text-align: justify;">➦ We have developed a custom python script, which connects to snowflake to get the metadata, performs all necessary aggregations and generate the multi tabbed excel with all inventory details at one place.</div>',unsafe_allow_html=True)
                    with right:
                        data=[['Database details','This tab contains various database details like database version, reserved space, free space and used space.'],
                              ['Table Details','This tab contains all table level details including table size, row count, ladt ddl date, status, compression etc.'],
                              ['Object count','This tab contains object counts. The count is aggregated at every database and schema level.'],
                              ['Code Complexity','This tab contains code complexity. The user can view complexity at object level and complexity bucket level.'],
                              ['Object details','This tab shows all the object level details like schema wise objects, status, object type, is temporary? etc.'],
                              ['Column details','This tab has all column level details like column name, data type, nullable, text length, number of nulls etc.'],
                              ['Table constraints','This tab shows table constraints including table name, constraint name, column name, position, key type etc.'],
                              ['Dependencies','This tab contains all object level dependencies including parent object and child object details.'],
                              ['User details','This tab shows all user level details like username, userid, account status, expiry date, last login date etc.'],
                              ['Role privileges','This tab contains information related to role privileges like role name, grantee, grantor, is default role? etc.'],
                              ['Table privileges','This tab shows table level privileges such as table name, grantee, grantor, privilege at a schema level.']]
                        df = pd.DataFrame(data,columns=['Inventory Details','Description'])

                        fig = go.Figure(data=[go.Table(
                            columnorder=[1, 2],
                            columnwidth=[90, 380],
                            header=dict(values=['<b>Inventory details<b>','<b>Description<b>'],
                                        font=dict(size=16, color='black'),
                                        fill_color='#94B49F',
                                        line_color='#2d545e',
                                        align='center',
                                        height=30
                                        ),
                            cells=dict(values=df.transpose().values.tolist(),
                                       font=dict(family='century gothic', size=14, color='black'),
                                       fill_color='#CEE5D0',
                                       line_color='#2d545e',
                                       align='left',
                                       height=30)
                        )
                        ])
                        fig.update_layout(title_x=0, margin=dict(l=0, r=0, b=0, t=25), width=220,height=390, title = "")
                        st.write('##')
                        st.write('##')
                        st.write('##')
                        st.plotly_chart(fig, use_container_width=True)

                st.write('---')
                # Our approach - Inventory collection
                with st.container():
                    st.subheader('2) Identifying unused tables')
                    left,right=st.columns((1,2))
                    with left:
                        st.image(Image.open(r'unused_tables.png').resize((400,500)))
                    with right:
                        #step - 1
                        #st.write('##')
                        data=[['select customer_segment from sales;','Scott','08-08-2022'],
                              ['delete from sales where id = 1000;','John','07-08-2022']]
                        df = pd.DataFrame(data, columns=['Sql text','Username','Executed date'])
                        fig = go.Figure(data=[go.Table(
                            columnorder=[1, 2, 3],
                            columnwidth=[175, 120, 120],
                            header=dict(values=['<b>Sql text<b>', '<b>Username<b>', '<b>Executed date<b>'],
                                        font=dict(size=15, color='black'),
                                        fill_color='#94B49F',
                                        line_color='#2d545e',
                                        align='center',
                                        height=25
                                        ),
                            cells=dict(values=df.transpose().values.tolist(),
                                       font=dict(family='century gothic', size=15, color='black'),
                                       fill_color='#CEE5D0',
                                       line_color='#2d545e',
                                       align='center',
                                       height=30)
                        )
                        ])
                        fig.update_layout(title_x=1, margin=dict(l=0, r=0, b=0, t=10), width=220, height=100, title = "")
                        st.plotly_chart(fig, use_container_width=True)
                        #st.write('The uery history is extracted at every 3 hour intervals in the above format and then parsed using python script.')

                        # step - 2
                        # st.write('##')
                        data = [['select customer_segment from sales_vw;', 'sales_vw', 'Scott', '08-08-2022','Select'],
                                ['delete from product where id = 1000;','product','John','07-08-2022','Delete']]
                        df = pd.DataFrame(data, columns=['Sql text', 'object name', 'Username', 'Executed date','Operation'])
                        fig = go.Figure(data=[go.Table(
                            columnorder=[1, 2, 3, 4, 5],
                            columnwidth=[175, 60, 50, 70, 75],
                            header=dict(values=['<b>Sql text<b>', '<b>Object name<b>','<b>Username<b>', '<b>Executed date<b>','<b>Operation<b>'],
                                        font=dict(size=15, color='black'),
                                        fill_color='#94B49F',
                                        line_color='#2d545e',
                                        align='left',
                                        height=25
                                        ),
                            cells=dict(values=df.transpose().values.tolist(),
                                       font=dict(family='century gothic', size=15, color='black'),
                                       fill_color='#CEE5D0',
                                       line_color='#2d545e',
                                       align='left',
                                       height=30)
                        )
                        ])
                        fig.update_layout(title_x=0, margin=dict(l=0, r=0, b=0, t=30), width=220, height=125, title = "")
                        st.plotly_chart(fig, use_container_width=True)

                        # step - 3
                        # st.write('##')
                        data = [['select customer_segment from sales_vw;', 'sales', 'Scott', '08-08-2022', 'Select'],
                                ['delete from product where id = 1000;', 'product', 'John', '07-08-2022', 'Delete']]
                        df = pd.DataFrame(data, columns=['Sql text', 'object name', 'Username', 'Executed date','Operation'])
                        fig = go.Figure(data=[go.Table(
                            columnorder=[1, 2, 3, 4, 5],
                            columnwidth=[175, 60, 50, 70, 75],
                            header=dict(
                                values=['<b>Sql text<b>', '<b>Table name<b>', '<b>Username<b>', '<b>Executed date<b>','<b>Operation<b>'],
                                font=dict(size=15, color='black'),
                                fill_color='#94B49F',
                                line_color='#2d545e',
                                align='left',
                                height=25
                                ),
                            cells=dict(values=df.transpose().values.tolist(),
                                       font=dict(family='century gothic', size=15, color='black'),
                                       fill_color='#CEE5D0',
                                       line_color='#2d545e',
                                       align='left',
                                       height=30)
                        )
                        ])
                        fig.update_layout(title_x=0, margin=dict(l=0, r=0, b=0, t=30), width=220, height=125, title = "")
                        st.plotly_chart(fig, use_container_width=True)

                        # step - 4
                        # st.write('##')
                        data = [['Inventory', 'Public', 'sales', 'Scott', '08-08-2022', 'Select','select * from sales_vw'],
                                ['Inventory', 'Public', 'product', 'John', '07-08-2022', 'Delete','delete from product where id=1000']]
                        df = pd.DataFrame(data,
                                          columns=['Database', 'Schema name', 'Table name', 'Username', 'Executed date', 'Operation','Sql'])
                        fig = go.Figure(data=[go.Table(
                            columnorder=[1, 2, 3, 4, 5, 6, 7],
                            columnwidth=[70, 60, 50, 70, 75, 70, 175],
                            header=dict(
                                values=['<b>Database<b>', '<b>Schema<b>', '<b>Table<b>', '<b>Username<b>', '<b>Access date<b>',
                                        '<b>Operation<b>','<b>Query<b>'],
                                font=dict(size=15, color='black'),
                                fill_color='#94B49F',
                                line_color='#2d545e',
                                align='left',
                                height=25
                            ),
                            cells=dict(values=df.transpose().values.tolist(),
                                       font=dict(family='century gothic', size=15, color='black'),
                                       fill_color='#CEE5D0',
                                       line_color='#2d545e',
                                       align='left',
                                       height=30)
                        )
                        ])
                        fig.update_layout(title_x=0, margin=dict(l=0, r=0, b=0, t=30), width=220, height=125, title = "")
                        st.plotly_chart(fig, use_container_width=True)

                    st.write('➦ After parsing the query history, The table usage pattern data is loaded to a snowflake table. This data is then compared with the existing list of tables that we have gathered during inventory collection to find the list of unused tables over a period of time.')

                st.write('---')
                with st.container():
                    st.subheader('3) Prioritize tables for migration')
                    left,right=st.columns((1,2))
                    with left:
                        st_lottie(use_case_3,height=300)
                    with right:
                        st.write('##')
                        st.markdown('<div style="text-align: justify;">➦ According to a report by Mckinsey corp, migration projects tend to get delayed by atleast 30%. From a business perspective, it is really important to tackle such scenarios. One such solution is to migrate the most frequently accessed tables first, so that even if migration gets delayed, we still have the business critical tables in the destination.</div>', unsafe_allow_html=True)
                        st.write('###')
                        st.markdown('<div style="text-align: justify;">➦ In order to prioritise tables for migration, we have derived table access count by parsing the query history and categorized tables into three categories namely hot, warm and cold tables. Hot tables are the ones that are very frequently accessed. Cold tables are the ones that are infrequently accessed and warm tables are the ones in between.</div>', unsafe_allow_html=True)
                        st.write('###')
                        st.markdown('<div style="text-align: justify;">➦ When it comes to migration, typically hot tables need to be migrated first followed by warm and then cold tables.</div>', unsafe_allow_html=True)

                st.write('---')

        if menu_id=="Feedback Form":
            #Feedback form
            with st.container():
                def email_alert(subject, body, recipient):
                    msg = EmailMessage()
                    msg.set_content(body)
                    msg['subject'] = subject
                    msg['to'] = recipient

                    user = st.secrets['EMAIL_USER']
                    password = st.secrets['EMAIL_PWD']
                    msg['from'] = user

                    server = smtplib.SMTP('smtp.mailersend.net', 587)
                    server.starttls()
                    server.login(user, password)
                    server.send_message(msg)
                    server.quit()

                left, right = st.columns(2)
                with left:
                    st.subheader('Pre-Migration Assistant 🤖')

                left,middle,right = st.columns((1.5,0.4,0.8))   
                with left:
                    with st.form('Feedback form',clear_on_submit=True):
                        first_name=st.text_input('Enter your first name')
                        last_name=st.text_input('Enter your last name')
                        company = st.text_input('Enter your company')
                        question=st.text_input('Enter your question')
                        
                        subject = 'Query from '+first_name+' '+last_name+' ('+company+')'

                        if st.form_submit_button('submit') and first_name and last_name and company and question:
                            email_alert(subject,question,'sahil.h.kumar@kipi.bi')
                with right:
                    st.image(Image.open('logo4.png'),use_column_width=True)
                    ph_no='0863-198-3764'
                    st.markdown(f"<h4 style='text-align: right; color: white;'>{ph_no}</h4>", unsafe_allow_html=True)
                    address='IT-Hub, Bangalore - 577501'
                    st.markdown(f"<h4 style='text-align: right; color: white;'>{address}</h4>",unsafe_allow_html=True)
                    state='Karnataka, India'
                    st.markdown(f"<h4 style='text-align: right; color: white;'>{state}</h4>",unsafe_allow_html=True)

        if menu_id=="Analysis":
            engine = create_engine(URL(
                    user=st.secrets['DB_USER'],
                    account=st.secrets['DB_ACCOUNT'],
                    # region=config.region,
                    role=st.secrets['DB_ROLE'],
                    password=st.secrets['DB_PASSWORD'],
                    warehouse=st.secrets['DB_WAREHOUSE'],
                    database='SAMPLE_DB',
                    schema='REPORTING'
                ))
            tabs = st.tabs(['Summary Report 📃', 'Volumetirc Analysis 📊 ', 'Performance Stats 📉','Temperature Analysis 🌡️','Future state 📈',])
            with tabs[0]:
                summary_report(engine)

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    else:
        menu = ["Login", "Sign Up", "Forgot Username", "Forgot Password"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            st.subheader("Login Section")
            with st.form(key='login_form'):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login")
                
                
                if submit_button:
                    if username and password:
                        if username in credentials and credentials[username]["password"] == hash_password(password):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.rerun()
                        else:
                            st.warning("Incorrect Username/Password")
                    else:
                        st.warning("Please fill in both fields")
            st.info("Made By Kipithon Enablement Team")

        elif choice == "Sign Up":
            st.subheader("Create New Account")
            with st.form(key='signup_form'):
                name = st.text_input("Name")
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                email = st.text_input("Email")
                submit_button = st.form_submit_button("Sign Up")

                if submit_button:
                    if name and new_username and new_password and confirm_password and email:
                        if new_password == confirm_password:
                            if user_exists(new_username):
                                st.warning("Username already taken")
                            else:
                                save_user(new_username, name, new_password, email)
                                credentials[new_username] = {"name": name, "password": hash_password(new_password), "email": email}
                                st.success("You have successfully created an account!")
                        else:
                            st.warning("Passwords do not match")
                    else:
                        st.warning("Please fill in all fields")

        elif choice == "Forgot Username":
            st.subheader("Retrieve Username")
            with st.form(key='forgot_username_form'):
                email = st.text_input("Email")
                submit_button = st.form_submit_button("Retrieve Username")
                
                if submit_button:
                    if email:
                        found = False
                        for user, details in credentials.items():
                            if details["email"] == email:
                                st.success(f"Your username is {user}")
                                found = True
                                break
                        if not found:
                            st.warning("Email not found")
                    else:
                        st.warning("Please enter your email")

        elif choice == "Forgot Password":
            st.subheader("Reset Password")
            if st.session_state.reset_user:
                with st.form(key='reset_password_form'):
                    new_password = st.text_input("New Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    submit_button = st.form_submit_button("Submit New Password")
                    
                    if submit_button:
                        if new_password and confirm_password:
                            if new_password == confirm_password:
                                update_password(st.session_state.reset_user, new_password)
                                st.success("Password has been reset successfully!")
                                st.session_state.reset_user = None
                            else:
                                st.warning("Passwords do not match")
                        else:
                            st.warning("Please fill in both fields")
            else:
                with st.form(key='verify_user_form'):
                    username = st.text_input("Username")
                    email = st.text_input("Email")
                    submit_button = st.form_submit_button("Verify")
                    
                    if submit_button:
                        if username and email:
                            if username in credentials and credentials[username]["email"] == email:
                                st.session_state.reset_user = username
                                st.rerun()
                            else:
                                st.warning("Incorrect Username/Email")
                        else:
                            st.warning("Please fill in both fields")


if __name__ == "__main__":
    main()
