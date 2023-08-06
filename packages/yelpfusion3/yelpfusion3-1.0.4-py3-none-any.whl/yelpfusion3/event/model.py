"""
Model abstractions for Yelp Fusion event endpoints.
"""

from typing import Dict, List, Literal, Optional, Union

from pydantic import HttpUrl, NonNegativeInt, confloat, constr, validator

from yelpfusion3.model import Location, Model


class SupportedCategories:  # pylint: disable=too-few-public-methods
    """
    A collection of categories supported by the Yelp Fusion API's Event Search endpoint.
    See `Supported Categories <https://www.yelp.com/developers/documentation/v3/event_categories_list>`_
    """

    categories: Dict = {
        "Music": "music",
        "Visual Arts": "visual-arts",
        "Performing Arts": "performing-arts",
        "Film": "film",
        "Lectures & Books": "lectures-books",
        "Fashion": "fashion",
        "Food & Drink": "food-and-drink",
        "Festivals & Fairs": "festivals-fairs",
        "Charities": "charities",
        "Sports & Active Life": "sports-active-life",
        "Nightlife": "nightlife",
        "Kids & Family": "kids-family",
        "Other": "other",
    }

    @staticmethod
    def contains(value: constr(strip_whitespace=True, to_lower=True, min_length=1)) -> bool:
        """
        Checks that ``value`` is a category supported by the Yelp Fusion API's Event search endpoint.

        :param value: The category alias to check.
        :type value: str
        :return: True if the category alias is supported.
        :rtype: bool
        """
        return value in SupportedCategories.categories.values()


class Event(Model):
    """
    Detailed information for a specific Yelp event.
    """

    attending_count: Optional[NonNegativeInt] = None
    """
    Number of Yelp users attending this event.
    """

    category: Optional[str] = None
    """
    The category of this event.
    """

    cost: Optional[confloat(ge=0.0)] = None
    """
    Cost of attending this event.
    """

    cost_max: Optional[confloat(ge=0.0)] = None
    """
    Maximum cost of attending this event.
    """

    description: Optional[str] = None
    """
    Detailed description of this event.
    """

    event_site_url: Optional[HttpUrl] = None
    """
    Yelp page of this event.
    """

    id: Optional[constr(min_length=1)] = None
    """
    Event id.
    """

    image_url: Optional[HttpUrl] = None
    """
    Yelp image URL of this event.
    """

    interested_count: Optional[NonNegativeInt] = None
    """
    Number of Yelp users interested in attending this event.
    """

    is_canceled: Optional[bool] = None
    """
    Whether this event is canceled.
    """

    is_free: Optional[bool] = None
    """
    Whether this event is free.
    """

    is_official: Optional[bool] = None
    """
    Whether this event is created by a Yelp community manager.
    """

    latitude: Optional[confloat(ge=-90.0, le=90.0)] = None
    """
    Latitude of this event.
    """

    longitude: Optional[confloat(ge=-180.0, le=180.0)] = None
    """
    Longitude of this event.
    """

    name: Optional[constr(min_length=1)] = None
    """
    Name of this event.
    """

    tickets_url: Optional[Union[HttpUrl, Literal[""]]] = None
    """
    URL to buy tickets for this event.
    """

    time_end: Optional[str]
    """
    Time this event ends. Returns date and time in ISO 8601 format: ``YYYY-MM-DDTHH:MM:SS+HH:MM``.
    """

    time_start: Optional[str] = None
    """
    Time this event starts. Returns date and time in ISO 8601 format: ``YYYY-MM-DDTHH:MM:SS+HH:MM``.
    """

    location: Optional[Location] = None
    """
    Location object of the event. Includes address, city, state, zip code and country.
    """

    business_id: Optional[constr(min_length=1)] = None
    """
    Yelp Business ID of this event. No ID is returned if a business is not associated with an event.
    """

    @validator("category")
    def _check_category(cls, value: str) -> str:  # pylint: disable=E0213
        """
        Checks that ``value`` is a supported category.

        :param value: Category alias.
        :type value: str
        :raise ValueError: If the category is unsupported.
        :return: The category alias.
        :rtype: str
        """

        # We could have done the validation in the "regex" argument to constr(), but it would be a lot more complicated
        # and not very readable.
        if SupportedCategories.contains(value):
            return value

        raise ValueError("'category' is set to an unsupported category.")


class EventSearch(Model):
    """
    Events returned by :py:class:`~yelpfusion3.event.endpoint.EventSearchEndpoint`.
    """

    total: int
    """
    Total number of events returned based on search criteria.
    """

    events: List[Event]
    """
    List of events found matching search criteria.
    """
