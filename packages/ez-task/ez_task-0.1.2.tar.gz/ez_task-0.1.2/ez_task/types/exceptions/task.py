
class TaskRunFailed(Exception):
    def __init__(self, message='Task failed to run'):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
    pass