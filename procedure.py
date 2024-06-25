import pandas as pd
import datetime
import os
import streamlit as st
from edit_entry import edit_dialog

from main_new import get_new_entry
from app_utilities import get_file_df
from app_utilities import save_file_df, FILE_MAP
# To do: tabs for: create quote, delete quote, edit quote and all quotes overview
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode, DataReturnMode


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
    print('ppppppppppppppppp',selected_rows)
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


        '''if 'edit_mode' in st.session_state and st.session_state.edit_mode:

            for i in range(st.session_state.selected_rows.shape[0]):
                st.write(f'Editing Row----------------------- :{i + 1}')
                row = st.session_state.selected_rows.iloc[i]
                print('*****', row)
                edited_data = {}

                for key in row.index:
                    if key != 'Procedure number':
                        if key == 'Approval date':
                            edited_data[key] = st.date_input(f'{key}:', value=str(row[key]), key=f'{i}-{key}')
                        else:
                            edited_data[key] = st.text_input(f'{key}:', value=str(row[key]), key=f'{i}-{key}')
                print('eeeeeeeeeeeeeeeeee', edited_data)
                print(edited_data.keys())
                if st.button('Save Changes', key=f'save-{choice}'):
                    print('hhhhhhhhhhhhhhh')
                    print('rrrrrrrrrrrrrrrrrrrrrrrrrrr', row["Procedure number"])
                    print(st.session_state.df)
                    index = row["Procedure number"]
                    for col in edited_data.keys():
                        st.session_state.df.loc[st.session_state.df['Procedure number'] == index, col] = edited_data[
                            col]
                    print('bbbbbbbbbbbbbbbbbb', st.session_state.df)
                    print('ffffffffffffff', FILE_MAP[f'{choice}'])
                    save_file_df(st.session_state.df, FILE_MAP[f'{choice}'])
                    st.success('updated successfully')
                    st.session_state.edit_mode = False
                    st.rerun()'''


    '''st.markdown("""
                    <style>
                    sidebar .sidebar-content {
                         max-width:100%;
                        background-color: #111 !important;
                    }
                    </style>
                        """, unsafe_allow_html=True)
    print('session df isssssssssssssssssssssssss',df)

    # Configure Ag-Grid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    gb.configure_column('Approval date',cellEditor='agDateCellEditor',
                        cellEditorParams={'maxValidYear': 2050, 'minValidYear': 1980})

    response = AgGrid(
        df,
        width=100,
        fit_columns_on_grid_load=True,
        gridOptions=gb.build(),

        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        data_return_mode=DataReturnMode.AS_INPUT,
        theme ='streamlit',

    )
    selected_rows = response["selected_rows"]
    print('sssssssssssssssss',selected_rows)



    #st.write(df)
    if not isinstance(selected_rows, type(None)):
        if not selected_rows.empty:

            st.write('selected rows--------------------------')

            if st.button('Edit'):
                st.session_state.edit_mode = True
                st.session_state.selected_rows = selected_rows
        if 'edit_mode' in st.session_state and st.session_state.edit_mode:

            for i in range(st.session_state.selected_rows.shape[0]):
                st.write(f'Editing Row----------------------- :{i + 1}')
                row = st.session_state.selected_rows.iloc[i]
                print('*****', row)
                edited_data = {}

                for key in row.index:
                    if key != 'Procedure number':
                        if key =='Approval date':
                            edited_data[key] = st.date_input(f'{key}:', value=str(row[key]), key=f'{i}-{key}')
                        else:
                            edited_data[key] = st.text_input(f'{key}:', value=str(row[key]), key=f'{i}-{key}')
                print('eeeeeeeeeeeeeeeeee', edited_data)
                print(edited_data.keys())
                if st.button('Save Changes', key=f'save-{choice}'):
                    print('hhhhhhhhhhhhhhh')
                    print('rrrrrrrrrrrrrrrrrrrrrrrrrrr',row["Procedure number"])
                    print(st.session_state.df)
                    index = row["Procedure number"]
                    for col in edited_data.keys():
                        st.session_state.df.loc[st.session_state.df['Procedure number'] == index, col] = edited_data[col]
                    print('bbbbbbbbbbbbbbbbbb', st.session_state.df)
                    print('ffffffffffffff', FILE_MAP[f'{choice}'])
                    save_file_df(st.session_state.df, FILE_MAP[f'{choice}'])
                    st.success('updated successfully')
                    st.session_state.edit_mode = False
                    st.rerun()'''





