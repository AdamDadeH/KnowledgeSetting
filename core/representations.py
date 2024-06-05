from pydantic import BaseModel
from typing import Union

class FilePath(BaseModel):
    path: str

class StringData(BaseModel):
    data: str

class PdfFile(FilePath):
    pass

class HtmlFile(FilePath):
    pass

class MarkdownFile(FilePath):
    pass

class MarkdownString(StringData):
    pass

# Additional file types as needed
