# Archived original RUS README (before 2026-10-22 research scope update)

The content below preserves the original README as recorded immediately before the camera-based research plan update. The 2026-09 LiDAR ROS2 code remains in `src/lidar_dropout/`.

---

# RUS 2D/3D LiDAR Sensor Fusion

## Research Topic

환경 변화 및 센서 데이터 열화에 강건한
2D/3D LiDAR 융합 기반 장애물 인식 성능 향상 연구

## Overview

본 프로젝트는 RUS 학부생 연구인턴 프로그램의 일환으로
2D/3D LiDAR 센서 데이터의 열화 상황에서
장애물 인식 성능 변화를 분석하고,
향후 센서 융합을 통해 보다 강건한 인지 시스템을 구현하는 것을 목표로 한다.

## Development Environment

- Ubuntu
- ROS2
- Python
- RViz2

## Current Work

현재 3D LiDAR PointCloud에 Point Dropout을 적용하여
센서 데이터 손실 상황을 구현하고 있다.

실험 Dropout Rate:

- 10%
- 30%
- 50%
- 70%

## ROS2 Package

현재 사용 중인 ROS2 패키지:

```text
src/lidar_dropout/
