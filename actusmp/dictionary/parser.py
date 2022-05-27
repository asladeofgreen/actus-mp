def parse(obj: dict):
    """Parses ACTUS dictionary so as to simplify upstream processing consistency.
    
    """
    _parse_term_default(obj)
    _parse_term_scaling_effect(obj)

    return obj


def _parse_term_default(obj: dict):
    """Parses a term default declaration.
    
    """
    for term_id in obj["terms"]:
        term: dict = obj["terms"][term_id]
        if term["default"] == "":
            term["default"] = None
        else:
            term["default"] = term["default"].strip()


def _parse_term_scaling_effect(obj: dict):
    """Parses a term declaration: scaling effect.
    
    """
    term: dict = obj["terms"]["scalingEffect"]
    term["default"] = "OOO"

    _ACRONYMS = {
        "000": "OOO",
        "I00": "IOO",
        "0N0": "ONO",
        "IN0": "INO",
    }
    for val in term["allowedValues"]:
        val["acronym"] = _ACRONYMS[val["acronym"]]

    obj["terms"]["scalingEffect"] = term
