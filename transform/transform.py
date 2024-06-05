

from pydantic import BaseModel


class RendererConfig(BaseModel):
    verbose: bool = False
class BaseRenderer:
    def __init__(self, config: RendererConfig = None):
        self.config = config

    def execute(self, data):
        raise NotImplementedError("Each renderer must implement this method.")


class RendererOptions(object):
    pass
