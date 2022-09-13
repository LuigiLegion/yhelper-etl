# Imports
from typing import TypedDict, Dict, List, Optional


# Initializations
class Datum(TypedDict):
    camis: Optional[str]
    dba: Optional[str]
    boro: Optional[str]
    building: Optional[str]
    street: Optional[str]
    zipcode: Optional[str]
    phone: Optional[str]
    cuisine_description: Optional[str]
    inspection_date: Optional[str]
    action: Optional[str]
    violation_code: Optional[str]
    violation_description: Optional[str]
    critical_flag: Optional[str]
    score: Optional[str]
    record_date: Optional[str]
    inspection_type: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    community_board: Optional[str]
    council_district: Optional[str]
    census_tract: Optional[str]
    bin: Optional[str]
    bbl: Optional[str]
    nta: Optional[str]


class Violation(TypedDict):
    description: Optional[str]
    critical: bool


class Inspection(TypedDict):
    date: Optional[str]
    score: Optional[int]
    grade: Optional[str]
    violations: List[Violation]


class Restaurant(TypedDict):
    name: Optional[str]
    phone: Optional[str]
    building: Optional[str]
    street: Optional[str]
    borough: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    inspections: List[Inspection]
    statistics: Dict[str, float]
