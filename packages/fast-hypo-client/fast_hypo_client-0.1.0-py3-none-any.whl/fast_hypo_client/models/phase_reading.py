import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.first_motion import FirstMotion
from ..models.onset import Onset
from ..models.phase_descriptor_p import PhaseDescriptorP
from ..models.phase_descriptor_s import PhaseDescriptorS
from ..types import UNSET, Unset

T = TypeVar("T", bound="PhaseReading")


@attr.s(auto_attribs=True)
class PhaseReading:
    """
    Attributes:
        station_name (str):
        p_arrival (datetime.datetime):
        p_onset (Union[Unset, Onset]): An enumeration. Default: Onset.VALUE_2.
        p_phase_descriptor (Union[Unset, PhaseDescriptorP]): An enumeration. Default: PhaseDescriptorP.VALUE_4.
        p_first_motion (Union[Unset, FirstMotion]): An enumeration.
        s_arrival (Union[Unset, datetime.datetime]):
        p_weight (Union[Unset, int]):
        s_onset (Union[Unset, Onset]): An enumeration. Default: Onset.VALUE_2.
        s_phase_descriptor (Union[Unset, PhaseDescriptorS]): An enumeration. Default: PhaseDescriptorS.VALUE_3.
        s_remark (Union[Unset, str]):  Default: '   '.
        s_first_motion (Union[Unset, FirstMotion]): An enumeration.
        s_weight (Union[Unset, int]):
        amplitude (Union[Unset, float]):
        period (Union[Unset, float]):
        time_correction (Union[Unset, float]):
        f_p_time (Union[Unset, float]):
    """

    station_name: str
    p_arrival: datetime.datetime
    p_onset: Union[Unset, Onset] = Onset.VALUE_2
    p_phase_descriptor: Union[Unset, PhaseDescriptorP] = PhaseDescriptorP.VALUE_4
    p_first_motion: Union[Unset, FirstMotion] = UNSET
    s_arrival: Union[Unset, datetime.datetime] = UNSET
    p_weight: Union[Unset, int] = UNSET
    s_onset: Union[Unset, Onset] = Onset.VALUE_2
    s_phase_descriptor: Union[Unset, PhaseDescriptorS] = PhaseDescriptorS.VALUE_3
    s_remark: Union[Unset, str] = "   "
    s_first_motion: Union[Unset, FirstMotion] = UNSET
    s_weight: Union[Unset, int] = UNSET
    amplitude: Union[Unset, float] = UNSET
    period: Union[Unset, float] = UNSET
    time_correction: Union[Unset, float] = UNSET
    f_p_time: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        station_name = self.station_name
        p_arrival = self.p_arrival.isoformat()

        p_onset: Union[Unset, str] = UNSET
        if not isinstance(self.p_onset, Unset):
            p_onset = self.p_onset.value

        p_phase_descriptor: Union[Unset, str] = UNSET
        if not isinstance(self.p_phase_descriptor, Unset):
            p_phase_descriptor = self.p_phase_descriptor.value

        p_first_motion: Union[Unset, str] = UNSET
        if not isinstance(self.p_first_motion, Unset):
            p_first_motion = self.p_first_motion.value

        s_arrival: Union[Unset, str] = UNSET
        if not isinstance(self.s_arrival, Unset):
            s_arrival = self.s_arrival.isoformat()

        p_weight = self.p_weight
        s_onset: Union[Unset, str] = UNSET
        if not isinstance(self.s_onset, Unset):
            s_onset = self.s_onset.value

        s_phase_descriptor: Union[Unset, str] = UNSET
        if not isinstance(self.s_phase_descriptor, Unset):
            s_phase_descriptor = self.s_phase_descriptor.value

        s_remark = self.s_remark
        s_first_motion: Union[Unset, str] = UNSET
        if not isinstance(self.s_first_motion, Unset):
            s_first_motion = self.s_first_motion.value

        s_weight = self.s_weight
        amplitude = self.amplitude
        period = self.period
        time_correction = self.time_correction
        f_p_time = self.f_p_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "station_name": station_name,
                "p_arrival": p_arrival,
            }
        )
        if p_onset is not UNSET:
            field_dict["p_onset"] = p_onset
        if p_phase_descriptor is not UNSET:
            field_dict["p_phase_descriptor"] = p_phase_descriptor
        if p_first_motion is not UNSET:
            field_dict["p_first_motion"] = p_first_motion
        if s_arrival is not UNSET:
            field_dict["s_arrival"] = s_arrival
        if p_weight is not UNSET:
            field_dict["p_weight"] = p_weight
        if s_onset is not UNSET:
            field_dict["s_onset"] = s_onset
        if s_phase_descriptor is not UNSET:
            field_dict["s_phase_descriptor"] = s_phase_descriptor
        if s_remark is not UNSET:
            field_dict["s_remark"] = s_remark
        if s_first_motion is not UNSET:
            field_dict["s_first_motion"] = s_first_motion
        if s_weight is not UNSET:
            field_dict["s_weight"] = s_weight
        if amplitude is not UNSET:
            field_dict["amplitude"] = amplitude
        if period is not UNSET:
            field_dict["period"] = period
        if time_correction is not UNSET:
            field_dict["time_correction"] = time_correction
        if f_p_time is not UNSET:
            field_dict["f_p_time"] = f_p_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        station_name = d.pop("station_name")

        p_arrival = isoparse(d.pop("p_arrival"))

        _p_onset = d.pop("p_onset", UNSET)
        p_onset: Union[Unset, Onset]
        if isinstance(_p_onset, Unset):
            p_onset = UNSET
        else:
            p_onset = Onset(_p_onset)

        _p_phase_descriptor = d.pop("p_phase_descriptor", UNSET)
        p_phase_descriptor: Union[Unset, PhaseDescriptorP]
        if isinstance(_p_phase_descriptor, Unset):
            p_phase_descriptor = UNSET
        else:
            p_phase_descriptor = PhaseDescriptorP(_p_phase_descriptor)

        _p_first_motion = d.pop("p_first_motion", UNSET)
        p_first_motion: Union[Unset, FirstMotion]
        if isinstance(_p_first_motion, Unset):
            p_first_motion = UNSET
        else:
            p_first_motion = FirstMotion(_p_first_motion)

        _s_arrival = d.pop("s_arrival", UNSET)
        s_arrival: Union[Unset, datetime.datetime]
        if isinstance(_s_arrival, Unset):
            s_arrival = UNSET
        else:
            s_arrival = isoparse(_s_arrival)

        p_weight = d.pop("p_weight", UNSET)

        _s_onset = d.pop("s_onset", UNSET)
        s_onset: Union[Unset, Onset]
        if isinstance(_s_onset, Unset):
            s_onset = UNSET
        else:
            s_onset = Onset(_s_onset)

        _s_phase_descriptor = d.pop("s_phase_descriptor", UNSET)
        s_phase_descriptor: Union[Unset, PhaseDescriptorS]
        if isinstance(_s_phase_descriptor, Unset):
            s_phase_descriptor = UNSET
        else:
            s_phase_descriptor = PhaseDescriptorS(_s_phase_descriptor)

        s_remark = d.pop("s_remark", UNSET)

        _s_first_motion = d.pop("s_first_motion", UNSET)
        s_first_motion: Union[Unset, FirstMotion]
        if isinstance(_s_first_motion, Unset):
            s_first_motion = UNSET
        else:
            s_first_motion = FirstMotion(_s_first_motion)

        s_weight = d.pop("s_weight", UNSET)

        amplitude = d.pop("amplitude", UNSET)

        period = d.pop("period", UNSET)

        time_correction = d.pop("time_correction", UNSET)

        f_p_time = d.pop("f_p_time", UNSET)

        phase_reading = cls(
            station_name=station_name,
            p_arrival=p_arrival,
            p_onset=p_onset,
            p_phase_descriptor=p_phase_descriptor,
            p_first_motion=p_first_motion,
            s_arrival=s_arrival,
            p_weight=p_weight,
            s_onset=s_onset,
            s_phase_descriptor=s_phase_descriptor,
            s_remark=s_remark,
            s_first_motion=s_first_motion,
            s_weight=s_weight,
            amplitude=amplitude,
            period=period,
            time_correction=time_correction,
            f_p_time=f_p_time,
        )

        phase_reading.additional_properties = d
        return phase_reading

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
