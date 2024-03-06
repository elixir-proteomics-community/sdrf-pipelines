"""Module for parsing `comment[...]` parameters in the SDRF file.
"""

from sdrf_pipelines_pydantic.cells.comments.base_comment import BaseComment
from sdrf_pipelines_pydantic.cells.comments.modification_parameter_comment import ModificationParameterComment
from sdrf_pipelines_pydantic.cells.comments.undefined_comment import UndefinedComment


def from_str(comment_type: str, comment_value: str) -> BaseComment:
    """Parses a string to a `ModificationParameterComment` object.

    Arguments
    ---------
    comment_type : str
        The string from `comment[...]` in the SDRF file.
        For example: `comment[modification parameter]`.
    comment_value : str
        The value of the comment.

    Returns
    -------
    Subclass of BaseComment.

    Raises
    ------
    ValueError
        If the comment type is not recognized.
    """
    stripped_comment_type = comment_type.strip()
    stripped_comment_value = comment_value.strip()

    match comment_type.strip():
        case "comment[modification parameter]":
            return ModificationParameterComment.from_str(stripped_comment_value)
        case _:
            return UndefinedComment(alias=stripped_comment_type, value=stripped_comment_value)
