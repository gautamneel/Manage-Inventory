import pandas as pd
import datetime
import streamlit as st
from app_utilities import get_risk_df
from app_utilities import save_risk_df
# To do: tabs for: create quote, delete quote, edit quote and all quotes overview
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode, DataReturnMode

MAX_TABLE_HEIGHT = 1000

custom_css ="""
                <style>
                sidebar .sidebar-content {
                    background-color:'grey'
                }
                </style>
                    """




def draw_grid(df):

    if 'df' not in st.session_state:
        st.session_state.df = df
        st.markdown(custom_css, unsafe_allow_html=True)
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    grid_options = gb.build()

    response= AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        data_return_mode=DataReturnMode.AS_INPUT,
        theme ='streamlit',
    )
    selected_rows = response["selected_rows"]
    print('sssssssssssssssss',selected_rows)



    #st.write(df)
    if not isinstance(selected_rows, type(None)):
        if not selected_rows.empty :

            st.write('selected rows--------------------------')

            if st.button('Edit'):
                st.session_state.edit_mode = True
                st.session_state.selected_rows = selected_rows
        if 'edit_mode' in st.session_state and st.session_state.edit_mode:
            print(st.session_state.selected_rows)
            print(type(st.session_state.selected_rows))
            for i in range(st.session_state.selected_rows.shape[0]):
                st.write(f'Editing Row----------------------- :{i+1}')
                row = st.session_state.selected_rows.iloc[i]
                print('*****',row)
                edited_data = {}
                for key in row.index:
                    if key!='Risk ID':
                        edited_data[key] = st.text_input(f'{key}:',value=str(row[key]),key=f'{i}-{key}')
                print('eeeeeeeeeeeeeeeeee',edited_data)
                print(edited_data.keys())
                if st.button('Save Changes', key=f'save-{i}'):
                    index = row["Risk ID"]
                    for col in edited_data.keys():
                        st.session_state.df.loc[st.session_state.df['Risk ID'] == index, col]=edited_data[col]
                    save_risk_df(st.session_state.df)
                    st.success('updated successfully')
                    st.session_state.edit_mode = False
                    st.experimental_rerun()





