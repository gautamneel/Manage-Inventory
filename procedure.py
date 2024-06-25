import pandas as pd
import datetime
import os
import streamlit as st
from edit_entry import edit_dialog
import os

from app_utilities import get_file_df
from app_utilities import save_file_df, FILE_MAP
# To do: tabs for: create quote, delete quote, edit quote and all quotes overview
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode, DataReturnMode
username = os.getlogin()

def get_file_from_local(policy_value=None):
    file_path = fr'C:\Users\ngautam\Brookfield\UK PRT UK Users - Documents\01. Corporate\03. Policies\1B BAC UK Credit Risk Policy June 2024.pdf'
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            return file.read()
    else:
        st.error(f"File for policy {policy_value} not found.")
        return None

def show_policy_details(policy_name):
    st.write(f"Details of {policy_name}")
    details = st.session_state.df[st.session_state.df['Policy number'] == policy_name]
    st.write(details)

def draw_grid_pr(choice,df,field=None):
    #df.reset_index(drop=True, inplace=True)
    st.session_state.df = df



    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)
    #df_with_selections.style.applymap(lambda x: 'background-color: #B4C6E7; color: black; border: 1.3px solid black; font-weight: bold')

    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True) },
        disabled=df.columns,
        use_container_width=True,

        #num_rows="dynamic",
    )

    selected_rows = edited_df[edited_df.Select]
    selected_rows = selected_rows.drop('Select', axis=1)
    if not isinstance(selected_rows, type(None)):
        if not selected_rows.empty:

            col1, col2 = st.columns([1,2])
            with col1:
                PDFbyte = get_file_from_local()
                st.download_button(label="Export Policy",
                                   data=PDFbyte,
                                   file_name="1B BAC UK Credit Risk Policy June 2024.pdf",
                                   mime='application/octet-stream')
            with col2:
                if st.button('Edit'):
                    st.session_state.edit_mode = True
                    st.session_state.selected_rows = selected_rows
                    edit_dialog(choice)

        if st.button('New'):
            get_new_entry(choice, df)
