from typing import Iterator

from citation_report import Report

from .citation import Citation, DocketCategory
from .constructors import ModelAC, ModelAM, ModelBM, ModelGR, Style
from .docket import setup_docket


def extract_citation_from_data(data: dict) -> Citation:
    """This enables creation of the Citation object from the originally scraped details.yaml
    >>> extract_citation_from_data({
        "date_prom": "1985-04-24",
        "docket": "General Register L-63915, April 24, 1985",
        "orig_idx": "GR No. L-63915",
        "phil": "220 Phil. 422",
        "scra": "136 SCRA 27",
        "offg": None,
    })
    Citation(
        docket="GR 63915, Apr. 24, 1985",
        docket_category=DocketCategory("GR"),
        docket_serial="63915",
        docket_date=datetime.date(1985, 4, 24),
        phil="220 Phil. 422",
        scra="136 SCRA 27",
        offg=None,
    )
    """

    # Create a docket string, if possible.
    try:
        cite = next(extract_citations(setup_docket(data)))
    except Exception:  # Some cases will not have a proper docket id
        cite = None

    # Gather all possible reports found within the file.
    reports = dict(
        phil=Report.extract_from_dict(data, "phil"),
        scra=Report.extract_from_dict(data, "scra"),
        offg=Report.extract_from_dict(data, "offg"),
    )

    # Recreate citation object with reports, if found.
    return Citation(
        docket=cite.docket if cite else None,
        docket_category=cite.docket_category if cite else None,
        docket_serial=cite.docket_serial if cite else None,
        docket_date=cite.docket_date if cite else None,
        **reports,
    )


def extract_citations(text: str) -> Iterator[Citation]:
    """Combine `Docket`s (which have `Reports`), and filtered `Report` models, if they exist.

    >>> text = "<em>Gatchalian Promotions Talent Pool, Inc. v. Atty. Naldoza</em>, 374 Phil 1, 10-11 (1999), citing: <em>In re Almacen</em>, 31 SCRA 562, 600 (1970).; People v. Umayam, G.R. No. 147033, April 30, 2003; <i>Bagong Alyansang Makabayan v. Zamora,</i> G.R. Nos. 138570, 138572, 138587, 138680, 138698, October 10, 2000, 342 SCRA 449; Villegas <em>v.</em> Subido, G.R. No. 31711, Sept. 30, 1971, 41 SCRA 190;"
    >>> [a.dict(exclude_none=True) for a in extract_citations(text)]
    [
        {
            "docket": "GR 147033, Apr. 30, 2003",
            "docket_category": "GR",
            "docket_serial": "147033",
            "docket_date": datetime.date(2003, 4, 30),
        },
        {
            "docket": "GR 138570, Oct. 10, 2000",
            "docket_category": "GR",
            "docket_serial": "138570",
            "docket_date": datetime.date(2000, 10, 10),
            "scra": "342 SCRA 449",
        },
        {
            "docket": "GR 31711, Sep. 30, 1971",
            "docket_category": "GR",
            "docket_serial": "31711",
            "docket_date": datetime.date(1971, 9, 30),
            "scra": "41 SCRA 190",
        },
        {"scra": "31 SCRA 562"},
        {"phil": "374 Phil. 1"},
    ]
    """
    from .helpers import filtered_reports

    def extract_report(obj):
        if isinstance(obj, Report):
            return Citation(
                docket=None,
                docket_category=None,
                docket_serial=None,
                docket_date=None,
                phil=obj.phil,
                scra=obj.scra,
                offg=obj.offg,
            )

    def extract_docket(obj):
        options = (ModelAC, ModelAM, ModelBM, ModelGR)
        if isinstance(obj, options) and obj.ids:
            return Citation(
                docket=str(obj),  # see Docket __str__
                docket_category=DocketCategory(obj.short_category),
                docket_serial=obj.serial_text,
                docket_date=obj.docket_date,
                phil=obj.phil,
                scra=obj.scra,
                offg=obj.offg,
            )

    if dockets := list(Style.extract(text)):
        if reports := list(Report.extract(text)):
            if undocketed := filtered_reports(text, dockets, reports):
                for docket in dockets:
                    if obj := extract_docket(docket):
                        if not obj.is_statute:
                            yield obj
                for report in undocketed:
                    if obj := extract_report(report):
                        yield obj
            else:
                for docket in dockets:
                    if obj := extract_docket(docket):
                        if not obj.is_statute:
                            yield obj
                for report in reports:
                    if obj := extract_report(report):
                        yield obj
        else:
            for docket in dockets:
                if obj := extract_docket(docket):
                    if not obj.is_statute:
                        yield obj
    else:
        if reports := list(Report.extract(text)):
            for report in reports:
                if obj := extract_report(report):
                    yield obj


def extract_citation(text: str) -> Citation | None:
    """If text contains a matching citation, get the first citation found."""
    try:
        return next(extract_citations(text))
    except StopIteration:
        return None
