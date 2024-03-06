"""Implementation for unrestricted comments
"""

from pydantic import Field

from sdrf_pipelines_pydantic.cells.comments.base_comment import BaseComment


class UndefinedComment(BaseComment):
    """
    Comments allow free text to be added to the SDRF file.
    This class is used when the comment type is not recognized.
    """

    alias: str = Field(..., min_length=1)
    """ Alias/Column name for the comment.
    """

    value: str = Field(..., min_length=1)
    """ The value of the comment.
    """
