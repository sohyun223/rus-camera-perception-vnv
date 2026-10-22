# Test Plan — Camera Perception Robustness & Automated V&V

> 설계 문서 (2026-10-22). 작성 당시 Camera 실험/CI는 **아직 구현·실행되지 않았음**.

## 검증 대상 및 공통 설정

- 공개 도로 영상 데이터셋(정답 Bounding Box가 있는 데이터)
- 단일 사전학습 객체 검출기 및 검출 대상 클래스 정의
- 고정된 평가 이미지 ID subset (동일한 원본 영상에 열화 적용)
- 평가 기준: Precision, Recall, mAP, False Negative, 평균 추론 시간
- reproducibility: 모델 weights / confidence / IoU / transform 파라미터 / 라이브러리 버전 / seed 기록

## Test Cases

| ID | 입력 조건 | 목적 |
|---|---|---|
| TC-00 | Original | 정상 Baseline 확보 |
| TC-01 | Brightness 감소 (약/중/강) | 저조도 취약성 |
| TC-02 | Blur (약/중/강) | 선명도 변화 |
| TC-03 | Gaussian Noise (약/중/강) | 영상 센서 잡음 |
| TC-04 | Fog (약/중/강) | 가시성 저하 |
| TC-05 | Low-light + Blur | 복합 열화 영향 |
| TC-06 | Fog + Blur | 복합 열화 영향 |
| TC-07 | 코드/모델 설정 수정 | 기준 대비 Regression 감지 |
| TC-08 | 빈 입력·미존재 파일 (확장) | 예외 처리 |

## Validation / Failure Boundary

1. Normal Baseline과 파일럿 열화 테스트를 실시한다.
2. 교수님/멘토와 요구 성능 판정 기준을 정의한 후 **본 실험 전에 고정**한다.
3. 각 강도와 복합 조건에서 동일한 Dataset subset으로 PASS/FAIL 판정한다.
4. PASS에서 FAIL로 전환되는 열화 수준을 기록한다. 성능이 비단조적이면 여러 전환 구간을 모두 기록한다.
5. 모델/전처리 변경 이후 동일 실험 결과를 고정 기준과 비교해 Regression을 탐지한다.

> 이 테스트의 PASS는 *설정한 객체 검출 성능 기준을 만족했다*는 뜻이지, 차량 운행의 안전성을 보증하지 않는다.

## 자동화 파이프라인 (목표)

```text
test_cases.yaml
   |
Load labeled images + model
   |
Generate controlled degraded images
   |
Infer with fixed detector
   |
Compare detections to Ground Truth
   |
Compute metrics, CSV, plots
   |
Requirement PASS/FAIL
   |
Compare to stored reference results
   |
Regression Report
```

GitHub Actions에서는 큰 데이터·GPU를 요구하는 모든 실험을 돌리지 않고, 소규모 deterministic unit/smoke tests만 실행한다.

## 계획 결과물

- `results/baseline.csv`
- `results/single_degradation.csv`
- `results/combined_degradation.csv`
- `results/robustness_map.csv`
- `results/regression_report.json`

모든 경로는 **예상 출력 파일명**이며, 실제 생성된 파일이라는 뜻이 아니다.
