
import streamlit as st
from app_utilities import save_file_df, FILE_MAP, FIELD_ID_MAP


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

                    if choice in ['Procedure Log', 'Contracts Log']:
                        print('choiceeeeeeeeeeeeeeeeeeee is sssssssss', choice)
                        if key in ['Approval date', 'Date']:
                            print('wewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww', key)
                            edited_data[key] = st.date_input(key, key=key)
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
