from analyze import *

class Alert:
    def __init__(self, input_file, filename):
        self.file = input_file.read().decode('utf-8')
        self.filename = filename

    def get_alerts(self):
        alerts = list()

        dict_problems["functions_length"] = 0
        dict_problems["file_length"] = 0
        dict_problems["find_unused_variables"] = 0
        dict_problems["find_missing_docstrings"] = 0

        get_functions_length(self.file)
        get_file_length(self.file)
        get_find_unused_variables(self.file)
        get_find_missing_docstrings(self.file)

        # הדפסת שם הקובץ
        title = f"Checking file: {self.filename}:"
        alerts.append(title)

        if dict_problems["functions_length"] > 0:
            res = f"Warning: {dict_problems['functions_length']} functions exceed 20 lines."
            alerts.append(res)

        if dict_problems["file_length"] > 0:
            res = f"Warning: The file exceeds 200 lines."
            alerts.append(res)

        if dict_problems["find_unused_variables"] > 0:
            res = f"Warning: {dict_problems['find_unused_variables']} unused variables found."
            alerts.append(res)

        if dict_problems["find_missing_docstrings"] > 0:
            res = f"Warning: {dict_problems['find_missing_docstrings']} functions are missing docstrings."
            alerts.append(res)

        # Resetting the problem dictionary for future checks
        for key in dict_problems:
            dict_problems[key] = 0

        return alerts
