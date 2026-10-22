# RUS — Camera Perception Robustness & Automated V&V

> **연구주제 변경 계획 (2026-10-22 ~ 2026-12-31)**  
> 공식 변경·승인 절차는 별도 확인 필요. 이 저장소에는 9월 LiDAR 선행 실험 코드도 보존합니다.

## 연구 주제

**환경 및 영상 열화 조건에서 Camera 기반 자율주행 인지 소프트웨어의 강건성 한계 분석 및 자동 검증 연구**

*Automated Robustness Validation and Failure Boundary Analysis of Camera-based Autonomous Driving Perception under Image Degradation*

## 연구 목표

단순히 영상 열화가 커질수록 인식 성능이 감소하는지 비교하는 데서 끝내지 않고, **요구 성능을 만족하지 못하기 시작하는 조건(Failure Boundary)**을 탐색하고 **반복 가능한 자동 검증·회귀 테스트(Regression Testing)**를 구축합니다.

1. 공개 자율주행 Camera 데이터셋 및 사전학습 객체 검출기(YOLO 계열)로 정상 영상 성능(Baseline) 측정
2. 저조도(Brightness 감소), Blur, Noise, Fog의 통제된 영상 열화 조건 생성
3. Precision, Recall, mAP, False Negative, 추론 시간 등 정량 평가
4. 요구 성능의 PASS/FAIL 전환 구간, 복합 열화 조건의 Robustness Map 분석
5. 테스트 자동 실행, 기존 결과 대비 Regression 검출, 소규모 GitHub Actions 기반 CI/CT 시도

**주의:** 데이터셋·모델 버전 및 PASS/FAIL Threshold는 예비 평가 이후 본 실험 전에 확정합니다. 영상 인지 성능 검증은 실차 주행 안전성 보증과 다릅니다.

## 연구 흐름 (계획)

```text
Labeled Camera Dataset
       ↓
Image Degradation Generator
(Brightness / Blur / Noise / Fog)
       ↓
Pretrained Object Detector
       ↓
GT-based Evaluation
(Precision / Recall / mAP / FN / Latency)
       ↓
Requirement Check → PASS / FAIL
       ↓
Failure Boundary / Robustness Map
       ↓
Automated Regression Test
       ↓
Lightweight CI / CT
```

## 진행 상태 (2026-10-22)

| 항목 | 상태 |
|---|---|
| RUS 연구 주제 및 10~12월 연구계획 변경안 정리 | 완료 (문서화) |
| 9월 LiDAR Point Dropout 실험 | 기존 선행연구로 보존 |
| Camera 데이터셋 / 모델 선정과 Baseline 평가 | 예정 |
| 열화 Generator / 성능 평가 | 예정 |
| Failure Boundary / 복합 열화 | 예정 |
| Test Runner / Regression Test / CI | 예정 |

아직 구현되지 않은 Camera 검증 기능은 완료로 표시하지 않습니다.

## 일정 / 문서

- [연구계획 변경안](docs/research_plan_2026_10_22.md)
- [10~12월 주차별 로드맵](docs/roadmap_2026_10_22.md)
- [Test Case / Metric 설계](docs/test_plan.md)
- [연구 변경 이력](docs/CHANGELOG.md)
- [Notion 연구일지·실험 기록](https://app.notion.com/p/f81225ee6937832b87c9019d33780aa7)

## 이전 LiDAR 연구 보존

2026년 9월에는 ROS2 Humble과 공개 VLP-16 데이터에서 PointCloud2 / rosbag을 활용하고 **Point Dropout 10%, 30%, 50%, 70%** 실험을 수행했습니다. 해당 내용은 신규 Camera 연구의 *선행 연구 경험*으로 보존합니다.

- [기존 ROS2 LiDAR Dropout 코드](src/lidar_dropout/)
- [변경 전 README 백업](docs/archive/README_lidar_original_2026-09.md)

## 졸업프로젝트와의 구분

- **졸업프로젝트:** CARLA + Autoware + V2V Cooperative Driving의 시스템 수준 검증
- **RUS:** Camera 객체 검출 SW의 열화 조건별 한계 및 자동 회귀검증

이번 RUS에는 CARLA 기반 전체 주행, V2V, Planning/Control, UGV 실환경 주행, HIL 구현은 포함하지 않습니다.

## 다음 학기 연구 방향 (제안)

2027년 1학기에 실제 UGV Camera 데이터를 수집하고, 이번 학기 검증 프레임워크를 재사용하여 인위적 영상 열화와 실제 저조도·역광·진동 환경의 **Synthetic-to-Real 강건성 차이**를 분석할 계획입니다.
