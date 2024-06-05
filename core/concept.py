"""
Content : Internal representation of elementary block of information.
"""
from pydantic import BaseModel, validator, ValidationError
from typing import Union, Callable, Tuple, List, Dict, Optional

from core.content_log import ContentLogData

ContentFunction = Callable[[Tuple[str, ...]], str]

class ConceptRepresentation(BaseModel):
    type: str
    content: Union[str, ContentFunction]

    @validator('content', pre=True, allow_reuse=True)
    def validate_content(cls, value):
        if isinstance(value, str) or callable(value):
            return value
        else:
            raise ValueError("Content must be either a string or a callable function.")


class ConceptBase:


    def get_title(self):
        pass
    def get_type(self):
        pass
    def get_concept(self, **kwargs):
        pass


class Concept(ConceptBase):
    """
    Content is the internal representation of an elementary block of information.

    Parameters
    - title
    - inline name
    - inline (method)
    - error data

    """

    def __init__(
        self,
        content_type: str,
        name: str,
        content: str,
        instance_rep="Missing",
        inline_content="Missing",
        errors=ContentLogData(),
    ):
        self.content_type = content_type
        self.name = name
        self.inline_name = instance_rep
        self.content = content
        self.inline_content = inline_content
        self.errors = errors

    @classmethod
    def default_from_name(cls, name):
        """
        Generate a dummy content from title only.
        :param name: name of content
        :return:
        """
        return cls.from_title_content(name, name)

    @classmethod
    def from_title_content(cls, title, content):
        return Concept(
            content_type="unknown",
            name=title,
            content=content,
            instance_rep=build_inline_constant(title),
            inline_content=build_inline_constant(content),
        )

    def get_title(self):
        return self.name

    def get_type(self):
        return self.content_type.capitalize()

    def get_concept(self, **kwargs):
        return self.content

    def __str__(self):
        return f"{self.name} : {self.content}"

    def __repr__(self):
        return f"{self.name} : {self.content}"


def build_inline_constant(string_rep):
    def get_md(args):
        return string_rep

    return get_md


def build_inline_method(string_rep, arg_names, arg_defaults):
    """

    :param string_rep:
    :param arg_names:
    :return:
    """

    def get_md(args):
        output = string_rep
        arg_count = len(args)
        for (ix, arg_name) in enumerate(arg_names):
            if ix >= arg_count and arg_defaults[ix] == None:
                print("Error : No default for {}".format(arg_names))
            elif ix >= arg_count:
                output = output.replace("∆{}".format(arg_name), arg_defaults[ix])
            else:
                output = output.replace("∆{}".format(arg_name), args[ix])

        return output

    return get_md
