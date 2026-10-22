# 연구 변경 이력

## 2026-10-22 — 연구 방향 변경 (계획)

- **기존 연구**: 환경 변화 및 센서 데이터 열화에 강건한 2D/3D LiDAR 융합 기반 장애물 인식 성능 향상
- **변경 연구**: 환경 및 영상 열화 조건에서 Camera 기반 자율주행 인지 소프트웨어의 강건성 한계 분석 및 자동 검증
- **보존 내용**: 9월 VLP-16 / ROS2 / PointCloud2 / Point Dropout (10·30·50·70%) 실험, `src/lidar_dropout/` 코드 및 기존 Git commit
- **변경 목적**: Camera Perception V&V, Failure Boundary, 반복 테스트와 Regression/CI·CT 연구에 집중
- **이번 학기**: Camera 이미지 열화 및 검출 성능 검증 체계 구축
- **다음 학기 제안**: UGV 실제 Camera 데이터에서 Synthetic-to-Real 강건성 비교
- **승인 상태**: 연구계획 변경안 문서화, 공식 승인 별도 확인 필요

기존 연구문서는 [원본 README 백업](archive/README_lidar_original_2026-09.md) 참조.
