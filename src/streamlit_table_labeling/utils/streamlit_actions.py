from streamlit_table_labeling.utils.config import logger

from streamlit_table_labeling.db.database import TableLabelingDatabase

def select_one_table(db : TableLabelingDatabase):
    """
    """
    result = db.get_random_table_to_labelise()
    try:
        dict_result = {
            "id": result[0],
            "labels": result[1],
            "table": result[2],
            "done": result[3],
        }
        logger.info(f"Selected table for labeling: {dict_result}")
        return dict_result
    except Exception as e:
        logger.warning(f"No more table to labelise: {e}")
        return None

def save_table_labels(labels):
    """
    """
    print(labels)