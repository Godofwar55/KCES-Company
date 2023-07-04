# ----------------------------------------- Import ---------------------------------------------------------------------
import pickle
from pathlib import Path
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import pandas as pd
import hashlib
import sqlite3
import plotly.express as px

# ------------------------------------------------ screen --------------------------------------------------------------

st.set_page_config(page_title='KCSAP',page_icon=':snow_capped_mountain:', layout='wide')

# ------------------------------------------------ data beast ----------------------------------------------------------
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

leader_data = sqlite3.connect('DB/leader_data.db')
leader_info = leader_data.cursor()
all_worker_data = sqlite3.connect('DB/all_worker.db')
all_worker_info = all_worker_data.cursor()


def create_usertable(db_info):
    db_info.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password,db_info,db_data):
    db_info.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    db_data.commit()


def login_user(username,password,db_info):
    db_info.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data=db_info.fetchall()
    return data


def view_all_users(db_info):
    db_info.execute('SELECT * FROM userstable')
    data=db_info.fetchall()
    return data


def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# ------------------------------------------------ read excel file -----------------------------------------------------
# df = pd.read_excel(
    # io='supermarkt_sales (1).xlsx',
    # engine='openpyxl',
    # sheet_name='Sheet1',
    # skiprows=3,
    # usecols='B:R',
    # nrows=1000,
# )

def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --------------------------------------------------- MAIN def ---------------------------------------------------------

def main():
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
    local_css("style/style.css")
    lottie_coding=load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_3rwasyjy.json")
    menu=["Home" ,"Login","Sign Up"]
    choice=st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        # hide_st_style="""
        # <style>
        # #MainMenu {visibility: hidden;}
        # footer {visibility: hidden;}
        # </style>
        # """
        # st.markdown(hide_st_style,unsafe_allow_html=True)
        # st.dataframe(df)
        with st.container():
            st.subheader('Hi, welcome to KACS website.')
            st.title('Information about us')
            st.write("This app made to help company to now that there worker is today working or no")
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)
            with left_column:
                st.header('what we do')
                st.write("##")
                st.write("""
                The company owner can make there account by going to sign up menu. then, puting their username and posword and click on the sign up button they asked to "Go to login menu to loqin. \n
                when they got to loqin menu they can use thier username and posword to loqin then a page will open for them if they click to sign up they can make an account for thier worker and the worker can user the username and posword thier company owner give them to loqin from loqin and they can by clicking a button sign in for thier company roll.
                """)
            with right_column:
                st_lottie(lottie_coding, height=300, key="coding")

        with st.container():
            st.write("---")
            st.header('giving feedback')
            st.write('##')
            contact_form = """
            <form action="https://formsubmit.co/mosavimujtaba366@gmail.com" method="POST">
             <input type="hidden" name="_captcha" value="false">
             <input type="text" name="name" placeholder="your name" required>
             <input type="email" name="email" placeholder="your email" required>
             <textarea name="message" placeholder="your massage here" required></textarea>
             <button type="submit">Send</button>
            </form>
            """
            left_column, right_column = st.columns(2)
            with left_column:
                st.markdown(contact_form, unsafe_allow_html=True)
            with right_column:
                st.empty()
    elif choice == "Login":
        login()
        hide_st_style="""
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
        st.markdown(hide_st_style,unsafe_allow_html=True)
    elif choice == "Sign Up":
        signup(db_info=leader_info, db_data=leader_data, loqin=True)
        hide_st_style="""
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
        st.markdown(hide_st_style,unsafe_allow_html=True)

# ------------------------------------------------ SIGNUP def ----------------------------------------------------------
def signup(db_info, db_data, loqin):
    left_column,right_column = st.columns(2)
    signup_imogi = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_d7zwANc67P.json")
    with right_column:
        st_lottie(signup_imogi,height=300,key="sign_up")
    with left_column:
        st.subheader("Create New Account")
    new_user=st.text_input("Username")
    new_password=st.text_input('password')
    if st.button("SignUp"):
        create_usertable(db_info=db_info)
        add_userdata(username=f'\n{new_user}',password=f'\t{new_password}', db_info=db_info, db_data=db_data)
        st.success("You have successfully created a valid Account")
        if loqin:
            st.subheader("Go to Login Menu if you want to login")

def signup_eemploy(db_info, db_data, db_info1, db_data1):
    left_column,right_column = st.columns(2)
    signup_imogi = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_d7zwANc67P.json")
    with right_column:
        st_lottie(signup_imogi,height=200,key="coding")
    with left_column:
        st.subheader("Create New Account")
    new_user=st.text_input("Username")
    new_password=st.text_input('password')
    if st.button("SignUp"):
        create_usertable(db_info=db_info)
        add_userdata(username=new_user,password=f'\t{new_password}', db_info=db_info, db_data=db_data)
        add_userdata(username=new_user,password=f'\t{new_password}', db_info=db_info1, db_data=db_data1)
        st.success("You have successfully created a valid Account")

