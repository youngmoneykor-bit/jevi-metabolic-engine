from __future__ import annotations
from dataclasses import dataclass
from .schemas import DailyInputs

@dataclass
class MetabolicModelConfig:
    baseline_sensitivity: float = 1.0
    sleep_penalty_per_hour: float = 0.08
    stress_penalty_per_level: float = 0.05
    precarbs_boost_per_g: float = 0.03
    preprotein_boost_per_g: float = 0.02

    strength_glucose_per_kg: float = 0.0025
    cardio_glucose_per_min: float = 0.4

    epoc_glucose_bonus_min: float = 6.0
    epoc_glucose_bonus_max: float = 10.0


class MetabolicEngine:
    def __init__(self, config: MetabolicModelConfig | None = None):
        self.config = config or MetabolicModelConfig()

    def need_precarb(self, inputs: DailyInputs) -> bool:
        if inputs.last_meal_gap_hours >= 5:
            return True
        if inputs.fbs < 95 and inputs.delta_7pm > 12:
            return True
        return False

    def calc_precarb_grams(self, inputs: DailyInputs) -> float:
        grams = 8.0 + (inputs.carb_load_planned / 40.0) * 4.0
        return min(grams, 15.0)

    def calc_irs(self, inputs: DailyInputs, precarbs: float, preprotein: float) -> float:
        c = self.config
        sleep_penalty = max(0.0, (7.0 - inputs.sleep_hours) * c.sleep_penalty_per_hour)
        stress_penalty = inputs.stress_index * c.stress_penalty_per_level
        pre_carb_boost = precarbs * c.precarbs_boost_per_g
        pre_protein_boost = preprotein * c.preprotein_boost_per_g
        irs = (
            c.baseline_sensitivity
            - sleep_penalty
            - stress_penalty
            + pre_carb_boost
            + pre_protein_boost
        )
        return max(0.6, min(1.4, irs))

    def calc_pegd(self, inputs: DailyInputs) -> float:
        c = self.config
        base = (
            inputs.strength_volume_kg * c.strength_glucose_per_kg
            + inputs.cardio_minutes * c.cardio_glucose_per_min
        )
        epoc = 0.0
        if inputs.is_epoc_day:
            epoc = (c.epoc_glucose_bonus_min + c.epoc_glucose_bonus_max) / 2.0
        return base + epoc

    def calc_drug_effect(self, inputs: DailyInputs, immediate: bool) -> float:
        effect = 0.0
        if inputs.taking_dpp4:
            effect += 12.0 if immediate else 6.0
        if inputs.taking_metformin:
            effect += 8.0
        return effect

    def predict_evening_dynamics(
        self,
        inputs: DailyInputs,
        precarbs: float,
        preprotein: float,
        immediate_drug: bool,
    ):
        irs = self.calc_irs(inputs, precarbs, preprotein)
        peg = self.calc_pegd(inputs)
        drug_effect = self.calc_drug_effect(inputs, immediate_drug)

        if inputs.gi_level == "high":
            gi_factor = 1.3
        elif inputs.gi_level == "medium":
            gi_factor = 1.0
        else:
            gi_factor = 0.7

        gi_factor *= 1.1

        cka_peak = inputs.carb_load_planned * gi_factor * irs * 0.9

        ppg_peak = inputs.fbs + cka_peak - peg - drug_effect

        bedtime = ppg_peak - 0.6 * inputs.carb_load_planned

        evening_rise = 0.0
        if inputs.delta_7pm > 0:
            suppression_factor = 0.5 if (peg > 10 or drug_effect > 0) else 0.2
            evening_rise = inputs.delta_7pm * (1.0 - suppression_factor)
        bedtime += evening_rise

        hepatic_output = 0.0
        if inputs.sleep_hours < 6.0:
            hepatic_output += 15.0
        if inputs.stress_index >= 2:
            hepatic_output += 10.0
        if peg > 10:
            hepatic_output -= 8.0

        fbs_next = bedtime * 0.55 + hepatic_output - (drug_effect * 0.5)

        return ppg_peak, bedtime, fbs_next
