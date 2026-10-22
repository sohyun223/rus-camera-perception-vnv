# 연구계획 변경안 — 2026.10.22

> 연구계획 검토안: 교수님·멘토의 최종 승인 및 공식 신청서 변경 여부는 별도 확인 예정.

## 연구명

- 국문: **환경 및 영상 열화 조건에서 Camera 기반 자율주행 인지 소프트웨어의 강건성 한계 분석 및 자동 검증 연구**
- 영문: **Automated Robustness Validation and Failure Boundary Analysis of Camera-based Autonomous Driving Perception under Image Degradation**
- 수행 기간: **2026-10-22 ~ 2026-12-31**

## 연구 배경 및 연구 목적

기존에는 2D/3D LiDAR 기반 센서 열화 및 융합을 연구하였다. 9월에 ROS2 환경, VLP-16 PointCloud 처리, 10/30/50/70% Point Dropout을 실험했다. 이 성과를 **기 수행 선행연구**로 남기고, 이후 Camera 기반 인지 소프트웨어의 *검증 방법론*으로 주제를 전환한다.

단순한 영상 열화별 정확도 변화 비교뿐 아니라, 정해진 성능 요구조건이 무너지기 시작하는 Failure Boundary를 식별하며 이러한 실험을 자동·반복할 수 있는 평가 체계를 구축한다.

## 연구 질문

1. 영상 열화 유형 및 강도가 객체 인식 Precision/Recall/mAP·False Negative에 어떤 영향을 주는가?
2. 사전에 정의한 요구 성능 미달로 전환하는 Failure Boundary는 어디인가?
3. 반복 가능한 실험과 기준 결과 대비 Regression Test를 자동화할 수 있는가?
4. 확장: 단일 열화와 저조도+Blur, Fog+Blur 같은 복합 열화는 어떻게 다른가?

## 실험 구성

- **데이터:** Ground Truth Bounding Box가 있는 공개 자율주행 Camera 데이터셋 한 종류를 선정하고 평가 subset의 ID를 고정
- **검출기:** 사전학습된 YOLO 계열 1종부터 시작. 모델·가중치·Confidence·IoU 기준을 실험마다 기록
- **열화:** Brightness(저조도), Blur, Gaussian Noise, Fog 각각 약·중·강
- **메트릭:** Precision, Recall, mAP, FN, 클래스별 결과, 추론 시간
- **경계 탐색:** 파일럿 단계에서 요구 성능 기준을 정하고 **주 실험 시작 전 고정**한 뒤 열화 강도별 PASS/FAIL 전환 구간을 탐색
- **복합조건:** Low-light+Blur, Fog+Blur 결과를 Robustness Map으로 정리
- **자동화:** YAML test config → 열화 생성 → 추론 → GT-based metric → CSV·그래프 → PASS/FAIL → Regression 비교
- **CI/CT:** 소규모 고정 샘플과 결정적 테스트만 GitHub Actions에 연결. 대규모 실험은 로컬 PC에서 실행

### 주의 및 한계

- 라벨이 없으면 객체 인식 정확도/mAP를 계산할 수 없으므로 반드시 Ground Truth가 있는 데이터 사용.
- 영상 열화 강도와 성능이 항상 단조적이지 않을 수 있으므로 단일 경계값을 억지로 가정하지 않고 전환 **구간**을 보고.
- 임의의 PASS/FAIL 기준은 실제 차량 안전 요구사항을 의미하지 않음.
- 결과가 없는 기능이나 데이터·모델은 완료라고 표기하지 않음.

## 졸업프로젝트와의 차별화

CARLA/Autoware/V2V 전체 자율주행 시스템 안전성과 주행 효율을 검증하는 졸업프로젝트와 달리 RUS에서는 Camera **인지 SW 단독 검증**, Fault Injection, Failure Boundary, Regression Test/CI-CT에 집중한다.

## 기대 산출물

1. 정상 Baseline 및 단일 열화 정량 결과
2. Failure Boundary 및 복합 열화 Robustness Map
3. 재현 가능한 실험 설정(YAML/Seed/모델 버전)
4. Test Runner 및 Regression 검출
5. CI 기반 소규모 테스트(시간 허용 시)
6. 결과 분석 및 다음 학기 UGV 확장 계획

## 다음 학기 후속 연구

2027년 1학기에 연구실 UGV Camera 데이터를 직접 수집·라벨링하고, 저조도/역광/진동의 실제 환경에서 같은 검증 방법을 적용한다. Synthetic-to-Real 성능 미달 경계 차이를 정량 비교하고, 실제 연산 장치에서의 지연 및 프레임 처리율을 필요시 추가한다. 실환경 UGV 시험과 HIL은 구분한다.
