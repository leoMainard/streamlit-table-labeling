import streamlit as st

from streamlit_table_labeling.utils.config import Vars
from streamlit_table_labeling.utils.streamlit_actions import save_table_labels, select_one_table

from streamlit_table_labeling.db.database import TableLabelingDatabase

TABLE_LABELS = Vars.TABLE_LABELS.value.split(',')

DB = TableLabelingDatabase()
DB.check_tables()

def app():

    with st.sidebar:
        st.title("Historic")

    st.title("Streamlit Table Labeling App")
    
    col_labels, col_validation = st.columns([3, 1])
    selection = col_labels.pills("Labels", TABLE_LABELS, selection_mode="multi", label_visibility="collapsed")
    validation_button = col_validation.button("Validate", use_container_width=True, type="primary")

    table_to_show = select_one_table(db = DB)
    table = st.dataframe(data=table_to_show.get("table", []), use_container_width=True)

    if validation_button:
        if selection:
            save_table_labels(labels= selection)
            # reset_selection()
            st.toast("Saved ! ", icon="✅")
        else:
            st.toast("Please select at least one label before validating.", icon="⚠️")

if __name__ == "__main__":
    app()