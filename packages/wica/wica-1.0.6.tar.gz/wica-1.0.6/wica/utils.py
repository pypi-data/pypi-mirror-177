from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Literal, Optional


@dataclass
class WicaStreamProperties:
    """Properties of a Wica stream.

    All intervals in milliseconds
    """

    qiet_mode: bool
    heartbeat_flux_nterval: int
    metadata_flux_interval: int
    monitored_value_flux_interval: int
    polled_value_flux_interval: int
    data_aquisition_mode: Literal['poll', 'monitor', 'poll-monitor', 'poll-and-monitor']
    polling_interval: int
    fields_of_interest: List[str]
    numeric_precision: int
    filter_type: Literal['ALL_VALUE', 'AVERAGER', 'CHANGE_DETECTOR', 'LAST_N', 'ONE_IN_M', 'RATE_LIMITER']
    filter_num_samples: int
    filter_num_samples_avg: int
    filter_cycle_length: int
    filter_sampling_interval: int
    filter_deadband: float


@dataclass
class WicaChannel:

    @dataclass
    class WicaChannelProperties:
        data_aquisition_mode: Optional[Literal['poll', 'monitor', 'poll-monitor', 'poll-and-monitor']] = None
        polling_interval: Optional[int] = None
        fields_of_interest: List[str] = None
        filter_type: Optional[Literal['ALL_VALUE', 'AVERAGER', 'CHANGE_DETECTOR', 'LAST_N', 'ONE_IN_M', 'RATE_LIMITER']] = None
        n: Optional[int] = None
        m: Optional[int] = None
        x: Optional[int] = None
        filter_sampling_interval: Optional[int] = None
        filter_deadband: Optional[float] = None

    name: str
    properties: WicaChannelProperties = None


@dataclass
class WicaMessage(object):
    stream_id: int = None
    event: Optional[Literal['heartbeat', 'metadata', 'value']] = None
    value_type: Optional[Literal['polled', 'monitored']] = None
    data: dict | str = field(default_factory=dict)
    time: Optional[datetime] = None
