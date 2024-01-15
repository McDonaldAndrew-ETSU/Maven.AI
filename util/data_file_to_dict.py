import os
from dotenv import load_dotenv

load_dotenv()


def data_file_to_dict(path: str):
    """
    Handles .txt file parsing to a python dict object

    Args:
        path (str): the file path to the data set

    Returns:
        dict: An array of strings
    """
    try:
        # 1. Open the file in read mode
        with open(path, "r") as file:
            # 1.1. Read the file and split it into lines
            lines = file.readlines()

        # 2. Remove newline characters from each line and create an array of string objects
        array_of_strings = [line.strip() for line in lines]

        return array_of_strings
    except FileNotFoundError as e:
        print(e)
        # 3. Return an empty array if file is not found
        return []
