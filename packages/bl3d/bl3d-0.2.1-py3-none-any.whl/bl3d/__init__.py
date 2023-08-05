# bl3d --- Domain Driven Design library
# Copyright © 2022 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any, Optional, Type, TypeVar

import pkg_resources

__version__ = pkg_resources.get_distribution(__name__).version


TypeDateAndTime = TypeVar("TypeDateAndTime", bound="DateAndTime")
TypeDate = TypeVar("TypeDate", bound="Date")
TypeDuration = TypeVar("TypeDuration", bound="Duration")
TypeFloat = TypeVar("TypeFloat", bound="Float")
TypeInteger = TypeVar("TypeInteger", bound="Integer")
TypeString = TypeVar("TypeString", bound="String")


class InvalidValue(ValueError):
    def __init__(self, classname: str, message: str) -> None:
        super().__init__(f"Invalid value for `{classname}`: {message}")


@dataclass
class ValueObject(ABC):
    """An object whose equality is not based on identity by on value.

    It **MUST** contains an `instanciate` method that validates
    business rules and return a valid value object.
    Unfortunatly, the signature of this method will depend on the
    value objet considered and cannot hard coded with a
    `@abstractmethod`.

    The business rules **SHOULD** not be verified when loading an object
    that was persisted and `__init__` should be used instead.
    """

    NAME = ""

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Two different value objects with the same values are considered equal."""
        ...


@dataclass
class String(ValueObject):
    MIN: Optional[int] = None
    MAX: Optional[int] = None

    @classmethod
    def instanciate(cls: Type[TypeString], value: str) -> TypeString:
        if cls.MIN is not None and len(value) < cls.MIN:
            raise InvalidValue(
                cls.__name__,
                f"This string is too short. [value={value}, min={cls.MIN}]",
            )
        if cls.MAX is not None and len(value) > cls.MAX:
            raise InvalidValue(
                cls.__name__, f"This string is too long. [value={value}, max={cls.MAX}]"
            )
        return cls(value)

    def __init__(self, value: str) -> None:
        self.__value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, String):
            return NotImplemented

        return other.__value == self.__value

    def __str__(self) -> str:
        return self.__value


@dataclass
class Integer(ValueObject):
    MIN: Optional[int] = None
    MAX: Optional[int] = None

    @classmethod
    def instanciate(cls: Type[TypeInteger], value: int) -> TypeInteger:
        if cls.MIN is not None and value < cls.MIN:
            raise InvalidValue(
                cls.__name__, f"Value is too small. [value={value}, min={cls.MIN}]"
            )
        if cls.MAX is not None and value > cls.MAX:
            raise InvalidValue(
                cls.__name__, f"Value is too big. [value={value}, max={cls.MAX}]"
            )
        return cls(value)

    def __init__(self, value: int) -> None:
        self.__value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Integer):
            return NotImplemented

        return other.__value == self.__value

    def __str__(self) -> str:
        return str(self.__value)

    def __int__(self) -> int:
        return self.__value


@dataclass
class Float(ValueObject):
    MIN: Optional[float] = None
    MAX: Optional[float] = None

    @classmethod
    def instanciate(cls: Type[TypeFloat], value: float) -> TypeFloat:
        if cls.MIN is not None and value < cls.MIN:
            raise InvalidValue(
                cls.__name__, f"Value is too small. [value={value}, min={cls.MIN}]"
            )
        if cls.MAX is not None and value > cls.MAX:
            raise InvalidValue(
                cls.__name__, f"Value is too big. [value={value}, max={cls.MAX}]"
            )
        return cls(value)

    def __init__(self, value: float) -> None:
        self.__value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Float):
            return NotImplemented
        return other.__value == self.__value

    def __str__(self) -> str:
        return str(self.__value)

    def __float__(self) -> float:
        return self.__value


@dataclass
class Date(ValueObject):
    @classmethod
    def instanciate(cls: Type[TypeDate], value: date) -> TypeDate:
        return cls(value)

    def __init__(self, value: date) -> None:
        self.__value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            return NotImplemented
        return other.__value == self.__value

    def to_date(self) -> date:
        return date(self.__value.year, self.__value.month, self.__value.day)

    def format(self, fmt: str) -> str:
        return self.__value.strftime(fmt)


@dataclass
class DateAndTime(ValueObject):
    @classmethod
    def instanciate(cls: Type[TypeDateAndTime], value: datetime) -> TypeDateAndTime:
        if not value.tzinfo:
            raise InvalidValue(cls.__name__, "Must define a timezone.")
        return cls(value)

    def __init__(self, value: datetime) -> None:
        self.__value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DateAndTime):
            return NotImplemented
        return other.__value == self.__value

    def to_datetime(self) -> datetime:
        return self.__value.replace()

    def format(self, fmt: str) -> str:
        return self.__value.strftime(fmt)


@dataclass
class Duration(ValueObject):
    @classmethod
    def instanciate(cls: Type[TypeDuration], value: timedelta) -> TypeDuration:
        if value.total_seconds() < 0:
            raise InvalidValue(cls.__name__, "Cannot be negative.")
        return cls(value)

    @classmethod
    def hours(cls: Type[TypeDuration], value: float) -> TypeDuration:
        return cls.instanciate(timedelta(hours=value))

    def __init__(self, value: timedelta) -> None:
        self.__value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented

        return other.__value == self.__value

    def to_hours(self) -> float:
        return float(self.__value.total_seconds() / 60 / 60)


class Entity(ABC):
    """A domain concept with an identity.

    They have methods that implement business rules and behaviour.
    Those methods mutate the state of the entity and emit events
    reflecting the changes.

    In Python, there is no way to "emit" events, so they are returned
    by the methods. But they are not, so to speak, return values.
    """

    pass


@dataclass(frozen=True)
class EntityState(ABC):
    """The state of an entity.

    A new state is created by applying an domain event to it.
    """

    class UnknownEvent(Exception):
        pass

    class IncompatibleVersions(Exception):
        pass

    version: int


@dataclass(frozen=True)
class DomainEvent(ABC):
    """An event that happened in the domain."""

    version: int

    @abstractproperty
    def entity_unique_identifier(self) -> str:
        """An identifier that uniquely identifies the entity
        that emitted the domain event.
        """
        ...


class History(ABC):
    """A sequence of events that happened inside the domain."""

    class EvenNotHandled(NotImplementedError):
        def __init__(self, name: str) -> None:
            super().__init__(f"History cannot handle event `{name}`!")

    class ReadError(AttributeError):
        def __init__(self, name: str, data: dict[str, Any]) -> None:
            super().__init__(f"Cannot read event's data `{name}`: {data}")

    @abstractmethod
    def read(self, stream: str) -> list[DomainEvent]:
        ...

    @abstractmethod
    def __lshift__(self, domain_events: list[DomainEvent]) -> None:
        ...
