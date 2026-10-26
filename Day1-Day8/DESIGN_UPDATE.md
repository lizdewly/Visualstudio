# 검정 편집형 디자인 적용

- 작업일: 2026-10-23 (Asia/Seoul)
- 입력: 사용자가 첨부한 BMW M 스타일 가이드와 선택한 Professional 방향.
- 적용: 검정 배경, 흰색 대형 제목, 700/300 굵기 대비, 직각 입력창, 흰색 윤곽선 버튼, 작은 삼색 마크, PC 2열·모바일 1열 배치.
- BMW 전용 폰트는 제공되지 않아 시스템 sans-serif 대체 글꼴을 사용합니다. BMW 로고는 포함하지 않습니다.
- 기존 서버 렌더링과 HTML 폼을 유지합니다. JavaScript와 새 Python 패키지를 추가하지 않습니다.
- Content-Security-Policy에 `img-src 'self'`를 추가해 자체 이미지 파일만 허용합니다.
- 자동차 이미지는 내장 image_gen으로 생성한 뒤 WebP로 변환했습니다. 이미지 경로: `static/hero-motorsport.webp` (98,970바이트).
- 이미지 생성 원본은 별도로 보존했습니다. 레이아웃 검증은 운영 DB 대신 `.test-tmp/design-preview.db`로 진행합니다.

## 검증

- 기존 pytest: 28 passed. 기존 HTTPX 사용 중단 예정 경고 1건.
- 실제 브라우저 1440 / 768 / 375 / 320px에서 가로 넘침 없음, 이미지 표시 확인.
- 임시 DB를 사용해 한글 글 등록과 목록 반영 확인.
- 화면 캡처: `preview-dark-desktop.png`, `preview-dark-mobile.png`.

## 생성 프롬프트 원문

Use case: ads-marketing. Asset type: wide website hero photograph for a black minimalist guestbook inspired by precision motorsport editorial design. Primary request: photorealistic unbranded graphite black performance coupe seen from low rear three-quarter angle on a dark racetrack at blue hour, very cinematic understated realistic commercial photography. Composition: wide panoramic horizontal image 2.5:1 or widest supported format, vehicle occupies right half with recognizable sculptural rear lights and black wheels, left half nearly black quiet track negative space for white headline to be overlaid in HTML, ample road around vehicle, no cropped car. Lighting: cool subdued blue rim light, gentle red tail lights, deep true blacks, image melts into black page at edges. No text, no badges, no logos, no watermarks, no BMW emblem, no UI elements. High-end lens realism, precise materials, restrained mood, no gradients drawn as graphics.
