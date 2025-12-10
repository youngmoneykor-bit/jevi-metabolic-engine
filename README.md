# Jevi Metabolic Engine

개인 맞춤형 저녁 혈당 최적화 모델.  
(Jevi Wong 개인 대사 패턴 기반 v3.0 모델 구현)

---

## 🚀 기능

- 저녁 식전 탄수(pre-carb) 필요 여부 자동 판단
- 적정 pre-carb g 계산 (8–15g)
- 식전 단백질/식이섬유 권장량 계산
- 운동량(근력/유산소)에 따른 포도당 소비량 예측
- 약물 복용 타이밍 추천 (식후 즉시 vs 1시간 후)
- 저녁 식후 혈당 피크 예측
- 취침 전 혈당 예측
- 다음날 공복 혈당 예측
- 전체를 종합하여 **오늘의 저녁 최적 프로토콜 생성**

---

## 📁 프로젝트 구조

```
jevi-metabolic-engine/
├─ README.md
├─ requirements.txt
├─ src/
│  └─ jevi_metabolic_engine/
│     ├─ __init__.py
│     ├─ schemas.py
│     ├─ model.py
│     ├─ planner.py
│     └─ cli.py
├─ examples/
│  ├─ example_day_simple.json
│  └─ example_day_heavy_carb.json
└─ notebooks/
   └─ exploration.ipynb (선택)
```

---

## 🔧 설치

```
pip install -r requirements.txt
```

---

## ▶ 실행

```
python -m jevi_metabolic_engine.cli examples/example_day_simple.json
```

출력 예:

```
=== Jevi Evening Plan ===
- Pre-carb : 12 g (긴 공복/저녁 자연상승 때문에 사전 탄수 권장)
- Pre-protein : 10 g
- Pre-fiber : 4 g
- Drug timing : immediate_after_meal
- Exercise : 식후 20~30분 걷기 추천

- Predicted PPG peak : 128 mg/dL
- Predicted bedtime : 102 mg/dL
- Predicted FBS next : 95 mg/dL
```

---

## 👤 Author  
Jevi Wong + ChatGPT Metabolic Model Lab

