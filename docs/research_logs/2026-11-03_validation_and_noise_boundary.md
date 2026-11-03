# 100장·3종 열화 파일럿 및 잠정 자동 판정

기록 갱신: 2026-11-03 (KST). 근거는 사용자가 연구실 PC에서 실행해 공유한 CSV 및 터미널 출력이다. 본 문서의 기록일이 모든 선행 실험의 실제 수행일이라는 뜻은 아니다.

## 평가 설정과 완료 범위

- KITTI 고정 100장, YOLO11n, 자동차(car)·보행자(person). GT는 각각 416개·78개.
- 추론: device=0, imgsz=640, conf=0.25, NMS IoU=0.7, rect=True.
- 평가: 기존 사용자 정의 평가기, 정답 연결 IoU=0.5. 공식 KITTI 점수·AP/mAP가 아니다.
- 기존 10조건: 원본 + 밝기 0.7/0.4/0.2 + Gaussian Blur σ=1/2/3 + Gaussian Noise 표준편차 10/20/30.
- 추가 탐색: 같은 100장·모델·설정·고정 시드로 Noise 25, 이후 22를 검사했다. 각 실행에 원본도 포함했고, 원본 집계는 기존과 같았다.
- 파일럿은 모델 학습이 아닌 사전학습 검출기의 성능 평가이다.

## 개별 실행과 통합 실행 비교

JSON 설정을 읽는 `scripts/run_validation.py`로 열화 생성→YOLO 추론→평가→CSV 저장을 연결했다. 개별 실험 CSV와 통합 CSV의 GT, predictions, TP, FP, FN, ignored는 동일하고 precision·recall은 허용오차 1e-12 이내로 비교하여 **20/20행 일치**를 확인했다. 20행은 기존 10조건 × 2클래스다. 개별 박스 좌표·신뢰도까지 일치함을 검증한 것은 아니다.

## 잠정 기준 draft_v0.1

- 설정파일: `configs/validation_criteria.json`; status=`provisional`.
- 재현율 유지율 = 해당 조건 재현율 / 원본 재현율.
- 자동차와 보행자가 각각 **90% 이상(경계 포함)**을 유지해야 조건 전체 PASS.
- 원본은 REFERENCE로 두고 PASS/FAIL 집계에서 제외한다.
- 기준은 연구용 초안이다. 멘토 검토와 본 평가 시작 전 기준 확정이 남아 있다.
- 예: Noise 22 보행자는 재현율 자체가 50.00%, 원본 대비 유지율은 39/44=88.64%이므로 FAIL이다.

| 조건 | 자동차 재현율 유지율 | 보행자 재현율 유지율 | 조건 판정 |
|---|---:|---:|---|
| original | 100.00% | 100.00% | REFERENCE |
| brightness_0p7 | 98.96% | 100.00% | PASS |
| brightness_0p4 | 95.16% | 97.73% | PASS |
| brightness_0p2 | 88.93% | 95.45% | FAIL |
| blur_sigma_1 | 99.65% | 100.00% | PASS |
| blur_sigma_2 | 92.73% | 97.73% | PASS |
| blur_sigma_3 | 88.24% | 81.82% | FAIL |
| noise_std_10 | 97.23% | 93.18% | PASS |
| noise_std_20 | 92.04% | 90.91% | PASS |
| noise_std_30 | 81.66% | 59.09% | FAIL |
| noise_std_22 | 90.66% | 88.64% | FAIL |
| noise_std_25 | 87.54% | 68.18% | FAIL |

기존 열화 9조건은 **PASS=6, FAIL=3**이다. 추가 Noise 22·25는 각각 FAIL이며 기존 10조건 집계에 합쳐 세지 않았다.

## 추가 Noise 탐색 해석

