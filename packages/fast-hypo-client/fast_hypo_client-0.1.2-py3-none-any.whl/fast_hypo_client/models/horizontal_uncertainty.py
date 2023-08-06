from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="HorizontalUncertainty")


@attr.s(auto_attribs=True)
class HorizontalUncertainty:
    """
    Attributes:
        max_horizontal_uncertainty_m (float):
        min_horizontal_uncertainty_m (float):
        azimuth_max_horizontal_uncertainty_deg (float):
    """

    max_horizontal_uncertainty_m: float
    min_horizontal_uncertainty_m: float
    azimuth_max_horizontal_uncertainty_deg: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        max_horizontal_uncertainty_m = self.max_horizontal_uncertainty_m
        min_horizontal_uncertainty_m = self.min_horizontal_uncertainty_m
        azimuth_max_horizontal_uncertainty_deg = self.azimuth_max_horizontal_uncertainty_deg

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_horizontal_uncertainty_m": max_horizontal_uncertainty_m,
                "min_horizontal_uncertainty_m": min_horizontal_uncertainty_m,
                "azimuth_max_horizontal_uncertainty_deg": azimuth_max_horizontal_uncertainty_deg,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        max_horizontal_uncertainty_m = d.pop("max_horizontal_uncertainty_m")

        min_horizontal_uncertainty_m = d.pop("min_horizontal_uncertainty_m")

        azimuth_max_horizontal_uncertainty_deg = d.pop("azimuth_max_horizontal_uncertainty_deg")

        horizontal_uncertainty = cls(
            max_horizontal_uncertainty_m=max_horizontal_uncertainty_m,
            min_horizontal_uncertainty_m=min_horizontal_uncertainty_m,
            azimuth_max_horizontal_uncertainty_deg=azimuth_max_horizontal_uncertainty_deg,
        )

        horizontal_uncertainty.additional_properties = d
        return horizontal_uncertainty

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
