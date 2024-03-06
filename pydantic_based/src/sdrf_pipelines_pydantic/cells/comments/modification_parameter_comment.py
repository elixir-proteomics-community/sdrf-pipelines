""" 
Implementation of the ModificationParameterComment class and 
related type aliases and information to parse `comment[modification parameter]`
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import Field
from pyteomics.mass import calculate_mass

from sdrf_pipelines_pydantic.cells.comments.base_comment import BaseComment

SUPPORTED_MOD_TYPE = Literal["Fixed", "Variable", "Annotated"]
""" Type alias for allowed modification types.
"""

SUPPORTED_POSITION = Literal["Anywhere", "Protein N-term", "Protein C-term", "Any N-term", "Any C-term"]
""" Type alias for allowed modification positions.
"""


class ModificationParameterComment(BaseComment):
    """
    See https://github.com/bigbio/proteomics-sample-metadata/tree/master/sdrf-proteomics#1021-protein-modifications
    for more information.
    """

    # mandatory
    name: str = Field(..., serialization_alias="NT", min_length=1)
    """ Name of the modification.
    """
    target_amino_acid: List[str] = Field(..., serialization_alias="TA", min_length=1)
    """ Target Amino acid
    """
    # optional
    accession: Optional[str] = Field(..., serialization_alias="AC")
    """ Accession number of the modification.
    """
    chemical_formula: Optional[str] = Field(..., serialization_alias="CF")
    """ Chemical formula of the modification.
    """
    modification_type: Optional[SUPPORTED_MOD_TYPE] = Field(..., serialization_alias="MT")
    """ Modification type.
    """
    position: Optional[SUPPORTED_POSITION] = Field(..., serialization_alias="PP")
    """ Position of the modification in the Polypeptide
    """
    monoisotopic_mass: Optional[float] = Field(..., serialization_alias="MM", min_digits=5)
    """ Monoisotopic mass of the modification.
    """
    target_site: Optional[str] = Field(..., serialization_alias="TS")
    """ Target site of the modification.
    """

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        # Make sure chemical_formula is used for calculating monoisotopic mass if it is present
        if self.chemical_formula is not None:
            self.monoisotopic_mass = calculate_mass(self.chemical_formula)

    @classmethod
    def from_str(cls, s: str) -> "ModificationParameterComment":
        """
        Create a ModificationParameterComment from a string like: `NT=Oxidation; MT=Variable; TA=M`

        Arguments
        ---------
        s : str
            The string to parse.

        Returns
        -------
        ModificationParameterComment
            The parsed ModificationParameterComment.

        Raises
        ------
        ValueError
            If the string is not in the expected format.
        """

        items: List[str] = s.split(";")
        pairs: List[List[str]] = [item.split("=") for item in items]

        for pair in pairs:
            if len(pair) != 2:
                raise ValueError(f"Invalid pair: `{pair}` in modification `{s}`")

        attributes: Dict[str, Any] = {key.strip(): value.strip() for key, value in pairs}
        # Split the target amino acid list, and remove any empty strings
        attributes["TA"] = list(
            filter(lambda target: len(target) > 0, [target.strip() for target in attributes.get("TA", "").split(",")])
        )

        return cls(
            name=attributes.get("NT", ""),
            target_amino_acid=attributes.get("TA", None),
            accession=attributes.get("AC", None),
            chemical_formula=attributes.get("CF", None),
            modification_type=attributes.get("MT", None),
            position=attributes.get("PP", None),
            monoisotopic_mass=attributes.get("MM", None),
            target_site=attributes.get("TS", None),
        )
