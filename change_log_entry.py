
import datetime
import streamlit as st
from app_utilities import save_file_df, FILE_MAP, FIELD_ID_MAP, ID_VALUE_MAP,get_file_df
from main_page import draw_grid
# To do: tabs for: create quote, delete quote, edit quote and all quotes overview
import pandas as pd

def get_next_val(df,val=None):

    if len(df)==0:
        return f'{ID_VALUE_MAP[val]}-1'
    else:

        max_id = df[f'{val}'].apply(lambda x: int(x.split('-')[1])).max()
        return f'{ID_VALUE_MAP[val]}-{max_id+1}'

def callback():
    st.session_state["first_form_clicked"] = True
def new_change_entry(choice,df,field=None):
    if choice in ['Procedure Log', 'Model Inventory','Contracts Log']:
        change_df = get_file_df('change_log')
        change_id = get_next_val(df,val='None')



def change_entry(choice,df,field=None):
  new_change_entry(choice, df,field)

