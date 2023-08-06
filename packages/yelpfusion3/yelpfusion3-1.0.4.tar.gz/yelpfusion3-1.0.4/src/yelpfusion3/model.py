"""
Shared data models used by multiple Yelp Fusion v3 endpoints.
"""

from typing import List, Optional

import pycountry
from pydantic import BaseModel, constr, validator


class Model(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Basic base class for all model implementations.
    """

    class Config:  # pragma: no cover   pylint: disable=C0115,too-few-public-methods
        anystr_strip_whitespace = True
        min_anystr_length = 0
        validate_assignment = True


class Location(Model):
    """
    The location of a business or event, including address, city, state, zip code and country.
    """

    address1: Optional[str] = None
    """
    Street address of this business or event.
    """

    address2: Optional[str] = None
    """
    Street address of this business or event, continued.
    """

    address3: Optional[str] = None
    """
    Street address of this business or event, continued.
    """

    city: str
    """
    City of this business or event.
    """

    state: constr(to_upper=True, min_length=2, max_length=3)
    """
    ISO 3166-2 (with a few exceptions) state code of this business or event.
    """

    zip_code: str
    """
    Zip code of this business or event.
    """

    country: constr(to_upper=True, min_length=2, max_length=3)
    """
    ISO 3166-1 alpha-2 country code of this business or event.
    """

    display_address: List[str]
    """
    Array of strings that if organized vertically give an address that is in the standard address format for the
    business or event's country.
    """

    cross_streets: Optional[str] = None
    """
    Cross streets for this business or event. (Only used in business or event details search results.)
    """

    @validator("country")
    def _check_country(cls, value: str) -> str:  # pylint: disable=E0213
        """
        Checks that ``value`` is a valid ISO 3166- alpha-2 country code.

        :param value: Two-letter country code.
        :type value: str
        :raise ValueError: If ``value`` is an invalid country code.
        :return: ``value`` if it passes validation.
        :rtype: str
        """

        if pycountry.countries.get(alpha_2=value):
            return value
        raise ValueError("Not a valid ISO 3166-1 alpha-2 country code.")
