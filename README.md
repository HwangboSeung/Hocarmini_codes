# Hocarmini - 라즈베리파이 자율주행 로봇 자동차 프로젝트

라즈베리파이(Raspberry Pi)를 기반으로 한 IoT 교육용 로봇 자동차 프로젝트입니다.  
기초 GPIO 제어부터 컴퓨터 비전을 활용한 차선 인식 자율주행까지 단계별로 구성되어 있습니다.

---

## 목차

- [프로젝트 개요](#프로젝트-개요)
- [하드웨어 구성](#하드웨어-구성)
- [소프트웨어 환경](#소프트웨어-환경)
- [GPIO 핀 맵](#gpio-핀-맵)
- [폴더 구조](#폴더-구조)
- [주요 기능](#주요-기능)
- [실행 방법](#실행-방법)
- [학습 단계](#학습-단계)

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **플랫폼** | Raspberry Pi |
| **언어** | Python 3 |
| **주요 제어** | DC 모터, 서보 모터, 초음파 센서, 카메라 |
| **응용 기술** | GPIO 제어, PWM, 컴퓨터 비전(OpenCV), 자율주행 |

---

## 하드웨어 구성

- **Raspberry Pi** (메인 제어 보드)
- **DC 모터 + L298N 모터 드라이버** (구동 모터)
- **서보 모터** (스티어링 제어)
- **HC-SR04 초음파 센서** (장애물 감지)
- **라즈베리파이 카메라 모듈** (피카메라, 차선 인식)
- **조이스틱** (수동 원격 제어)
- **LED, 버튼** (기초 GPIO 실습)

---

## 소프트웨어 환경

```
Python 3.x
gpiozero      - 고수준 GPIO 제어
RPi.GPIO      - 저수준 GPIO 제어
picamera2     - 라즈베리파이 카메라 제어
OpenCV (cv2)  - 영상 처리 및 차선 인식
NumPy         - 수치 계산
lgpio         - GPIO 백엔드 드라이버
```

> **설치 명령어 (라즈베리파이)**
> ```bash
> pip install gpiozero RPi.GPIO picamera2 opencv-python numpy
> sudo apt install python3-lgpio
> ```

---

## GPIO 핀 맵

### Hocar 자동차 (hocar_24 시리즈)

| GPIO 핀 | 역할 |
|---------|------|
| GPIO 25 | DC 모터 ENA (PWM 속도 제어) |
| GPIO 24 | DC 모터 IN1 (방향) |
| GPIO 23 | DC 모터 IN2 (방향) |
| GPIO 17 | 서보 모터 (스티어링) |
| GPIO 27 | 초음파 Trigger |
| GPIO 22 | 초음파 Echo |

### 자율 주행 자동차 (autocar_01)

| GPIO 핀 | 역할 |
|---------|------|
| GPIO 4  | 왼쪽 모터 전진 |
| GPIO 14 | 왼쪽 모터 후진 |
| GPIO 17 | 오른쪽 모터 전진 |
| GPIO 27 | 오른쪽 모터 후진 |
| GPIO 22 | 초음파 Trigger |
| GPIO 23 | 초음파 Echo |

### 기초 실습

| GPIO 핀 | 역할 |
|---------|------|
| GPIO 17 | LED |
| GPIO 2  | 버튼 입력 |
| GPIO 18 | 서보 / PWM |
| GPIO 23 | 초음파 Echo |
| GPIO 24 | 초음파 Trigger |

---

## 폴더 구조

```
Hocarmini_codes/
│
├── 2026code/                   # 기초 센서/모터 제어 실습 코드
│   ├── led_*.py                  - LED 점등 및 점멸 제어
│   ├── button_*.py               - 버튼 입력 처리
│   ├── servo_*.py                - 서보 모터 각도 제어
│   ├── pwm_*.py                  - PWM 기반 속도 제어
│   ├── ultrasonic_*.py           - 초음파 센서 거리 측정
│   ├── DCMotor_*.py              - DC 모터 기본 제어
│   ├── GPIOInput*.py             - GPIO 입력 핀 읽기
│   ├── autocar_01.py             - 장애물 회피 자율 주행
│   └── basics/                   - 파이썬 기초 문법 예제
│       ├── condition.py
│       ├── loops.py
│       ├── function.py
│       └── lists.py
│
├── activities/                 # 수업 활동 및 과제
│   ├── activity_1.py ~ activity_11.py
│   ├── Activity-01.py, Activity-02.py
│   └── picamera2_video_test1.py
│
└── tested_code/                # 실제 동작 검증된 완성 코드
    ├── hocar_24/                 - 완전 통합 자동차 제어 시스템
    │   ├── hocar.py              → 핵심 제어 클래스 (모터 + 센서)
    │   ├── hocar_24.py           → 조이스틱 원격 제어
    │   ├── hocar_24_ai.py        → AI 기반 자동 제어
    │   └── hocar_24_ai2.py       → AI 자동 제어 개선 버전
    │
    ├── lane/                     - 차선 인식 자율주행
    │   ├── whiteExample-01~05.py → 단계별 차선 인식 알고리즘
    │   ├── whiteExample-04Steering.py → 스티어링 제어 통합
    │   └── cam*.py, video*.py    → 카메라 영상 취득
    │
    ├── camera/                   - 카메라 모듈 테스트
    │   ├── picam2_stream.py      → 실시간 스트리밍
    │   ├── capture_jpeg.py       → 이미지 캡처
    │   └── video.py, easy_video.py
    │
    ├── DCmotor-AI.py             - DC 모터 PWM 속도 제어
    ├── servo-1.py, servo-2.py    - 서보 모터 제어
    ├── distance.py               - 초음파 거리 측정
    ├── joystick.py               - 조이스틱 입력 처리
    └── L298n.py, GS965R.py       - 모터 드라이버 제어
```

---

## 주요 기능

### 1. 장애물 회피 자율주행 (`2026code/autocar_01.py`)

- **초음파 센서**로 전방 30cm 이내 장애물 감지
- 감지 시 자동으로 **정지 → 후진 → 우회전 → 재전진**
- `gpiozero`의 이벤트 기반(`when_in_range`) 구현

```python
# 동작 방식
sensor.when_in_range  → 정지 후 후진(0.5초) → 우회전(0.5초) → 전진 재개
sensor.when_out_of_range → 정상 전진 복귀
```

### 2. 조이스틱 원격 제어 (`tested_code/hocar_24/hocar_24.py`)

- 조이스틱 **X축**: 스티어링 각도 조절
- 조이스틱 **Y축**: 모터 속도 조절
- 버튼 **Z**: 전진 / **TR**: 후진 / **Y**: 정지 / **TL**: 직진 정렬

### 3. Hocar 핵심 제어 클래스 (`tested_code/hocar_24/hocar.py`)

| 메서드 | 기능 |
|--------|------|
| `setMotorControl(speed, state)` | 모터 속도(0~100%) 및 방향(전진/후진/정지) 제어 |
| `setServoAngle(angle)` | 스티어링 각도 설정 (60° ~ 120°) |
| `measureDistance()` | 초음파 거리 측정 (상보필터 노이즈 제거 적용) |

### 4. 차선 인식 자율주행 (`tested_code/lane/`)

- **OpenCV** 기반 흰색 차선 검출
- ROI(관심영역) 설정으로 하단 도로 영역만 분석
- 좌/우 차선 중심 계산 후 **자동 스티어링 각도 산출**

```python
# 스티어링 계산
steer = arctan2(midx - center_offset, height)
```

### 5. 카메라 스트리밍 (`tested_code/camera/`)

- **Picamera2** 모듈 기반 실시간 스트리밍
- 이미지/비디오 캡처 및 저장

---

## 실행 방법

```bash
# 1. 장애물 회피 자율주행
python3 2026code/autocar_01.py

# 2. 조이스틱 제어
python3 tested_code/hocar_24/hocar_24.py

# 3. 차선 인식 (이미지 테스트)
python3 tested_code/lane/whiteExample-04Steering.py

# 4. 카메라 스트리밍
python3 tested_code/camera/picam2_stream.py

# 5. 기초 실습 (LED 점멸)
python3 2026code/led_01_blink.py
```

> **주의**: 모든 GPIO 코드는 라즈베리파이에서 실행해야 합니다.

---

## 학습 단계

```
[1단계] Python 기초
   └── basics/ (조건문, 반복문, 함수, 리스트)

[2단계] 단일 부품 제어
   └── 2026code/ (LED, 버튼, 서보, 초음파, DC 모터)

[3단계] 수업 활동
   └── activities/ (통합 실습 과제)

[4단계] 자동차 완성 시스템
   └── tested_code/hocar_24/ (조이스틱 제어 + 장애물 회피)

[5단계] 컴퓨터 비전 자율주행
   └── tested_code/lane/ (카메라 + 차선 인식 + 스티어링 자동 제어)
```

---

## 라이선스

교육 목적의 프로젝트입니다.