Noise 20에서는 두 클래스 모두 통과하지만 22에서는 보행자가 미달했다. 25에서는 두 클래스 모두 미달했다. 이번 고정 표본·시드·잠정 기준에서 확인한 평가점이다. 정확한 최대 허용 강도, 단조적 성능 저하, 독립 본 평가 결과, 실차 안전성으로 일반화하지 않는다. 추가 강도 탐색은 일단 종료했다.

## Noise 실패 사례 분석

원본 대비 Noise 30에서 자동차는 새로 놓침 66개·새로 찾음 13개로 TP가 순 53개 감소(289→236), 보행자는 새로 놓침 18개·새로 찾음 0개로 순 18개 감소(44→26)했다. 전체 새로 놓침 84개·새로 찾음 13개이며 집계 변화와 일치한다. 새로 놓침은 GT의 TP→FN 전환이며 예측 박스의 완전 소실과 같은 의미는 아니다. 연구실 결과 위치: `results/noise_pilot_100/failure_comparison/`.

## 자동 판정과 확인한 회귀검증 범위

`scripts/judge_validation.py`는 저장된 summary.csv를 읽어 클래스별 유지율과 조건 전체 판정을 계산하고 입력 CSV 옆에 judgement.csv를 저장한다. YOLO를 다시 실행하지 않는다.

`--summary` 옵션을 추가해 입력 경로를 선택할 수 있도록 했다. 들여쓰기 오류를 수정한 후 Noise 22·25 모두 PASS=0/FAIL=1 및 파일 저장을 확인했다. 옵션 없는 기존 실행에서도 PASS=6/FAIL=3이 유지됐다.

확인한 것은 경로 옵션 추가 후 기존 기본 판정 유지와 집계 일치이다. 모델 변경에 따른 성능 회귀 자동 탐지, 개별 예측 상세 비교, CI는 아직 미구현이다.

## 연구실 PC 실행 명령

```bash
python scripts/run_validation.py
python scripts/judge_validation.py
python scripts/run_validation.py --config configs/validation_noise_22.json --out results/validation_noise_22
python scripts/judge_validation.py --summary results/validation_noise_22/summary.csv
python scripts/run_validation.py --config configs/validation_noise_25.json --out results/validation_noise_25
python scripts/judge_validation.py --summary results/validation_noise_25/summary.csv
```

통합 실행은 기존 출력 폴더가 있으면 중단하므로 위 실험 명령을 그대로 재실행할 때는 새로운 --out 경로가 필요하다. 판정 코드는 해당 폴더의 judgement.csv를 갱신한다.

## 백업과 원격 보관 범위

- 사용자 PC 백업: `/home/sohyun/camera_perception_backup_20261103_165357.tar.gz`.
- 크기: 사용자 출력 4489.1 MB (1024² 바이트 단위 계산).
- 포함: scripts, configs, results, yolo11n.pt; requirements_initial.txt가 존재하면 포함하는 코드로 실행.
- 제외: KITTI 원본 데이터와 .venv. gzip 전체 읽기 무결성 검사 통과. 복원 시험은 수행하지 않았다.
- 압축파일 자체를 GitHub에 올린 것은 아니다.
- 이 커밋의 CSV는 제공된 터미널 수치로 재구성했다. 비율은 TP/FP/GT로 계산했고 계수 관계를 검증했다. 원본 파일의 바이트 동일성은 주장하지 않는다.
- 연구실 PC의 최신 실제 .py·manifest·상세 JSON·신규 이미지·전체 패키지 목록은 이번 원격 업데이트에서 직접 확보하지 않았다. 아래 문서/CSV/기준 설정과 사용자 PC의 실행 완료를 구분한다.

## 다음 작업

11/5 보고서의 수행 내용과 사진을 정리하고 멘토 검토·서명을 준비한다. 이후 잠정 기준의 근거와 최종 기준을 확정하고 파일럿과 분리된 데이터로 본 평가를 진행한다. Fog·복합 열화·mAP·CI는 완료 항목으로 표시하지 않는다.
