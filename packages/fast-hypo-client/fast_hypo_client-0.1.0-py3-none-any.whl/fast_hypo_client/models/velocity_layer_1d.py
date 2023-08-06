from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VelocityLayer1D")


@attr.s(auto_attribs=True)
class VelocityLayer1D:
    """
    Attributes:
        depth_km (float):
        vp_top (float):
        vs_top (float):
        rho_top (float):
        vp_grad (Union[Unset, float]):
        vs_grad (Union[Unset, float]):
        rho_grad (Union[Unset, float]):
    """

    depth_km: float
    vp_top: float
    vs_top: float
    rho_top: float
    vp_grad: Union[Unset, float] = 0.0
    vs_grad: Union[Unset, float] = 0.0
    rho_grad: Union[Unset, float] = 0.0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        depth_km = self.depth_km
        vp_top = self.vp_top
        vs_top = self.vs_top
        rho_top = self.rho_top
        vp_grad = self.vp_grad
        vs_grad = self.vs_grad
        rho_grad = self.rho_grad

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "depth_km": depth_km,
                "vp_top": vp_top,
                "vs_top": vs_top,
                "rho_top": rho_top,
            }
        )
        if vp_grad is not UNSET:
            field_dict["vp_grad"] = vp_grad
        if vs_grad is not UNSET:
            field_dict["vs_grad"] = vs_grad
        if rho_grad is not UNSET:
            field_dict["rho_grad"] = rho_grad

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        depth_km = d.pop("depth_km")

        vp_top = d.pop("vp_top")

        vs_top = d.pop("vs_top")

        rho_top = d.pop("rho_top")

        vp_grad = d.pop("vp_grad", UNSET)

        vs_grad = d.pop("vs_grad", UNSET)

        rho_grad = d.pop("rho_grad", UNSET)

        velocity_layer_1d = cls(
            depth_km=depth_km,
            vp_top=vp_top,
            vs_top=vs_top,
            rho_top=rho_top,
            vp_grad=vp_grad,
            vs_grad=vs_grad,
            rho_grad=rho_grad,
        )

        velocity_layer_1d.additional_properties = d
        return velocity_layer_1d

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
