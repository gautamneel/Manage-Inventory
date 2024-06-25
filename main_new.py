import pandas as pd
import datetime
import streamlit as st

from app_utilities import save_file_df, FILE_MAP, FIELD_ID_MAP
from app_utilities import save_file_df, FILE_MAP, FIELD_ID_MAP, ID_VALUE_MAP, get_file_df
import hydralit_components as hc

# To do: tabs for: create quote, delete quote, edit quote and all quotes overview
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode, DataReturnMode


import datetime
import streamlit as st
from app_utilities import save_file_df, FILE_MAP, FIELD_ID_MAP, ID_VALUE_MAP,get_file_df


import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode, DataReturnMode

def get_next_val(df,val=None):

    if len(df)==0:
        return f'{ID_VALUE_MAP[val]}-1'
    else:
        print('dataframe issssssssssss',df)
        print(df[val])
        max_id = df[val].apply(lambda x: int(x.split('-')[1])).max()
        print('id isssssssssssssssssssss',f'{ID_VALUE_MAP[val]}-{max_id+1}')
        return f'{ID_VALUE_MAP[val]}-{max_id+1}'

def callback():
    st.session_state["first_form_clicked"] = True


@st.experimental_dialog("Add New details", width="large")
def get_new_entry(choice,df,field=None):
        st.session_state["first_form_clicked"] = False
        print('in new entryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy',choice,df)

        input_fields = {}





        print('columnsssssssssss are  =========  ',df.columns)
        for i, key in enumerate(df.columns):
            if key not in ['Risk ID','Procedure number', 'Model Number', 'Judgement ID', 'Control ID', 'Contract Number','Policy number','Report number','Change log']:
                if choice in ['Procedure Log','Contracts Log']:
                    print('choiceeeeeeeeeeeeeeeeeeee is sssssssss',choice)
                    if key in ['Approval date', 'Date']:
                        print('wewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',key)
                        input_fields[key] = st.date_input(key,key=key)
                    else:
                        input_fields[key] = st.text_input(key, key=key)

                else:
                    input_fields[key] = st.text_input(key, key=key)
        submit_form = st.button(label="Save", help="Click to save!")

        # Checking if all the fields are non empty
        if submit_form:
            print('submiteedddddddddddd',input_fields)
            print('field is ',field)
            new_df = {}
            st.write(submit_form)
            if all(new_df.values()):
                if choice:
                    print('ccccccccccccccccccccccccc')
                    val = FIELD_ID_MAP[choice]
                    print('vvvvvvvvvvvvvv',val)
                    print(print(val,ID_VALUE_MAP[val]))

                    next_val = get_next_val(df, val)
                    input_fields[FIELD_ID_MAP[choice]] = next_val

                df = pd.concat([df, pd.DataFrame([input_fields])], ignore_index=True)
                print('fffffffffffffffffffffffffffffff', FILE_MAP[f'{choice}'])
                save_file_df(df, FILE_MAP[f'{choice}'])
                if choice in ['Model Inventory','Controls Log','Contracts Log','Policy Log'] :
                    change_df = {}
                    org_df = get_file_df('change_log').reset_index(drop=True,inplace=True)
                    val_choice = FIELD_ID_MAP['Change log']
                    print('valllllllllllll ',choice, val_choice)
                    print('choice vallllllllllllll',org_df[val_choice])
                    new_val = get_next_val((org_df, val_choice))
                    change_df['change_df'] = new_val
                    change_df['Type'] = choice
                    pd.concat([org_df, pd.DataFrame([change_df])], ignore_index=True)
                    final_df = pd.concat([df, pd.DataFrame([input_fields])], ignore_index=True)
                    print('fffffffffffffffffffffffffffffff', FILE_MAP[f'{choice}'])
                    save_file_df(final_df, FILE_MAP[f'{choice}'])



                st.rerun()

                # get change entry


            else:
                st.error('Please fill all the fields')
            return df


def new_entry(choice,df,field=None):

    '''if st.button('New Entry',key='nw'):
        if "first_form_clicked" not in st.session_state:
            st.session_state["first_form_clicked"] = False'''
    st.session_state["first_form_clicked"] = False
    df = get_new_entry(choice,df)
    #get_rval(df)
