from datetime import datetime

class Commit:
    def __init__(self, message):
        self.hash_commit = hash(message)
        self.message = message
        self.date = datetime.now().strftime("%Y-%M-%D %H:%M:%S:")

    def __str__(self):
        return f"Commit(hash_commit={self.hash_commit}, message={self.message}, date={self.date})"
