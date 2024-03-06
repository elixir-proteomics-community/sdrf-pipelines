from typing import Dict, Tuple, Type
from unittest import TestCase

from sdrf_pipelines_pydantic.cells.comments.modification_parameter_comment import ModificationParameterComment
from sdrf_pipelines_pydantic.cells.comments.undefined_comment import UndefinedComment
from sdrf_pipelines_pydantic.cells.comments.base_comment import BaseComment
from sdrf_pipelines_pydantic.cells.comments import from_str as comment_from_str


WORKING_COMMENTS: Dict[str, Tuple[str, Type[BaseComment]]] = {
    "comment[modification parameter]": ("NT=Something; TA=S,T,Y", ModificationParameterComment),
    "comment[something very undefined]": ("Mysterious", UndefinedComment),
}
"""A dictionary of working comments. The key is the comment type and the value is the comment value.
"""


class TestCommentsModule(TestCase):
    def test_to_str(self):
        for comment_type, (comment_value, comment_class) in WORKING_COMMENTS.items():
            comment = comment_from_str(comment_type, comment_value)
            self.assertEqual(type(comment), comment_class)
