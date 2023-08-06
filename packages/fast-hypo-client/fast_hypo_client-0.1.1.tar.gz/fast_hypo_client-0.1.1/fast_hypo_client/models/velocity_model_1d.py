from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.velocity_layer_1d import VelocityLayer1D


T = TypeVar("T", bound="VelocityModel1D")


@attr.s(auto_attribs=True)
class VelocityModel1D:
    """
    Attributes:
        layers (List['VelocityLayer1D']):
    """

    layers: List["VelocityLayer1D"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        layers = []
        for layers_item_data in self.layers:
            layers_item = layers_item_data.to_dict()

            layers.append(layers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "layers": layers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.velocity_layer_1d import VelocityLayer1D

        d = src_dict.copy()
        layers = []
        _layers = d.pop("layers")
        for layers_item_data in _layers:
            layers_item = VelocityLayer1D.from_dict(layers_item_data)

            layers.append(layers_item)

        velocity_model_1d = cls(
            layers=layers,
        )

        velocity_model_1d.additional_properties = d
        return velocity_model_1d

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
