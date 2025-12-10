import json
import sys
from .schemas import DailyInputs
from .planner import EveningPlanner

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m jevi_metabolic_engine.cli <input_json_path>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    inputs = DailyInputs(**data)
    planner = EveningPlanner()
    plan = planner.create_plan(inputs)

    print("=== Jevi Evening Plan ===")
    print(f"- Pre-carb : {plan.pre_carb_grams} g ({plan.pre_carb_note})")
    print(f"- Pre-protein : {plan.pre_protein_grams} g")
    print(f"- Pre-fiber : {plan.pre_fiber_grams} g")
    print(f"- Drug timing : {plan.drug_timing}")
    print(f"- Exercise : {plan.exercise_recommendation}\n")
    print(f"- Predicted PPG peak : {plan.predicted_peak} mg/dL")
    print(f"- Predicted bedtime : {plan.predicted_bedtime} mg/dL")
    print(f"- Predicted FBS next : {plan.predicted_fbs_next} mg/dL\n")
    print(f"Comments: {plan.comments}")

if __name__ == "__main__":
    main()
