import base64
import logging
import os
from abc import ABC
from typing import List

import py
from pydantic import BaseModel, validator

from summed.summed_platform import IPlatform, SumMedPlatform


class IUser(ABC):
    """User class, representes an (potentially authenticated) user."""

    pass


class User(BaseModel, IUser):

    platform: SumMedPlatform
    name: str

    _authenticated: bool = False

    def authenticate(self) -> bool:
        """
        Authenticate the user, and give access to available Spaces

        Returns:
            bool: True is authentication was successful, False otherwise
        """

        # TODO FIXME authenticate user and load space(s), instead of recreating everythign here
        # default_space = Space(name="default", description="Default space")
        # default_space.initialize({})

        # self.spaces = [default_space]

        self._authenticated = True

        return True

    def logout(self):
        """ """
        # self.spaces = None
        self._authenticated = False
        return True

    class Config:
        underscore_attrs_are_private = True
