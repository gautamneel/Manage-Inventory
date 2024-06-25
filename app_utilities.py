import streamlit as st
import pandas as pd
import os.path as path
import sys
import os

import calendar
from pathlib import Path
from datetime import datetime
username = os.getlogin()

# this code checks for current path (it depends whether it is called from an exe or not)
if getattr(sys, 'frozen', False):
    this_path = path.dirname(sys.executable)
elif __file__:
    this_path = path.abspath(path.dirname(__file__))


FILE_MAP = {
        'Risk Register': 'risk_mgmt',
        'Procedure Log': 'procedure_log',
        'Model Inventory': 'models_inventory',
        'Expert Judgement Log': 'expert_judgement_logs',
        'Controls Log': 'controls_log',
        'Contracts Log': 'contracts_log',
        'Policy Log': 'policy_log',
        'Reports Log': 'reports_log'
}

FIELD_ID_MAP = {
                'Risk Register': 'Risk ID',
                'Procedure Log': 'Procedure number',
                 'Model Inventory': 'Model Number',
                 'Expert Judgement Log': 'Judgement ID',
                 'Controls Log': 'Control ID',
                 'Contracts Log': 'Contract Number',
                 'Policy Log': 'Policy number',
                 'Reports Log': 'Report number',
                 'Change log' : 'Change request'}

ID_VALUE_MAP = {
                'Risk ID' : 'RSK',
                 'Procedure number' : 'PROC',
                 'Model Number' : 'MOD' ,
                 'Judgement ID' : 'EJ',
                 'Control ID' : 'CTRL',
                 'Contract Number' : 'CONT',
                 'Policy number' : 'POL',
                 'Report number' : 'RPT',
                 'Change request': 'C'

}

def hide_streamlit_style():
    txt = """
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
    """
    return txt
def get_file_df(file_name=None):
    print(fr'C:\Users\{username}\logs\{file_name}.xlsx')
    risk_data = pd.read_excel(fr'C:\Users\{username}\logs\{file_name}.xlsx')
    return risk_data

def save_file_df(df,file_name=None):
    risk_data = df.to_excel(fr'C:\Users\{username}\logs\{file_name}.xlsx', index=False)
    return risk_data
def app_ttl():
    return 'UK PRT Pricing Suite'

def get_app_logo():
    # Set the sidebar logo
    full_logo = path.join(path.join(this_path, 'images'), "Brookfield_Annuity_Logo.png")
    full_logo = Path(full_logo).relative_to(Path.cwd())
    return str(full_logo)


# Function to read and return the content of the text file
def read_text_file(file_path):
   with open(file_path, 'r', encoding='utf-8') as file:
       content = file.read()
   return content

def last_day_of_month(year, month):
    last_day = calendar.monthrange(year, month)[1]
    return last_day

def read_config(conf_path):
    config = {}
    df_config = pd.read_excel(conf_path, index_col=0)
    for index, row in df_config.iterrows():
        # get the variable and value from the row
        variable = index
        value = row[0]
        config[variable] = value
    return config

# Function to filter data based on user-selected filters
def apply_filters(df, filters):
    for column, value in filters.items():
        if value != "*":
            df = df[df[column] == value]
    return df




def app_icon():
    icon_path = path.join(path.join(this_path, 'data'), "ow3.png")
    icon_path = Path(icon_path).relative_to(Path.cwd())
    return str(icon_path)






