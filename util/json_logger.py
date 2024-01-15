import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class __JsonLogger:
    """Logs predictions along with input to a JSON file.

    Attributes:
        file_path (str): The path to the JSON log file.
        log_entries (list): A list containing log entries loaded from the JSON file.

    Methods:
        __init__(self, logger_type: str)
            Initializes a JsonLogger instance with the specified logger type.

        __load_log_entries(self) -> list
            Loads log entries from the JSON file specified by the file_path attribute.

        __format(self, prediction: str, input_data: str)
            Formats a log entry with timestamp, prediction, and input, and appends it to log_entries.

        log(self, prediction: str, input_data: str)
            Logs a prediction along with input, updating the JSON log file.

    Example:
        # Example usage for logging false positives
        false_positive_logger = __JsonLogger(logger_type='false_positive')
        false_positive_logger.log(prediction='Some Prediction', input_data='Software Engineer')
    """

    def __init__(self, logger_type):
        log_paths = {
            "false_positive": "logs/false_positive_log.json",
            "false_negative": "logs/false_negative_log.json",
            "true_positive": "logs/true_positive_log.json",
            "true_negative": "logs/true_negative_log.json",
        }

        self.file_path = log_paths.get(logger_type)
        if not self.file_path:
            raise ValueError(f"Invalid logger_type: {logger_type}")

        self.log_entries = self.__load_log_entries()

    def __load_log_entries(self) -> list:
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def __format(self, prediction, input_data):
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": f"{prediction}",
            os.getenv("ENTRY_TEXT_TITLE"): input_data,
        }

        self.log_entries.append(log_entry)
        return

    def log(self, prediction, input_data):
        """
        Logs a prediction along with input, and updates the JSON log file to a
        JsonLogger instance's file_path.

        Args:
            prediction (str): The prediction value.
            input_data (str): The input text associated with the prediction.
        """
        self.__format(prediction, input_data)

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w") as file:
            json.dump(self.log_entries, file, indent=2)

        return


false_positive_logger = __JsonLogger("false_positive")
false_negative_logger = __JsonLogger("false_negative")
true_positive_logger = __JsonLogger("true_positive")
true_negative_logger = __JsonLogger("true_negative")
