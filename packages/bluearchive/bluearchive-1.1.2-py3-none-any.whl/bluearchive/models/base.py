from abc import ABCMeta
from typing import Final

import attr

from bluearchive.models.abc import JsonObject


@attr.s
class BlueArchiveObject(JsonObject, metaclass=ABCMeta):
    """
    Abstract Base class for all Blue Archive objects.
    """
    id: Final[int] = attr.field()       # id of this object.

