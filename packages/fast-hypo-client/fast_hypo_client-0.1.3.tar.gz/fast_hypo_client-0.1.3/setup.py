# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_hypo_client',
 'fast_hypo_client.api',
 'fast_hypo_client.api.non_lin_loc',
 'fast_hypo_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3.0', 'httpx>=0.15.4,<0.24.0', 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'fast-hypo-client',
    'version': '0.1.3',
    'description': 'A client library for accessing Fast-Hypo',
    'long_description': '# API Client for Earthquake Location\n\n## Installation\n```sh\npip install fast-hypo-client\n```\n\n## Usage\n\n```py\nfrom datetime import datetime\nimport requests\n\nfrom fast_hypo_client.models import VelocityLayer1D, VelocityModel1D, PhaseReading, StationLatLng, PhaseDescriptorP, FirstMotion, LocationRequestNLLoc\nfrom fast_hypo_client.client import Client\nfrom fast_hypo_client.api.non_lin_loc import locate_nlloc_locate_nlloc_post\n\nvelocity_model = VelocityModel1D(\n    layers=[\n        VelocityLayer1D(\n            depth_km=0.0,\n            vp_top=4.0,\n            vs_top=2.38,\n            rho_top=2.7,\n            vp_grad=0.0,\n            vs_grad=0.0,\n            rho_grad=0.0,\n        ),\n        VelocityLayer1D(\n            depth_km=2.0,\n            vp_top=6.0,\n            vs_top=3.57,\n            rho_top=2.7,\n            vp_grad=0.0,\n            vs_grad=0.0,\n            rho_grad=0.0,\n        ),\n        VelocityLayer1D(\n            depth_km=10.0,\n            vp_top=6.3,\n            vs_top=3.75,\n            rho_top=2.7,\n            vp_grad=0.0,\n            vs_grad=0.0,\n            rho_grad=0.0,\n        ),\n    ]\n)\n\nstations = [\n    StationLatLng(\n        code="SBF",\n        latitude=43.8635,\n        longitude=7.43483,\n        elevation_km=0.847,\n        depth_km=0.0,\n    ),\n    StationLatLng(\n        code="CEPP",\n        latitude=43.9163,\n        longitude=7.7465,\n        elevation_km=1.08,\n        depth_km=0.0,\n    ),\n    StationLatLng(\n        code="MVIF",\n        latitude=43.8965,\n        longitude=7.1525,\n        elevation_km=1.48,\n        depth_km=0.0,\n    ),\n    StationLatLng(\n        code="IMI",\n        latitude=43.9105,\n        longitude=7.89317,\n        elevation_km=0.84,\n        depth_km=0.0,\n    ),\n]\n\nevents = [\n    [\n        PhaseReading(\n            station_name="SBF",\n            p_phase_descriptor=PhaseDescriptorP.P,\n            p_arrival=datetime.fromisoformat("1995-04-21T08:03:00.260"),\n        ),\n        PhaseReading(\n            station_name="CEPP",\n            p_phase_descriptor=PhaseDescriptorP.P,\n            p_first_motion=FirstMotion.UP,\n            p_arrival=datetime.fromisoformat("1995-04-21T08:03:01.140"),\n        ),\n        PhaseReading(\n            station_name="MVIF",\n            p_phase_descriptor=PhaseDescriptorP.P,\n            p_weight=0,\n            p_arrival=datetime.fromisoformat("1995-04-21T08:03:03.580"),\n            s_arrival=datetime.fromisoformat("1995-04-21T08:03:08.680"),\n        ),\n        PhaseReading(\n            station_name="IMI",\n            p_phase_descriptor=PhaseDescriptorP.P,\n            p_weight=0,\n            p_arrival=datetime.fromisoformat("1995-04-21T08:03:02.770"),\n        ),\n    ]\n]\n\nrequest = LocationRequestNLLoc(\n    events=events,\n    stations=stations,\n    velocity_model=velocity_model,\n)\n\nclient = Client(base_url="https://fast-hypo.fly.dev")\n\nresponse = locate_nlloc_locate_nlloc_post.sync_detailed(client=client, json_body=request)\nprint(response.parsed)\n\n# [Origin(latitude=43.882196, longitude=7.550554, depth_m=11976.562, uncertainty=HorizontalUncertainty(max_horizontal_uncertainty_m=25324.4, min_horizontal_uncertainty_m=15945.2, azimuth_max_horizontal_uncertainty_deg=163.321, additional_properties={}), additional_properties={})]\n```',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
