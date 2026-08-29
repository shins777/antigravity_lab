# Desktop CPU Status Dashboard

`psutil`, `Streamlit`, `Plotly`를 활용하여 로컬 데스크톱의 CPU 및 시스템 자원 상태를 실시간으로 모니터링하는 인터랙티브 대시보드입니다.

---

## 1. 주요 기능 (Features)

1. **실시간 CPU 종합 모니터링**:
   - 전체 CPU 사용률 (%) 및 실시간 시계열 타임라인 영역 차트
   - 물리 코어 vs 논리 코어 수, 동작 주파수(MHz), 로드 애버리지 (1분/5분/15분)
2. **코어별 사용률 (Per-Core Breakdown)**:
   - 각 코어별(Core 0 ~ Core N) 실시간 사용률 프로그레스 바 표시
3. **메모리(RAM) 및 스왑(Swap) 상태**:
   - 총 용량, 사용량, 가용량(GB) 및 실시간 사용률 게이지
4. **상위 리소스 점유 프로세스 테이블**:
   - CPU / RAM 점유율 기준 정렬
   - 프로세스 이름 필터링 검색
   - PID, 프로세스명, 스레드 수, 상태, 실행 유저 정보 제공
5. **동적 제어 및 알림**:
   - 자동 갱신 주기(0.5초 ~ 5.0초) 슬라이더 및 일시 정지(Pause) 토글
   - 고부하(High CPU) 임계치 초과 시 상단 실시간 경고 배너 표시

---

## 2. 디렉터리 구성

```text
lab/cpu_dashboard/
├── app.py           # Streamlit 메인 대시보드 애플리케이션
├── metrics.py       # psutil 기반 시스템 및 프로세스 메트릭 수집 모듈
├── run.sh           # 대시보드 실행 쉘 스크립트
├── requirements.txt # 의존성 패키지 목록
└── README.md        # 사용 설명서
```

---

## 3. 실행 방법 (How to Run)

### 1) 의존성 패키지 설치

```bash
pip install -r lab/cpu_dashboard/requirements.txt
```

### 2) 대시보드 실행

```bash
# 방법 1: 쉘 스크립트 실행
./lab/cpu_dashboard/run.sh

# 방법 2: 직접 streamlit 실행
streamlit run lab/cpu_dashboard/app.py
```

실행 후 브라우저가 자동으로 열리거나 `http://localhost:8501`에 접속하여 확인할 수 있습니다.
