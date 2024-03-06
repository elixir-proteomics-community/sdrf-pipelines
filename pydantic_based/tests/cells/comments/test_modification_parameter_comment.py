"""Tests for the ModificationParameterComment class.
"""

from unittest import TestCase
from pydantic import ValidationError
from sdrf_pipelines_pydantic.cells.comments.modification_parameter_comment import ModificationParameterComment

ONLY_MANDATORY: str = "NT=Something; TA=S,T,Y"
MISSING_NT: str = "TA=M"
MISSING_TA: str = "NT=Something"
CHEMICAL_FORMULA_AND_MONO_MASS: str = "NT=Something; TA=S,T,Y; CF=H2O; MM=1"
MT_TEMPLATE: str = "NT=Something; TA=S,T,Y; MT=<MT>"
NOT_ALLOWED_MT: str = "NT=Something; TA=S,T,Y; MT=NotAllowed"
PP_TEMPLATE: str = "NT=Something; TA=S,T,Y; PP=<PP>"
NOT_ALLOWED_PP: str = "NT=Something; TA=S,T,Y; PP=NotAllowed"


class TestModificationParameterComment(TestCase):
    def test_from_str_only_mandatory(self):
        mod = ModificationParameterComment.from_str(ONLY_MANDATORY)
        self.assertEqual(mod.name, "Something")
        self.assertEqual(mod.target_amino_acid, ["S", "T", "Y"])

    def test_from_str_missing_nt(self):
        self.assertRaises(ValidationError, ModificationParameterComment.from_str, MISSING_NT)

    def test_from_str_missing_ta(self):
        self.assertRaises(ValidationError, ModificationParameterComment.from_str, MISSING_TA)

    def test_from_str_chemical_formula_and_mono_mass(self):
        """
        Makes sure that the monoisotopic mass is calculated from the chemical formula.
        """
        mod = ModificationParameterComment.from_str(CHEMICAL_FORMULA_AND_MONO_MASS)
        self.assertEqual(mod.monoisotopic_mass, 18.0105646837)

    def test_allowed_modification_types(self):
        for mod_type in ["Fixed", "Variable", "Annotated"]:
            mod = ModificationParameterComment.from_str(MT_TEMPLATE.replace("<MT>", mod_type))
            self.assertEqual(mod.modification_type, mod_type)

    def test_not_allowed_modification_types(self):
        self.assertRaises(ValidationError, ModificationParameterComment.from_str, NOT_ALLOWED_MT)

    def test_allowed_positions(self):
        for mod_type in ["Anywhere", "Protein N-term", "Protein C-term", "Any N-term", "Any C-term"]:
            mod = ModificationParameterComment.from_str(PP_TEMPLATE.replace("<PP>", mod_type))
            self.assertEqual(mod.position, mod_type)

    def test_not_allowed_positions(self):
        self.assertRaises(ValidationError, ModificationParameterComment.from_str, NOT_ALLOWED_PP)

    def test_demo_error_print(self):
        """Just a demo to see which information we can get from the ValidationError and how to print.
        TODO: Put the formatting ing some sort of helper function.
        """
        try:
            ModificationParameterComment.from_str(NOT_ALLOWED_PP)
        except ValidationError as e:
            for error in e.errors(include_input=True):
                print(f"{error['msg']}, incorrect attribute `{error['input']}` in `{NOT_ALLOWED_PP}`")
