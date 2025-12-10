from .schemas import DailyInputs, EveningPlan
from .model import MetabolicEngine

class EveningPlanner:
    def __init__(self):
        self.engine = MetabolicEngine()

    def create_plan(self, inputs: DailyInputs) -> EveningPlan:
        need_pre = self.engine.need_precarb(inputs)
        if need_pre:
            pre_carb = self.engine.calc_precarb_grams(inputs)
            pre_carb_note = "긴 공복/저녁 자연상승 때문에 사전 탄수 권장"
        else:
            pre_carb = 0.0
            pre_carb_note = "오늘은 사전 탄수 없이도 가능"

        if need_pre:
            pre_protein = 10.0
            pre_fiber = 4.0
        else:
            pre_protein = 14.0
            pre_fiber = 5.0

        immediate_drug = False
        if inputs.delta_7pm > 10 or inputs.carb_load_planned > 30:
            immediate_drug = True
            drug_timing = "immediate_after_meal"
        else:
            drug_timing = "one_hour_after_meal"

        ppg_peak, bedtime, fbs_next = self.engine.predict_evening_dynamics(
            inputs,
            precarbs=pre_carb,
            preprotein=pre_protein,
            immediate_drug=immediate_drug,
        )

        if inputs.exercise_type == "none":
            if inputs.carb_load_planned > 25:
                ex_comment = "식후 20~30분 걷기 추천"
            else:
                ex_comment = "가벼운 산책 10~15분이면 충분"
        else:
            ex_comment = "운동 계획량 충분 (걷기 10분 추가시 더 안정적)"

        comments = []
        if ppg_peak <= 135:
            comments.append("오늘 식후 혈당 패턴 안정적 예상.")
        else:
            comments.append("탄수/운동량 조정시 더 낮출 수 있음.")
        if fbs_next <= 105:
            comments.append("내일 공복혈당 양호할 가능성 높음.")
        else:
            comments.append("수면/스트레스 영향으로 공복혈당 상승 가능.")

        return EveningPlan(
            pre_carb_grams=round(pre_carb, 1),
            pre_carb_note=pre_carb_note,
            pre_protein_grams=pre_protein,
            pre_fiber_grams=pre_fiber,
            drug_timing=drug_timing,
            exercise_recommendation=ex_comment,
            predicted_peak=round(ppg_peak, 1),
            predicted_bedtime=round(bedtime, 1),
            predicted_fbs_next=round(fbs_next, 1),
            comments=" ".join(comments),
        )
