class Pipeline:
    def __init__(self, stages=None):
        if stages:
            self.stages = stages
        else:
            self.stages = []

    def add_stage(self, renderer):
        self.stages.append(renderer)

    def execute(self, data):
        for stage in self.stages:
            data = stage.execute(data)
        return data