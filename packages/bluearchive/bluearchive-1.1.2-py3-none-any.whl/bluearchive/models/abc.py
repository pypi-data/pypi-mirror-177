from abc import abstractmethod, ABCMeta

from bluearchive.types import JSON


class JsonObject(metaclass=ABCMeta):
    """
    Abstract Base Class to implement json serialization / deserialization.
    """
    @classmethod
    @abstractmethod
    def from_json(cls, data: JSON) -> "JsonObject":
        """Deserialize json data and wrap it into Python Object (JsonObject).

        Args:
            data (JSON): json data.

        Returns:
            JsonObject: wrapped python object.
        """
        raise NotImplemented

    @abstractmethod
    def to_json(self) -> JSON:
        """Serialize JsonObject instance into json data.

        Returns:
            JSON: json data.
        """
        raise NotImplemented