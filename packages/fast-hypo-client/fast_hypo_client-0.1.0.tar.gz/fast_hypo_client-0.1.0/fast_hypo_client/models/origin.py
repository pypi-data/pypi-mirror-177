from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.horizontal_uncertainty import HorizontalUncertainty


T = TypeVar("T", bound="Origin")


@attr.s(auto_attribs=True)
class Origin:
    """
    Attributes:
        latitude (float):
        longitude (float):
        depth_m (float):
        uncertainty (Union[Unset, HorizontalUncertainty]):
    """

    latitude: float
    longitude: float
    depth_m: float
    uncertainty: Union[Unset, "HorizontalUncertainty"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        latitude = self.latitude
        longitude = self.longitude
        depth_m = self.depth_m
        uncertainty: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.uncertainty, Unset):
            uncertainty = self.uncertainty.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "latitude": latitude,
                "longitude": longitude,
                "depth_m": depth_m,
            }
        )
        if uncertainty is not UNSET:
            field_dict["uncertainty"] = uncertainty

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.horizontal_uncertainty import HorizontalUncertainty

        d = src_dict.copy()
        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        depth_m = d.pop("depth_m")

        _uncertainty = d.pop("uncertainty", UNSET)
        uncertainty: Union[Unset, HorizontalUncertainty]
        if isinstance(_uncertainty, Unset):
            uncertainty = UNSET
        else:
            uncertainty = HorizontalUncertainty.from_dict(_uncertainty)

        origin = cls(
            latitude=latitude,
            longitude=longitude,
            depth_m=depth_m,
            uncertainty=uncertainty,
        )

        origin.additional_properties = d
        return origin

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
