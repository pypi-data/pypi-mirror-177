import datetime
from enum import Enum

from pydantic import BaseModel, Field, root_validator
from slugify import slugify

from .constructors import Style
from .exceptions import CitationBasedStatutes


class DocketCategory(str, Enum):
    """
    Each Philippine Supreme Court docket citation can be classified under the following:

    1. General Register (`GR`)
    2. Administrative Matter (`AM`)
    3. Administrative Case (`AC`)
    4. Bar Matter (`BM`)
    """

    GR = Style.GR.value.short_category
    AM = Style.AM.value.short_category
    AC = Style.AC.value.short_category
    BM = Style.BM.value.short_category


class Citation(BaseModel):
    """
    # Concept
    Based on a cursory overview of various Supreme Court decisions that cite or refer to other Supreme Court decisions, there are two main modes of identifying a unique decision:

    1. docket; and
    2. report.

    ## Docket
    A docket is a combination of a category, serial number, and a date.

    The rationale for the combination is that some decisions have the same category and serial number and thus needs to be distinguished by the date of their issuance.

    ## Report
    A report consists of a volume number, an identifying acronym of the reporter, and the page of the reported volume.

    There are 3 main reporters:
    - Philippine Reports (`phil`)
    - Supreme Court Reports Annotated (`scra`)
    - Official Gazette (`offg`)

    ## Technical Notes
    - The col and index fields are populated in anticipation of future use via the `sqlpyd` library.
    - The `@slug` is a possible primary key based on consolidated fields.
    """

    docket_category: DocketCategory | None = Field(
        None,
        title="Docket Category",
        description="Common categories of PH Supreme Court decisions.",
        col=str,
        index=True,
    )
    docket_serial: str | None = Field(
        None,
        title="Docket Serial Number",
        description="Serialized identifier of the decision, based on the docket category.",
        col=str,
        index=True,
    )
    docket_date: datetime.date | None = Field(
        None,
        title="Docket Date",
        description="Can distinguish similarly serialized decisions.",
        col=datetime.date,
        index=True,
    )
    docket: str | None = Field(
        None,
        title="Docket Reference",
        description="Cleaned docket based on the contents of the itemized docket parts: category, serial, and date.",
        col=str,
        index=True,
    )
    phil: str | None = Field(
        None,
        title="Philippine Reports",
        col=str,
        index=True,
    )
    scra: str | None = Field(
        None,
        title="Supreme Court Reports Annotated",
        col=str,
        index=True,
    )
    offg: str | None = Field(
        None,
        title="Official Gazette",
        col=str,
        index=True,
    )

    class Config:
        use_enum_values = True
        anystr_strip_whitespace = True

    @property
    def is_statute(self) -> bool:
        """This flag is a special rule to determine whether a combination of category and serial number would qualify the citation instance as a statutory pattern rather than a decision pattern."""
        if self.docket_category:
            if self.docket_category == DocketCategory.BM:
                if bm_text := self.docket_serial:
                    if CitationBasedStatutes.BAR.pattern.search(bm_text):
                        return True
        return False

    @property
    def has_citation(self):
        """Since each field may be null, check if at least one is not null for it be considered a valid citation object."""
        els = [self.docket, self.scra, self.phil, self.offg]
        values = [el for el in els if el is not None]
        return values

    @property
    def display(self):
        """Combine citation strings into a descriptive string."""
        if self.has_citation:
            return ", ".join(self.has_citation)
        return "No citation detected."

    @property
    def slug(self) -> str | None:
        """If any of the possible values are present, convert this instance into a slug that can serve as a primary key."""
        if self.has_citation:
            return slugify(" ".join(self.has_citation)).strip()
        return None
