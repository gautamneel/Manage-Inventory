import pandas as pd
import datetime
import streamlit as st
from app_utilities import save_file_df, FILE_MAP, FIELD_ID_MAP
from new_entry import get_new_entry

MAX_TABLE_HEIGHT = 1500

custom_css = """
                <style>
               
                .css-18e3th9{
                    flex: 1 1 80%;
                    max-width:80%;
                    background-color:'grey';
                    'font-size': '14px''
                    
                }
                </style>
                    """


@st.experimental_dialog("Edit details", width="large")
def edit_dialog(choice):

    if 'edit_mode' in st.session_state and st.session_state.edit_mode:
        print(st.session_state.selected_rows)
        print(type(st.session_state.selected_rows))
        for i in range(st.session_state.selected_rows.shape[0]):

            row = st.session_state.selected_rows.iloc[i]
            edited_data = {}
            for key in row.index:
                if key not in ['Risk ID', 'Procedure number', 'Model Number', 'Judgement ID', 'Control ID',
                               'Contract Number', 'Policy number', 'Report number', 'Change log']:

                    if choice in ['Procedure Log','Contracts Log']:
                        if key in ['Approval date', 'Date']:
                            edited_data[key] = st.date_input(key,key=key)
                        else:
                            edited_data[key][key] = st.text_input(key, key=key)

                    else:
                        edited_data[key] = st.text_input(key, key=key)

                    edited_data[key] = st.text_input(f'{key}:', value=str(row[key]), key=f'{i}-{key}')
            if st.button('Save Changes', key=f'save-{choice}'):
                index = row[FIELD_ID_MAP[choice]]
                for col in edited_data.keys():
                    st.session_state.df.loc[st.session_state.df[FIELD_ID_MAP[choice]] == index, col] = edited_data[
                        col]
                save_file_df(st.session_state.df, FILE_MAP[f'{choice}'])
                st.success('updated successfully')
                st.session_state.edit_mode = False
                st.rerun()

def draw_grid(choice,df):
    st.session_state.df = df

    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True), 'background-color': 'black'},
        disabled=df.columns,
        use_container_width=True,

        # num_rows="dynamic",
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]


    selected_rows = selected_rows.drop('Select', axis=1)
    if not isinstance(selected_rows, type(None)):
        if not selected_rows.empty:

            if st.button('Edit'):
                st.session_state.edit_mode = True
                st.session_state.selected_rows = selected_rows
                edit_dialog(choice)
    if st.button('New'):
        get_new_entry(choice,df)

