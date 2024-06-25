import pandas as pd
import datetime
import streamlit as st
from app_utilities import save_file_df, FILE_MAP, FIELD_ID_MAP
from main_new import get_new_entry
# To do: tabs for: create quote, delete quote, edit quote and all quotes overview
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode, DataReturnMode

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
            print('*****', row)
            edited_data = {}
            for key in row.index:
                if key not in ['Risk ID', 'Procedure number', 'Model Number', 'Judgement ID', 'Control ID',
                               'Contract Number', 'Policy number', 'Report number', 'Change log']:

                    if choice in ['Procedure Log','Contracts Log']:
                        print('choiceeeeeeeeeeeeeeeeeeee is sssssssss',choice)
                        if key in ['Approval date', 'Date']:
                            print('wewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',key)
                            edited_data[key] = st.date_input(key,key=key)
                        else:
                            edited_data[key][key] = st.text_input(key, key=key)

                    else:
                        edited_data[key] = st.text_input(key, key=key)

                    edited_data[key] = st.text_input(f'{key}:', value=str(row[key]), key=f'{i}-{key}')
            print('eeeeeeeeeeeeeeeeee', edited_data)
            print(edited_data.keys())
            if st.button('Save Changes', key=f'save-{choice}'):
                print('hhhhhhhhhhhhhhh')
                index = row[FIELD_ID_MAP[choice]]
                for col in edited_data.keys():
                    st.session_state.df.loc[st.session_state.df[FIELD_ID_MAP[choice]] == index, col] = edited_data[
                        col]
                print('bbbbbbbbbbbbbbbbbb', st.session_state.df)
                print('ffffffffffffff', FILE_MAP[f'{choice}'])
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
    print('dirrrrrrrrrrrrrrrrrrr', edited_df[edited_df.Select])
    selected_rows = edited_df[edited_df.Select]
    print('ppppppppppppppppp', selected_rows)

    selected_rows = selected_rows.drop('Select', axis=1)
    print('after axissssssssssssssssssssss',selected_rows)
    if not isinstance(selected_rows, type(None)):
        if not selected_rows.empty:

            st.write('selected rows--------------------------')

            if st.button('Edit'):
                st.session_state.edit_mode = True
                st.session_state.selected_rows = selected_rows
                edit_dialog(choice)
    if st.button('New'):
        get_new_entry(choice,df)

'''  if 'df' not in st.session_state:
        st.session_state.df = df
        #st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown("""
                <style>
                sidebar .sidebar-content {
                     max-width:80%;
                    background-color: #111 !important;
                }
                </style>
                    """, unsafe_allow_html=True)
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    gb.configure_default_column(resizable=True)
    gb.configure_grid_options(domLayout='autoHeight')
    grid_options = gb.build()

    response= AgGrid(
        df,
        width='100%',
        fit_columns_on_grid_load=True,
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
                    if key not in ['Risk ID', 'Procedure number', 'Model Number', 'Judgement ID', 'Control ID',
                                   'Contract Number', 'Policy number', 'Report number', 'Change log']:
                        edited_data[key] = st.text_input(f'{key}:',value=str(row[key]),key=f'{i}-{key}')
                print('eeeeeeeeeeeeeeeeee',edited_data)
                print(edited_data.keys())
                if st.button('Save Changes', key=f'save-{choice}'):
                    print('hhhhhhhhhhhhhhh')
                    index = row["Risk ID"]
                    for col in edited_data.keys():
                        st.session_state.df.loc[st.session_state.df[FIELD_ID_MAP[choice]] == index, col] = edited_data[col]
                    print('bbbbbbbbbbbbbbbbbb',st.session_state.df)
                    print('ffffffffffffff',FILE_MAP[f'{choice}'])
                    save_file_df(st.session_state.df,FILE_MAP[f'{choice}'])
                    st.success('updated successfully')
                    st.session_state.edit_mode = False
                    st.rerun()'''





