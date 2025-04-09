"""Label Submodule for getting labels"""

# Python Standard Library Imports
import traceback

# Local Library Imports
from ..database.model import ResearchField


__all__ = ["get_unknown_label_from_research_field"]


def get_unknown_label_from_research_field(research_field_obj: ResearchField) -> int:
    """Gets the unknown label id from a specified research field.

    Args:
        research_field_obj (ResearchField): Research field object to retrieve
        the label id from

    Raises:
        TypeError: If the input argument is not of type ResearchField

    Returns:
        int: The id of the unknown label category.
        If none is found then returns 0.
    """
    try:
        # Verifying the research field object
        if not isinstance(research_field_obj, ResearchField):
            raise TypeError("Must be of type Domain")

        # Getting the research field label map
        research_label_map = research_field_obj.label_map

        # Searching for the "Unknown label in the map"
        for label in research_label_map:
            # Checking to see if name matches unknown
            if label["name"].lower() == "unknown":
                unknown_label_id = label["id"]
                break
        else:
            # If the for loop is not broken this means there is
            # no unknown category so the id returned is 0
            return 0
        return unknown_label_id
    except (RuntimeError, TypeError, RuntimeWarning, KeyError) as error:
        traceback.print_tb(error.__traceback__)
        return None
