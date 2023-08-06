from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.phase_reading import PhaseReading
    from ..models.station_lat_lng import StationLatLng
    from ..models.velocity_model_1d import VelocityModel1D


T = TypeVar("T", bound="LocationRequestNLLoc")


@attr.s(auto_attribs=True)
class LocationRequestNLLoc:
    """
    Attributes:
        velocity_model (VelocityModel1D):
        stations (List['StationLatLng']):
        events (List[List['PhaseReading']]):
    """

    velocity_model: "VelocityModel1D"
    stations: List["StationLatLng"]
    events: List[List["PhaseReading"]]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        velocity_model = self.velocity_model.to_dict()

        stations = []
        for stations_item_data in self.stations:
            stations_item = stations_item_data.to_dict()

            stations.append(stations_item)

        events = []
        for events_item_data in self.events:
            events_item = []
            for events_item_item_data in events_item_data:
                events_item_item = events_item_item_data.to_dict()

                events_item.append(events_item_item)

            events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "velocity_model": velocity_model,
                "stations": stations,
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.phase_reading import PhaseReading
        from ..models.station_lat_lng import StationLatLng
        from ..models.velocity_model_1d import VelocityModel1D

        d = src_dict.copy()
        velocity_model = VelocityModel1D.from_dict(d.pop("velocity_model"))

        stations = []
        _stations = d.pop("stations")
        for stations_item_data in _stations:
            stations_item = StationLatLng.from_dict(stations_item_data)

            stations.append(stations_item)

        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = []
            _events_item = events_item_data
            for events_item_item_data in _events_item:
                events_item_item = PhaseReading.from_dict(events_item_item_data)

                events_item.append(events_item_item)

            events.append(events_item)

        location_request_nl_loc = cls(
            velocity_model=velocity_model,
            stations=stations,
            events=events,
        )

        location_request_nl_loc.additional_properties = d
        return location_request_nl_loc

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
