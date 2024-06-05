"""
ContentLog collects errors during the parsing & construction of Content
instances.
"""


class ContentLogData:
    """
    Error, Warnings, Debug messages associated to a specific piece of content.
    """

    def __init__(self):
        self.warnings = []
        self.errors = []

    def warn(self, message):
        """Raise warning"""
        self.warnings.append(message)

    def error(self, message):
        """Raise error"""
        self.errors.append(message)

    def log(self, message, severity):
        """
        Log message with given severity.
        :param message:
        :param severity:
        :return:
        """
        if severity == "error":
            self.error(message)
        elif severity == "warn":
            self.warn(message)
        else:
            raise Exception("Unknown error type {}".format(severity))
