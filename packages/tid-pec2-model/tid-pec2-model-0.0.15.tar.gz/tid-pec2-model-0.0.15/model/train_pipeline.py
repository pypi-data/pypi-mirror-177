import pandas as pd
from config.core import config
from pipeline import pipe
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split

def run_training() -> None:
    # read training data
    data = load_dataset(file_name=config.app_config.data_file)
    # divide train and test
    X_train, X_test, Y_train, Y_test = train_test_split(
        data[config.model_config.features],
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )
    
    X_train = pd.DataFrame(X_train, columns = config.model_config.features)
    X_test = pd.DataFrame(X_test, columns = config.model_config.features)
    Y_train = pd.DataFrame(Y_train, columns = config.model_config.target)
    Y_test = pd.DataFrame(Y_test, columns = config.model_config.target)
    
    pipe.fit(X_train, Y_train.values.ravel())

    # persist trained model
    save_pipeline(pipeline_to_persist=pipe)

if __name__ == "__main__":
    run_training()