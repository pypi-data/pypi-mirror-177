# API Client for Earthquake Location

## Usage

```py
from datetime import datetime
import requests

from fast_hypo_client.models import VelocityLayer1D, VelocityModel1D, PhaseReading, StationLatLng, PhaseDescriptorP, FirstMotion, LocationRequestNLLoc
from fast_hypo_client.client import Client
from fast_hypo_client.api.non_lin_loc import locate_nlloc_locate_nlloc_post

velocity_model = VelocityModel1D(
    layers=[
        VelocityLayer1D(
            depth_km=0.0,
            vp_top=4.0,
            vs_top=2.38,
            rho_top=2.7,
            vp_grad=0.0,
            vs_grad=0.0,
            rho_grad=0.0,
        ),
        VelocityLayer1D(
            depth_km=2.0,
            vp_top=6.0,
            vs_top=3.57,
            rho_top=2.7,
            vp_grad=0.0,
            vs_grad=0.0,
            rho_grad=0.0,
        ),
        VelocityLayer1D(
            depth_km=10.0,
            vp_top=6.3,
            vs_top=3.75,
            rho_top=2.7,
            vp_grad=0.0,
            vs_grad=0.0,
            rho_grad=0.0,
        ),
    ]
)

stations = [
    StationLatLng(
        code="SBF",
        latitude=43.8635,
        longitude=7.43483,
        elevation_km=0.847,
        depth_km=0.0,
    ),
    StationLatLng(
        code="CEPP",
        latitude=43.9163,
        longitude=7.7465,
        elevation_km=1.08,
        depth_km=0.0,
    ),
    StationLatLng(
        code="MVIF",
        latitude=43.8965,
        longitude=7.1525,
        elevation_km=1.48,
        depth_km=0.0,
    ),
    StationLatLng(
        code="IMI",
        latitude=43.9105,
        longitude=7.89317,
        elevation_km=0.84,
        depth_km=0.0,
    ),
]

events = [
    [
        PhaseReading(
            station_name="SBF",
            p_phase_descriptor=PhaseDescriptorP.P,
            p_arrival=datetime.fromisoformat("1995-04-21T08:03:00.260"),
        ),
        PhaseReading(
            station_name="CEPP",
            p_phase_descriptor=PhaseDescriptorP.P,
            p_first_motion=FirstMotion.UP,
            p_arrival=datetime.fromisoformat("1995-04-21T08:03:01.140"),
        ),
        PhaseReading(
            station_name="MVIF",
            p_phase_descriptor=PhaseDescriptorP.P,
            p_weight=0,
            p_arrival=datetime.fromisoformat("1995-04-21T08:03:03.580"),
            s_arrival=datetime.fromisoformat("1995-04-21T08:03:08.680"),
        ),
        PhaseReading(
            station_name="IMI",
            p_phase_descriptor=PhaseDescriptorP.P,
            p_weight=0,
            p_arrival=datetime.fromisoformat("1995-04-21T08:03:02.770"),
        ),
    ]
]

request = LocationRequestNLLoc(
    events=events,
    stations=stations,
    velocity_model=velocity_model,
)

client = Client(base_url="https://fast-hypo.fly.dev")

locate_nlloc_locate_nlloc_post.sync_detailed(client=client, json_body=request)
```