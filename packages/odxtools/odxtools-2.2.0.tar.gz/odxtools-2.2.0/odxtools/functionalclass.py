# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH

from dataclasses import dataclass
from typing import Optional, List

from .utils import read_description_from_odx
from .odxlink import OdxLinkId, OdxDocFragment


@dataclass()
class FunctionalClass:
    """
    Corresponds to FUNCT-CLASS.
    """
    odx_id: OdxLinkId
    short_name: str
    long_name: Optional[str] = None
    description: Optional[str] = None


def read_functional_class_from_odx(et_element, doc_frags: List[OdxDocFragment]):
    short_name = et_element.findtext("SHORT-NAME")
    odx_id = OdxLinkId.from_et(et_element, doc_frags)
    assert odx_id is not None

    long_name = et_element.findtext("LONG-NAME")
    description = read_description_from_odx(et_element.find("DESC"))

    return FunctionalClass(odx_id=odx_id,
                           short_name=short_name,
                           long_name=long_name,
                           description=description)
