from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="StationLatLng")


@attr.s(auto_attribs=True)
class StationLatLng:
    """
    Attributes:
        code (str):
        latitude (float):
        longitude (float):
        elevation_km (float):
        depth_km (float):
    """

    code: str
    latitude: float
    longitude: float
    elevation_km: float
    depth_km: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        latitude = self.latitude
        longitude = self.longitude
        elevation_km = self.elevation_km
        depth_km = self.depth_km

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "latitude": latitude,
                "longitude": longitude,
                "elevation_km": elevation_km,
                "depth_km": depth_km,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        elevation_km = d.pop("elevation_km")

        depth_km = d.pop("depth_km")

        station_lat_lng = cls(
            code=code,
            latitude=latitude,
            longitude=longitude,
            elevation_km=elevation_km,
            depth_km=depth_km,
        )

        station_lat_lng.additional_properties = d
        return station_lat_lng

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
