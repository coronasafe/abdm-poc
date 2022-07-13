from typing import TypedDict


class CareContext(TypedDict):
    reference_number: str
    display: str
    details: str


class Patient(TypedDict):
    mobile: str
    name: str
    gender: str
    id: str
    abha: str
    linked: bool
    care_contexts: list[CareContext]


class Facility(TypedDict):
    name: str
    id: str
    patients: list[Patient]


facilities: list[Facility] = [
    {
        "id": "f1",
        "name": "facility #1",
        "patients": [
            {
                "id": "p1",
                "name": "patient 1",
                "mobile": "999999999",
                "abha": None,
                "gender": "M",
                "linked": False,
                "care_contexts": [],
            },
        ],
    }
]

consents = {}
