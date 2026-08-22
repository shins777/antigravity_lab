---
name: agy_setting
title: Antigravity 설치 및 환경 구성 실습 가이드
version: 1.0.0
description: Antigravity 환경 설치, 의존성 구성 및 초기 실행 검증을 위한 교육용 실습용 자료 markdown 문서(md) 생성 SKILL 모듈
tags:
  - setup
  - environment
  - antigravity
  - lab
---

# Antigravity 설치 및 환경 구성
아래 내용에 대해서 실습을 진행하며 Antigravity 환경을 구축하고 초기 실행을 검증하는 markdown 문서( .md 파일를 만들어주는 SKILL 모듈입니다. 

## 1. 개요 및 학습 목표
* Antigravity 실행에 필요한 시스템 요구사항 및 패키지 의존성을 확인합니다.
* 가상 환경을 구축하고 Antigravity 코어를 설치합니다.
* 기본 설정 파일을 작성하고 정상 동작 여부를 검증합니다.

---

## 2. 사전 준비 사항 (Prerequisites)
* **OS:** Linux (Ubuntu 22.04 LTS 권장) / macOS / Windows WSL2
* **Python:** 3.10 이상
* **Package Manager:** `pip` 또는 `uv` / `poetry`
* **필수 권한:** 터미널 접근 및 패키지 설치 권한

---

## 3. 실습 단계 (Lab Steps)

### Step 1: 작업 디렉터리 생성 및 가상환경 설정
```bash
# 1. 작업 디렉터리 생성 및 이동
mkdir -p ~/antigravity-lab/agy_setting
cd ~/antigravity-lab/agy_setting

# 2. Python 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate