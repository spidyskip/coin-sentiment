import functools
from .debug import *
import os

VAR_OUTPUT = "save_path"


def save_decorator(func):
    """
    Decorator to save the dataframe to a csv or xlsx file.

    Name of the file saved is composed of the subreddit name and the function name.

    Example:
        {sub}_{func.__name__}.csv

    Output:
        CSV or XLSX file (if is defined name of the file)

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result_df = func(*args, **kwargs)
        save_path = kwargs.get(VAR_OUTPUT)
        sub = kwargs.get("sub")

        if save_path is not None and result_df is not None:
            # Check extension output file
            file_extension = "xlsx" if save_path.endswith(".xlsx") else "csv"
            # Define file name
            file_name = f"{func.__name__}_{sub}.{file_extension}"
            # Define file path
            if not save_path.endswith(file_extension):
                # If save_path is a file, save the file in the same directory
                # with the same name
                save_path = save_path + "/"
                os.makedirs(save_path, exist_ok=True)
            if not os.path.isdir(save_path):
                file_path = f"{save_path.split('.')[0]}_{file_name}"
            else:
                # If save_path is a directory, save the file in the directory
                file_path = os.path.join(save_path, file_name)

            # Save file
            if file_extension == "csv":
                result_df.to_csv(f"{file_path}", index=False)
            else:
                result_df.to_excel(f"{file_path}", index=False)
            logging.info(
                "%s file saved at %s", file_path.split(".")[-1].upper(), file_path, extra={'log_color': 'green'}
            )

        return result_df

    return wrapper
