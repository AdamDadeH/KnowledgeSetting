from transform.transform import RendererOptions, BaseRenderer


class LinearRendererOptions(RendererOptions):
    def __init__(self, to_substitute):
        self.to_substitute = to_substitute


class IllegalCharCheck(BaseRenderer):

    def __init__(self, char):
        self.char = char

    def execute(self, data):
        for line in data.split("\n"):
            if self.char in line:
                raise Exception(f"Illegal character ${self.char} in output")
        return data

class UnmatchedBracket(BaseRenderer):

    def __init__(self, left_bracket, right_bracket):
        self.left_bracket = left_bracket
        self.right_bracket = right_bracket

    def execute(self, data):
        for line in data.split("\n"):
            if self.left_bracket!=self.right_bracket and line.count(self.left_bracket) != line.count(self.right_bracket):
                print("Non terminated latex math in line : {}".format(line))
            elif line.count(self.left_bracket)%2 != 0:
                print("Non terminated latex math in line : {}".format(line))
        return data
