"""
Record for `default` usecase, 
defined https://github.com/bigbio/proteomics-sample-metadata/blob/master/templates/sdrf-default.tsv
"""

from pydantic import BaseModel, Field


class DefaultRecord(BaseModel):
    source_name: str = Field(..., alias="source name")
    technology_type: str = Field(..., alias="technology type")
    assay_name: str = Field(..., alias="assay name")
    # TODO: Add missing comments and characteristics
