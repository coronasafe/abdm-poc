import json
import os
from datetime import datetime
from typing import List
from uuid import uuid4

from fhir.resources.bundle import Bundle
from fhir.resources.composition import Composition

HOSTED_URL = os.environ.get("url", "default_url_here")


def gen_timestamp():
    return str(datetime.now().astimezone().isoformat(timespec="milliseconds"))


def gen_bundle(entries: List[any]):
    uuid = str(uuid4())
    identifier = {"system": HOSTED_URL, "value": uuid}
    timestamp = gen_timestamp()
    meta = {"versionId": "1", "lastUpdated": timestamp}
    bundle = Bundle(
        entry=entries,
        type="document",
        id=uuid,
        identifier=identifier,
        timestamp=timestamp,
        meta=meta,
    ).json(return_bytes=True)
    return bundle


def gen_composition(id: int, title: str):
    timestamp = gen_timestamp()
    comp = Composition(
        title="Prescription record",
        id=id,
        date=timestamp,
        subject={},
        status="final",
        type={},
        author=[],
        attester=[],
        section=[],
    )
    return comp
