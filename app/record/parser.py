from typing import Dict, Any

import msgpack
from aiokafka import ConsumerRecord
from typing_extensions import TypedDict


class ParsedRecord(TypedDict):
    value: Dict[str, Any]
    headers: Dict[str, Any]



def parse_consumer_record(record: ConsumerRecord) -> ParsedRecord:
    return {
        'value': msgpack.unpackb(record.value),
        'headers': {},
    }