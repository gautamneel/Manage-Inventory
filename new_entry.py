
import datetime
import streamlit as st
from app_utilities import save_file_df, FILE_MAP, FIELD_ID_MAP, ID_VALUE_MAP,get_file_df
import pandas as pd


def get_next_val(df,val=None):

    if len(df)==0:
        return f'{ID_VALUE_MAP[val]}-1'
    else:
        max_id = df[val].apply(lambda x: int(x.split('-')[1])).max()
        return f'{ID_VALUE_MAP[val]}-{max_id+1}'

def callback():
    st.session_state["first_form_clicked"] = True


@st.experimental_dialog("Add New details", width="large")
def get_new_entry(choice,df,field=None):
        st.session_state["first_form_clicked"] = False
        input_fields = {}





        for i, key in enumerate(df.columns):
            if key not in ['Risk ID','Procedure number', 'Model Number', 'Judgement ID', 'Control ID', 'Contract Number','Policy number','Report number','Change log']:
                if choice in ['Procedure Log','Contracts Log']:
                    if key in ['Approval date', 'Date']:
                        input_fields[key] = st.date_input(key,key=key)
                    else:
                        input_fields[key] = st.text_input(key, key=key)

                else:
                    input_fields[key] = st.text_input(key, key=key)
        submit_form = st.button(label="Save", help="Click to save!")

        # Checking if all the fields are non empty
        if submit_form:
            new_df = {}
            st.write(submit_form)
            if all(new_df.values()):
                if choice:
                    val = FIELD_ID_MAP[choice]
                    next_val = get_next_val(df, val)
                    input_fields[FIELD_ID_MAP[choice]] = next_val

                df = pd.concat([df, pd.DataFrame([input_fields])], ignore_index=True)
                save_file_df(df, FILE_MAP[f'{choice}'])
                if choice in ['Model Inventory','Controls Log','Contracts Log','Policy Log'] :
                    change_df = {}
                    org_df = get_file_df('change_log').reset_index(drop=True,inplace=True)
                    val_choice = FIELD_ID_MAP['Change log']
                    new_val = get_next_val((org_df, val_choice))
                    change_df['change_df'] = new_val
                    change_df['Type'] = choice
                    pd.concat([org_df, pd.DataFrame([change_df])], ignore_index=True)
                    final_df = pd.concat([df, pd.DataFrame([input_fields])], ignore_index=True)
                    save_file_df(final_df, FILE_MAP[f'{choice}'])



                st.rerun()

                # get change entry


            else:
                st.error('Please fill all the fields')
            return df