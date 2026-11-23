# Firmware Career Tracker

전국 펌웨어·임베디드 SW 채용공고를 한눈에 확인하는 개인 대시보드입니다.

- 목표 연봉: **4,500만 원 이상**, 연봉 미공개 공고도 포함
- 의료기기·대기업·자동차 전장·중견기업 우선
- 실제 확인된 공고만 표시하며 연봉을 추정하지 않습니다.
- GitHub Actions에서 매일 5회 데이터 갱신을 시도합니다.

## 배포
GitHub 저장소 Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save.

## 데이터 연동
기본 제공: 공개 Greenhouse / Lever 채용 보드 API. `data/sources.json`에 실제 채용 보드 식별자를 등록해야 수집됩니다. 사람인·고용24·잡코리아 등은 공식 접근 권한 및 별도 구현이 필요합니다. 현재 모든 사이트가 연결된 상태는 아닙니다.

## 주의
GitHub Pages는 공개 사이트입니다. 개인 연락처, 회사 내부 소스, 비밀 API 키를 커밋하지 마세요. 지원 상태는 브라우저 localStorage에 저장됩니다.
