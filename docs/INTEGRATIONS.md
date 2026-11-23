# 채용사이트 연동 현황

| 사이트 | 상태 | 필요 조건 |
|---|---|---|
| 고용24 | 공식 API 연동 코드 제공, 미활성 | 고용24 기업회원의 API 승인키를 GitHub Actions secret WORK24_API_KEY로 설정 |
| Greenhouse | 공식 공개 보드 수집기 제공, 미활성 | 실제 board token을 data/sources.json에 등록 |
| Lever | 공식 공개 보드 수집기 제공, 미활성 | 실제 board token을 data/sources.json에 등록 |
| 사람인 | 미연동 | 이용 가능한 공식 API 또는 허용된 수집 방식 확인 필요 |
| 잡코리아 | 미연동 | 이용 가능한 공식 API 또는 허용된 수집 방식 확인 필요 |
| 기업 채용 페이지 | 미연동 | 기업별 허용된 피드 또는 API 확인 필요 |

수집하지 못한 공고를 임의로 생성하지 않습니다. GitHub Pages는 공개 웹사이트이므로 API 키를 소스 파일에 쓰지 마세요.

고용24 공식 API 안내: https://www.work24.go.kr/cm/e/a/0110/selectOpenApiSvcInfo.do?fullApiSvcId=000000000000000000000000000000
