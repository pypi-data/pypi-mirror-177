import pandas as pd

from model import __version__ as _version
from model.config.core import config
from model.processing.data_manager import load_pipeline

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_pipe = load_pipeline(file_name=pipeline_file_name)

def make_prediction(
    input_data: pd.DataFrame,
):
    """Make a prediction using a saved model pipeline."""
    data = pd.DataFrame(input_data)
    print(data)
    return _pipe.predict(data)