# ------------------------------------------------- LOGIN def ----------------------------------------------------------
def login():
    if st.button("employer"):
        username_e = st.text_input("User Name")
        password_e = st.text_input("Password",type='password')
        company_e = st.text_input("Your company")
        if st.checkbox("Login"):
            create_usertable(db_info=leader_info)
            result = login_user(username=f'\n{username_e}', password=f'\r{password_e}', db_info = leader_info)
            if result:
                worker()
            else:
                st.warning("Incorrect Username/Password")
    if st.button("company_owner"):
        username = st.text_input("User Name")
        password = st.text_input("Password",type='password')
        if st.checkbox("Login"):
            create_usertable(db_info=leader_info)
            result=login_user(username=f'\n{username}',password=f'\t{password}',db_info=leader_info)
            if result:
                leader(leadername=username)
            else:
                st.warning("Incorrect Username/Password")

# ---------------------------------------------- Leader screen ---------------------------------------------------------
def leader(leadername):
    company = st.text_input("Your company")
    worker_data = sqlite3.connect(f"DB/{company}.db")
    worker_info=worker_data.cursor()
    selected = option_menu(
        menu_title=None,
        options=["Help", "Present", "Absent" , "Sinup", "More data"],
        icons=["question-circle-fill","person-check","person-dash", "person-plus", "three-dots"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important","black": "#fafafa"},
            "icon": {"color": "Orange","font-size": "25px","font-colot": "black"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#04AA6D",
            },
            "nav-link-selected": {"background-color": "green"}
        },
    )
    # ---------------------------------------- Help part of leader -----------------------------------------------------
    if selected == "Help":
        helps = ["All", "How to make new worker account", "How to check who is working", "How to check who is not working", "How to see mor informtion about you employees"]
        help = st.selectbox("search",helps)
        if help == "All" or help == "How to check who is working":
            st.header('If you want to check who is working to day click on "Who is working today"\n')
        if help == "All" or help == "How to check who is not working":
            st.header('If you want to check who is not hear today click on "Who is not working today"\n')
        if help == "All" or help == "How to make new worker account":
            st.header('If you get a new employee and want to make an account for hem/her click on "Make New employee account"\n')
        if help == "All" or help == "How to see mor informtion about you employees":
            st.header('If you want to get past data who was working or not working click on "More data"')
    # -------------------------------------------- Present leader part -------------------------------------------------
    if selected == "Present":
        st.header("This is the lest of your worker who is today working")
        present(leadername=leadername)
    # -------------------------------------- Absent leader part --------------------------------------------------------
    if selected == "Absent":
        st.header('This is the least of the lest of your worker who is not working teacher.')
    # --------------------------------------------- Sinup --------------------------------------------------------------
    if selected == "Sinup":
        # st.write('This is the lest of your worker if you want to add another worker click on add worker account.')
        st.subheader("User Profiles")
        try:
            user_result=view_all_users(db_info=worker_info)
            clean_db=pd.DataFrame(user_result,columns=["Username","Password"])
            st.dataframe(clean_db)
        except:
            st.subheader("You have no employee")
        # st.title("Add")
        signup_eemploy(db_info=worker_info, db_data=worker_data, db_info1=all_worker_info, db_data1=all_worker_data)
    if selected == "More data":
        st.header("This is the least of your worker")

        st.header(f'This is info about{chois_worker}')
        filter_menu = ["password", "Info in this year", "Info in this mounth", "Info in this week", "more"]
        filter = st.selectbox("filter here", filter_menu)
        if filter == "password":
            st.subheader(f'This is the password of {chois_worker}')
            st.header(password)


def present(leadername):
    None


def absent(leadername):
    None

# ------------------------------------------------ Worker --------------------------------------------------------------

def worker(worker_name, worker_compny):
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Help", "Sign in", "Give feedback", "The day I did not comed"],
            icons=["house", "book", "envelope"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important","black": "#fafafa"},
                "icon": {"color": "Orange","font-size": "25px", "font-colot": "black"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#04AA6D",
                },
                "nav-link-selected": {"background-color": "green"},
            },
            )

    if selected == "Help":
        st.subheader('If you want to sign in for your company click on sign in menu and you will see a button working today and not working. If you click on working you will see message sind if you click on not working you will see an input. write your ressan thier.')
    if selected == "Sign in":
        my_input=st.text_input("pleas, write your Name and last mane. ",
                               st.session_state["my_input"])
        working_today = st.button('Workingt today')
        not_working_today = st.button('Not working Today')
        if not_working_today:
            st.title('you are not working until')
            my_input=st.text_input("the day you are not working until. ",
                                   st.session_state["my_input"])
    if selected == "The day I did not comed":
        st.title(f"you have selected {selected}")
    if selected == "Give feedback":
        with st.container():
            st.write("---")
            st.header('Giving Feedback')
            st.write('##')
            contact_form="""
               <form action="https://formsubmit.co/mosavimujtaba366@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="your name" required>
                <input type="email" name="email" placeholder="your email" required>
                <textarea name="message" placeholder="your massage here" required></textarea>
                <button type="submit">Send</button>
               </form>
               """
            left_column,right_column=st.columns(2)
            with left_column:
                st.markdown(contact_form,unsafe_allow_html=True)
            with right_column:
                st.empty()


if __name__ == '__main__':
	main()
