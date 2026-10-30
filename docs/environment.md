# Camera 연구 개발 환경과 실행 방법

실행 확인일: 2026-10-30 (KST). 기록 갱신일: 2026-10-31.
근거: 연구실 PC에서 실행한 사용자 제공 터미널 로그와 검출 결과 캡처.

## 확인된 환경

| 항목 | 값 |
|---|---|
| OS | Ubuntu 22.04.5 LTS (기존 연구 환경 기록) |
| Python | 3.10.12 |
| GPU | NVIDIA GeForce RTX 3060, 12GB |
| NVIDIA Driver | 580.178.04 |
| PyTorch | 2.7.1+cu128 |
| PyTorch CUDA runtime | 12.8 |
| Ultralytics | 8.4.193 |
| 모델 | YOLO11n (`yolo11n.pt`) |
| 연구 폴더 | `~/camera_perception_validation` |
| 가상환경 | `~/camera_perception_validation/.venv` |

`nvidia-smi`에 표시된 CUDA 13.0은 드라이버의 지원 버전 표시다. 실제 PyTorch가 사용하는 CUDA runtime은 12.8로 확인했다.
`torch.cuda.is_available()`는 True이고, GPU 행렬 곱 결과는 100.0으로 확인했다.

## 새 터미널에서 다시 시작하기

```bash
cd ~/camera_perception_validation
source .venv/bin/activate
```

터미널을 닫아도 가상환경과 설치된 패키지는 유지된다. 새 터미널에서는 활성화만 다시 하면 된다.

## 초기 설치에 사용한 명령

아래는 새로운 환경을 구성할 때의 기록이다. 이미 설치한 PC에서 매번 반복할 필요는 없다.

```bash
sudo apt update
sudo apt install python3-venv python3-pip
mkdir -p ~/camera_perception_validation
cd ~/camera_perception_validation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu128
python -m pip install ultralytics
```

마지막 설치 결과의 Ultralytics 버전은 8.4.193이었다. 이후 재구성할 때 이 직접 의존성 버전을 맞추려면 `python -m pip install ultralytics==8.4.193`을 사용한다. 전체 전이 의존성의 동일성까지 확인된 것은 아니다.

## GPU 계산 확인

```python
import sys
import torch
import ultralytics

print("Python 경로:", sys.executable)
print("PyTorch:", torch.__version__)
print("Ultralytics:", ultralytics.__version__)
print("PyTorch CUDA:", torch.version.cuda)
print("GPU 사용 가능:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU 이름:", torch.cuda.get_device_name(0))
    x = torch.ones((100, 100), device="cuda")
    y = x @ x
    torch.cuda.synchronize()
    print("GPU 계산 결과:", y[0, 0].item())
```

## 실제 실행한 첫 검출 명령

```bash
yolo predict model=yolo11n.pt source=https://ultralytics.com/images/bus.jpg device=0 imgsz=640 conf=0.25 save=True project=results name=first_prediction
```

실제 저장 위치는 실행 로그로 확인했다.

```text
~/camera_perception_validation/runs/detect/results/first_prediction/bus.jpg
```

결과 이미지 열기:

```bash
xdg-open ~/camera_perception_validation/runs/detect/results/first_prediction/bus.jpg
```

처음 안내했던 `~/camera_perception_validation/results/first_prediction/bus.jpg` 경로에는 파일이 없어 열기에 실패했다. 검출은 성공한 상태였으며, `Results saved to ...`에 나온 경로로 열어 해결했다. 재실행 시 폴더 이름에 숫자가 붙을 수 있으므로 실제 로그를 확인한다.

## 전체 패키지 버전 기록 (파일 확보 필요)

```bash
python -m pip freeze > requirements_initial.txt
```

이 명령은 설치된 패키지와 버전을 텍스트로 저장한다. 가상환경을 활성화하는 명령이 아니다.
연구실 PC의 실제 `requirements_initial.txt` 내용은 아직 전달받지 못했으므로 이 저장소에 전체 목록을 임의 생성하지 않았다. 위 표는 로그에서 확인된 주요 버전 기록이다.

## 기록 관리

- `.venv/`, 모델 가중치, 원본 데이터셋과 전체 실행 출력은 Git 추적에서 제외한다.
- 대표 결과 이미지는 `docs/assets/`에 선별 보관한다.
- 이번 예제 실행은 동작 확인이다. 정답 기반 Precision, Recall, mAP, FN 평가는 아직 수행하지 않았다.
