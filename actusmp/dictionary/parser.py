
def parse(obj: dict):
    """Parses ACTUS dictionary so as to simplify upstream processing consistency.

    """
    _parse_contract_reference_enums(obj)
    _parse_contract_types(obj)
    _parse_term_default(obj)
    _parse_term_scaling_effect(obj)

    return obj


def _parse_contract_reference_enums(obj: dict):
    """Parses contract reference enum declarations.

    """
    obj["contractReference"]["role"]["identifier"] = "referenceRole"
    obj["contractReference"]["type"]["identifier"] = "referenceType"


def _parse_contract_types(obj: dict):
    """Parses contract type declarations.

    """
    # Collection of unsupported contract types.
    unsupported = []

    # Iterate taxonomy and cache unsupported.
    for taxonomy_item in obj["taxonomy"].values():
        # Exclude ill-defined.
        if taxonomy_item["acronym"] == "EXOTi":
            continue

        # Determine whether in taxonomy but not in terms.
        is_defined = False
        for contract_type in obj["terms"]["contractType"]["allowedValues"]:
            if taxonomy_item["acronym"] == contract_type["acronym"]:
                is_defined = True
                break

        # If not defined in terms then add to collection.
        if not is_defined:
            unsupported.append(taxonomy_item)

    # Extend contract type enum but set option to a negative number.
    for idx, item in enumerate(sorted(unsupported, key=lambda i: i["acronym"])):
        obj["terms"]["contractType"]["allowedValues"].append({
            "option": -idx - 1,
            "identifier": item["identifier"],
            "name": item["name"],
            "acronym": item["acronym"].upper(),
            "description": item["description"]
        })


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
