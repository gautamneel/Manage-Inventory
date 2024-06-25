import pandas as pd
import datetime
import streamlit as st
from ui.app_utilities import get_next_quote_id

# To do: tabs for: create quote, delete quote, edit quote and all quotes overview
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode

MAX_TABLE_HEIGHT = 1500


def get_numeric_style_with_precision(precision: int) -> dict:
    return {"type": ["numericColumn", "customNumericFormat"], "precision": precision}


PRECISION_ZERO = get_numeric_style_with_precision(0)
PRECISION_ONE = get_numeric_style_with_precision(1)
PRECISION_TWO = get_numeric_style_with_precision(2)
PINLEFT = {"pinned": "left"}






def highlight(color, condition):
    code = f"""
        function(params) {{
            color = "grey";
            if ({condition}) {{
                return {{
                    'backgroundColor': "grey"
                }}
            }}
        }};
    """
    return JsCode(code)
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
def update_quote_object(quote_data):
    """ take quote dataframe and update quote object"""
    quote_data



def draw_grid(
        df,
        formatter: dict = None,
        selection = "multiple",
        use_checkbox = True,
        fit_columns = True,
        theme = "streamlit",
        max_height: int = MAX_TABLE_HEIGHT,
        wrap_text: bool = False,
        auto_height: bool = False,
        grid_options: dict = None,
        key = None,
        css: dict = None
    ):

        gb = GridOptionsBuilder()
        gb.configure_default_column(
        filterable = True,
        groupable = False,
        editable = False,
        wrapText = wrap_text,
        autoHeight = auto_height,
        )

        if grid_options is not None:
            gb.configure_grid_options(**grid_options)

        for latin_name, (cyr_name, style_dict) in formatter.items():
            gb.configure_column(latin_name, header_name=cyr_name, **style_dict)

        gb.configure_selection(selection_mode=selection, use_checkbox=use_checkbox)

        return AgGrid(
            df,
            gridOptions=gb.build(),
            update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
            allow_unsafe_jscode=True,
            fit_columns_on_grid_load=fit_columns,
            height=min(max_height, (1 + len(df.index)) * 50),
            theme=theme,
            key=key,
            custom_css=css
        )



