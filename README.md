# jevi-metabolic-engine

개인 맞춤형 저녁 혈당 최적화 모델.

- 목적:
  - 저녁 식후 혈당 피크 예측
  - 취침 전 혈당 예측
  - 다음날 공복혈당 예측
  - 그에 맞는 **식전 탄수/단백질/섬유 + 운동 + 약물 타이밍 추천**

---

## Quick Start

```bash
git clone https://github.com/<your-id>/jevi-metabolic-engine.git
cd jevi-metabolic-engine
pip install -r requirements.txt
python -m jevi_metabolic_engine.cli examples/example_day_simple.json
