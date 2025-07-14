from sqlmodel import Session, select
import streamlit as st

from streamlit_table_labeling.utils.config import logger
from streamlit_table_labeling.db.database import TableLabelingDatabase
from streamlit_table_labeling.db.schemas import TableLabeling

def select_one_table(db : TableLabelingDatabase):
    """ Fetches a random table to labelise from the database.
    Args:
        db (TableLabelingDatabase): The database instance to use.
    Returns:
        dict: A dictionary containing the table's id, labels, table data, and done status
    """
    result = db.get_random_table_to_labelise()
    try:
        dict_result = {
            "id": result[0],
            "labels": result[1],
            "table": result[2],
            "done": result[3],
        }
        return dict_result
    except Exception as e:
        logger.warning(f"No more table to labelise: {e}")
        return {}

def save_table_labels(table_infos: dict, labels: list, db: TableLabelingDatabase):
    """
    Updates the labels of a table in the database.
    Args:
        table_infos (dict): Dictionary containing information about the table. Must include an 'id' key.
        labels (list): List of labels to assign to the table.
        db (TableLabelingDatabase): The database instance to use.
    Raises:
        ValueError: If 'id' is not present in table_infos or if no table with the given id is found.
    """
    table_id = table_infos.get("id")
    if table_id is None:
        raise ValueError("table_infos must contain an 'id'.")

    with Session(db.get_engine()) as session:
        statement = select(TableLabeling).where(TableLabeling.id == table_id)
        result = session.exec(statement).first()
        if not result:
            raise ValueError(f"No table with id {table_id} found.")

        result.labels = labels
        result.done = True

        session.add(result)
        session.commit()

def init_session_state(db: TableLabelingDatabase):
    """ Initializes the session state for the Streamlit app.
    Sets up the initial state for showing success toast, history, and the current table to labelise.
    Args:
        db (TableLabelingDatabase): The database instance to use for fetching the initial table.
    """
    if "show_success_toast" not in st.session_state:
        st.session_state["show_success_toast"] = False
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "current_table_to_labelise" not in st.session_state:
        st.session_state["current_table_to_labelise"] = select_one_table(db=db)


def sidebar_history(history):
    """ Displays the history of labeled tables in the sidebar.
    Args:
        history (list): List of dictionaries containing the history of labeled tables.
    """
    st.title("Historic")
    if not history:
        st.write("No history yet.")
        return

    st.subheader("Last 5 labeled tables:")
    for item in reversed(history[-5:]):
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(128,61,245, 0.1);
                    padding: 0px 0.25rem;
                    margin-top: 0.5rem;
                    border-radius: 0.25em;
                    color: rgb(109, 63, 192);
                    font-size: 0.875rem;
                    display: inline-block;">
                    Table id: {item['id']}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            if st.button(
                " ",
                key=f"reload_{item['id']}",
                icon=":material/edit:",
                help="Edit this table",
                type="tertiary",
            ):
                st.session_state["current_table_to_labelise"] = {
                    "id": item["id"],
                    "table": item["table"]
                }
                st.rerun()

def save_and_update_history(table_info, labels, db):
    """ Saves the labels for a table and updates the session history.
    Args:
        table_info (dict): Dictionary containing information about the table.
        labels (list): List of labels to assign to the table.
        db (TableLabelingDatabase): The database instance to use.
    """
    save_table_labels(table_infos=table_info, labels=labels, db=db)
    current_entry = {
        "id": table_info.get("id"),
        "labels": labels,
        "table": table_info.get("table"),
    }
    existing_ids = [item["id"] for item in st.session_state["history"]]
    if current_entry["id"] in existing_ids:
        st.session_state["history"] = [
            current_entry if item["id"] == current_entry["id"] else item
            for item in st.session_state["history"]
        ]
    else:
        st.session_state["history"].append(current_entry)

    st.session_state["show_success_toast"] = True
    del st.session_state["current_table_to_labelise"]
    st.rerun()
