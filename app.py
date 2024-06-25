import streamlit as st
import os.path as path
import sys

import schedule
from check_contract_expiration import run_schedular
import threading

from main_page import draw_grid
#from main_new import draw_grid
from procedure import draw_grid_pr
from app_utilities import (
    app_ttl,
    hide_streamlit_style,
    get_app_logo,
    get_file_df,

)

custom_css = """
                <style>
                sidebar .sidebar-content {
                    background-color:'black'

                }
                .css-1d391kg {
                    max-width:15%;
                    }
                .css-18e3th9{
                    flex: 1 1 80%;
                    max-width:80%;
                    background-color:'black';

                }
                </style>
                    """


def get_numeric_style_with_precision(precision: int) -> dict:
    return {"type": ["numericColumn", "customNumericFormat"], "precision": precision}

# this code checks for current path (it depends whether it is called from an exe or not)
if getattr(sys, 'frozen', False):
    this_path = path.dirname(sys.executable)
elif __file__:
    this_path = path.abspath(path.dirname(__file__))

# Hide the hamburger menu and set the favicon
st.set_page_config(page_title=app_ttl(),page_icon=get_app_logo(),layout='wide',)
st.markdown(hide_streamlit_style(), unsafe_allow_html=True)

def sidebar():
    st.sidebar.image(get_app_logo(), use_column_width=True)
    st.markdown("""
        <style>
        sidebar .sidebar-content {
             max-width:15%;
            background-color: #111 !important;
        }
        </style>
            """, unsafe_allow_html=True)
    st.sidebar.subheader('UK BAC Inventory Logs')
    options = ['Risk Register', 'Change Log', 'Procedure Log', 'Model Inventory', 'Expert Judgement Log','Controls Log','Contracts Log','Policy Log','Reports Log']
    choice = st.sidebar.radio('select',options,label_visibility='collapsed')

    
    return choice

def body(choice):
    if choice == 'Risk Register':
        df = get_file_df('risk_mgmt')
        draw_grid(choice,df)
        #new_entry(choice,df,'Risk ID')
    if choice == 'Change Log':
        df = get_file_df('change_log')
        draw_grid(choice,df)
        #new_entry(choice,df)
    if choice == 'Procedure Log':

        df = get_file_df('procedure_log')
        draw_grid_pr(choice,df,'Procedure number')


    if choice == 'Model Inventory':
        df = get_file_df('models_inventory')
        draw_grid(choice,df)

    if choice == 'Expert Judgement Log':
        df = get_file_df('expert_judgement_logs')
        draw_grid(choice,df)

    if choice == 'Controls Log':
        df = get_file_df('controls_log')
        draw_grid(choice,df)

    if choice == 'Policy Log':
        df = get_file_df('policy_log')
        draw_grid(choice,df)

    if choice == 'Reports Log':
        df = get_file_df('reports_log')
        draw_grid(choice,df)


    if choice == 'Contracts Log':
        df = get_file_df('contracts_log')
        draw_grid(choice, df)


def main():
    choice = sidebar()
    body(choice)



if __name__ == '__main__':

    threading.Thread(target=run_schedular, daemon=True).start()
    main()