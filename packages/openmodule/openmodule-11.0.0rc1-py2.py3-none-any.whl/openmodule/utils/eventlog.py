from datetime import datetime
from enum import Enum
from typing import Optional, Dict

from pydantic import validator

from openmodule.core import core
from openmodule.models.base import OpenModuleModel, ZMQMessage, timezone_validator


class AnonymizationType(str, Enum):
    lpr = "lpr"  # anonymize to "***AB"
    medium = "medium"  # anonymize if linked to a session
    default = "default"  # anonymize ":anonymize:" -> display with anonymize icon
    no = "no"


class MessageKwarg(OpenModuleModel):
    value: str
    anonymization_type: AnonymizationType = AnonymizationType.default
    format_type: str

    @staticmethod
    def lpr(value):
        return MessageKwarg(value=value, format_type="lpr", anonymization_type=AnonymizationType.lpr)

    @staticmethod
    def medium(value):
        return MessageKwarg(value=value, format_type="medium", anonymization_type=AnonymizationType.medium)

    @staticmethod
    def string(value):
        return MessageKwarg(value=value, format_type="string", anonymization_type=AnonymizationType.default)


class EventInfo(OpenModuleModel):
    type: str  # a category for icons and grouping, must contain at least one "_", hierarchy via prefix
    timestamp: datetime
    gate: Optional[str]
    license_plate: Optional[str]  # anonymized with type lpr
    license_plate_country: Optional[str]
    session_id: Optional[str]
    related_session_id: Optional[str]
    vehicle_id: Optional[str]
    price: Optional[int]  # cents, maybe as str including currency, so we don't need to get the currency of the garage

    _tz_timestamp = timezone_validator("timestamp")

    @validator("type")
    def type_contains_underscore(cls, v):
        assert "_" in v, "type must container at least one underscore"
        return v

    @staticmethod
    def create(type: str, timestamp: Optional[datetime] = None, gate: Optional[str] = None,
               license_plate: Optional[str] = None, license_plate_country: Optional[str] = None,
               session_id: Optional[str] = None, related_session_id: Optional[str] = None,
               vehicle_id: Optional[str] = None, price: Optional[int] = None):
        return EventInfo(type=type, timestamp=timestamp, gate=gate, license_plate=license_plate,
                         license_plate_country=license_plate_country, session_id=session_id,
                         related_session_id=related_session_id, vehicle_id=vehicle_id, price=price)


class Event(OpenModuleModel):
    message: str  # e.g. 'Session with license plate {lpr} at entry "Einfahrt" started.'
    message_kwargs: Dict[str, MessageKwarg]  # e.g. {"lpr": }
    infos: EventInfo


class EventlogMessage(ZMQMessage):
    type = "create_event"
    event: Event

    def send(self):
        """publish the message with the core publisher on the eventlog topic"""
        core().publish(self, "eventlog")

    @staticmethod
    def create(infos: EventInfo, message: str, **message_kwargs: MessageKwarg):
        """create a new eventlog message with the given parameters"""
        return EventlogMessage(event=Event(infos=infos, message=message, message_kwargs=message_kwargs))


def send_event(infos: EventInfo, message: str, **message_kwargs: MessageKwarg):
    EventlogMessage.create(infos=infos, message=message, **message_kwargs).send()
