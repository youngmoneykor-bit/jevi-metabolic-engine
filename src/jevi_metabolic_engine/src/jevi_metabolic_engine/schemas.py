from dataclasses import dataclass
from typing import Literal

GILevel = Literal["low", "medium", "high"]
ExerciseType = Literal["none", "strength", "cardio", "mixed"]

@dataclass
class DailyInputs:
    fbs: float
    delta_7pm: float
    last_meal_gap_hours: float

    carb_load_planned: float
    gi_level: GILevel
    fiber_grams: float
    protein_grams: float

    exercise_type: ExerciseType
    strength_volume_kg: float
    cardio_minutes: float

    taking_dpp4: bool
    taking_metformin: bool

    sleep_hours: float
    stress_index: int
    is_epoc_day: bool = False


@dataclass
class EveningPlan:
    pre_carb_grams: float
    pre_carb_note: str

    pre_protein_grams: float
    pre_fiber_grams: float

    drug_timing: str
    exercise_recommendation: str

    predicted_peak: float
    predicted_bedtime: float
    predicted_fbs_next: float

    comments: str
