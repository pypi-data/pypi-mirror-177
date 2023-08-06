"""
Application-wide repository for shared configuration settings.
"""

from typing import Optional

from pydantic import BaseSettings, Field, HttpUrl, parse_obj_as


class Settings(BaseSettings):
    """
    Centralized settings repository using Pydantic's BaseSettings abstraction.
    """

    api_key: Optional[str] = Field(default=None, env="YELP_API_KEY")
    base_url: HttpUrl = parse_obj_as(HttpUrl, "https://api.yelp.com/v3")

    @property
    def headers(self) -> dict:
        """
        Creates a dictionary containing prepopulated request header fields for Yelp Fusion endpoints.
        :return:
        """
        return {"Authorization": f"Bearer {self.api_key}"}
