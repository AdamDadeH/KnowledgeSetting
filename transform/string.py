from transform.transform import BaseRenderer


class StringToFile(BaseRenderer):

    def __init__(self, output_path: str):
        self.output_path = output_path
        super().__init__()

    def execute(self, string: str):
        with open(self.output_path, 'w') as f:
            f.write(string)
        return self.output_path
