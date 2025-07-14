import streamlit as st

from streamlit_table_labeling.utils.config import Vars
from streamlit_table_labeling.utils.streamlit_actions import save_table_labels, sidebar_history, init_session_state, save_and_update_history

from streamlit_table_labeling.db.database import TableLabelingDatabase

@st.cache_resource
def get_database(check=True):
    """ Initializes and returns a TableLabelingDatabase instance.
    Args:
        check (bool): If True, checks the database tables.
    Returns:
        TableLabelingDatabase: An instance of the database.
    """
    db = TableLabelingDatabase()
    if check:
        db.check_tables()
    return db

DB = get_database(check=True)
TABLE_LABELS = Vars.TABLE_LABELS.value.split(',')


def app():
    """ Main function to run the Streamlit app for table labeling. """
    # Session state
    init_session_state(DB)

    if st.session_state.get("show_success_toast", False):
        st.toast("Saved ! ", icon="✅")
        st.session_state["show_success_toast"] = False

    # ---------------------------------------------------------------------------------

    table_to_labelise = st.session_state["current_table_to_labelise"]
    selection_key = f"label_selection_{table_to_labelise.get('id')}"

    with st.sidebar:
        sidebar_history(st.session_state["history"])


    st.title("Streamlit Table Labeling App")
    
    col_labels, col_validation = st.columns([3, 1])
    selection = col_labels.pills("Labels", TABLE_LABELS, selection_mode="multi", label_visibility="collapsed", key=selection_key)
    validation_button = col_validation.button("Validate", use_container_width=True, type="primary")


    if not table_to_labelise:
        st.info("✅ All tables have been labeled!")
        return
    else:
        table = st.dataframe(data=table_to_labelise.get("table", []),  use_container_width=True)
        st.badge(f"Table id : {table_to_labelise.get('id')}", icon=":material/star:", color="violet")

    if validation_button:
        save_and_update_history(
            table_info=table_to_labelise,
            labels=selection,
            db=DB
        )

if __name__ == "__main__":
    app()