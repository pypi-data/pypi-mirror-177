from citation_docket.simple_matcher import updated_cat_idx
from dateutil.parser import parse

from .citation import DocketCategory
from .constructors import DOCKET_DATE_FORMAT


def setup_docket(raw: dict) -> str:
    """Assumes the previous creation of details.yaml file which can be deserialized to a `raw` dictionary containing relevant keys."""

    def formalize(cat: str, idx: str):
        for category in DocketCategory:
            if cat.lower() == category.value.lower():
                return f"{category.name} No. {idx}"
        raise Exception(f"Invalid {cat=}{idx=}")

    def get_partial_docket(detail: dict):
        _p = updated_cat_idx(detail)
        if _p and "cat" in _p and "idx" in _p:
            return formalize(_p["cat"], _p["idx"])
        raise ValueError(f"No cat/idx from {detail=}")

    def decode_docket(text: str):
        """The details.yaml file uses a custom 'General Register' format that needs to be updated. Until then, can adjust by making a replacement prior to extraction."""
        if text.startswith("General Register"):
            return text.replace("General Register", "G.R. No.")
        elif text.startswith("Administrative Matter"):
            return text.replace("Administrative Matter", "A.M. No.")
        elif text.startswith("Administrative Case"):
            return text.replace("Administrative Case", "A.C. No.")
        elif text.startswith("Bar Matter"):
            return text.replace("Bar Matter", "B.M. No.")
        return text

    if "date_prom" not in raw:
        raise ValueError(f"No docket without date from {raw=}")
    if "docket" not in raw and "orig_idx" not in raw:
        raise ValueError(f"Docket or orig_idx needed in {raw=}")
    if raw.get("docket"):  # Legacy decisions have a matching docket key.
        return decode_docket(raw["docket"])
    try:
        d = parse(raw["date_prom"]).date()
        return f"{get_partial_docket(raw)}, {d.strftime(DOCKET_DATE_FORMAT)}"
    except Exception as e:
        raise ValueError(f"Unexpected docket/date; {e=}")
