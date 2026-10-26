# 이미지 생성 기록

- 도구: 내장 image_gen (imagegen 스킬)
- 기존 Notion 페이지와 수업 원본은 변경하지 않음.
- Day5는 자료 미확인으로 표시.
- 웹툰의 예약 서비스는 여러 수업 개념을 연결하기 위한 비유.

## 인포그래픽 프롬프트

Use case: infographic-diagram.
Create a polished Korean educational architecture infographic as a large high-resolution landscape poster, ideally 2400x1600 or larger. Audience is a beginner learning Python through FastAPI. Clear beautiful professional information design, generous whitespace, navy headings on warm ivory, teal and blue main flows, purple for object design, amber for testing. This is an explanatory course diagram, not a screenshot. All Korean text must be crisp and carefully typeset. No gibberish or tiny body text.
Main title verbatim: "Day1–Day8, 하나의 API로 연결하기"
Subtitle: "기초 문법 → 데이터 구조 → 객체 설계 → 검증 → 비동기 처리 → 테스트"
Three clear horizontal layers:
TOP: Learning journey, 8 distinct numbered cards in a left-to-right sequence. Each card has a small elegant illustrated icon and ONLY these exact short labels:
"Day1" / "입력·조건·반복"
"Day2" / "자료구조·필터링"
"Day3" / "함수·객체·예외"
"Day4" / "난수·대입·교환"
"Day5" / "자료 미확인"
"Day6" / "Pydantic·FastAPI"
"Day7" / "async·HTTPX"
"Day8" / "API 검증·테스트"
Day5 is gray dashed, explicitly unknown, no invented topic. Main confirmed progression arrow from Day4 bypasses Day5 and continues to Day6; dotted stub to Day5. Do not suggest Day5 is a technical dependency.
MIDDLE, dominant large architecture panel heading "요청이 처리되는 구조". Five clearly connected left-to-right stages:
"클라이언트" illustrated browser sending a JSON envelope
→ "입력 검증" illustrated Pydantic shield with a short tag "Day6"
→ "업무 로직" illustrated condition gates, loop and object gears, tags "Day1–4"
→ "메모리 저장소" illustrated small dictionary drawer, tag "Day6"
→ "JSON 응답" illustrated response envelope through a filter labelled "응답 모델".
A secondary branch BELOW 업무 로직 to illustrated external cloud "외부 API" tag "Day7" and back, explicitly bidirectional, caption "await · 동시 대기". External API and memory are separate dependencies, not forced into one linear path.
Show small red rejection arrow leaving input validation labelled "422 입력 오류". Another small amber exit from business logic labelled "404 없음 · 409 충돌".
BOTTOM wide testing feedback rail, heading "Day8이 전체 흐름을 검증". Magnifying glass and checkboxes with exactly "정상값", "경계값", "오류 응답", "응답 구조", "실패 후 상태". Subtle upward bracket/arrows from testing rail to architecture stages; do not add spaghetti.
Footer two memory anchors: "Day2의 필터링 → Day6의 입력 검증" and "Day3의 상태 관리 → Day8의 상태 보존".
Small final note: "수업 코드 기반 개념도 · Day5 자료 미확인 · 저장소는 수업용 메모리 dict"
Use clear distinct arrowheads, readable numbered hierarchy and accurate relationships. No actual database cylinder because this course implementation uses in-memory dict. No React, SQL database, Kubernetes, authentication or invented frameworks. All 8 days must appear exactly once in the top journey. Avoid decorative clutter.

## 웹툰 프롬프트

Use case: illustration-story.
Create a finished high-resolution Korean educational WEBTOON POSTER explaining how Day1 through Day8 connect when learning Python and FastAPI. Portrait 2 columns x 4 rows, eight equal clearly separated story panels with a title band and a bottom summary ribbon. Ideally 1536x2560 or higher. This is a warm expressive educational Korean comic with real scenes, character actions, clear balloons and a continuous story; not a grid of infographic cards. Beautiful navy ink outlines, soft warm cream, mint, blue and purple coloring, bright welcoming lighting. Consistent protagonists across every actual lesson panel: a young Korean student developer with short dark bob, round glasses and yellow hoodie; a small rounded turquoise robot tutor. Characters visibly interact with meaningful objects and mechanisms. Carefully typeset readable Korean labels and short dialogue. No gibberish, no tiny text. Reading order left to right, then down. Each panel numbered by Day.
Title exact: "코드 조각이 API가 되기까지"
Subtitle exact: "Day1–Day8 연결 웹툰"
The narrative uses a simple reservation service ONLY as a learning metaphor that connects separate original exercises. Do not claim actual unified original project. No real AI prediction, no actual database; storage is memory dictionary.
Panel 1 upper left:
heading "Day1 · 입력과 흐름"
Student receives an input ticket "3석", robot directs it through an IF fork and a small repeated loop conveyor. One balloon from tutor: "입력받고, 판단하고, 반복해!"
Link bridge capsule on panel bottom: "값을 다루는 기초"
Panel 2 upper right:
heading "Day2 · 데이터와 규칙"
Student organizes named request envelopes into dictionary cubbyholes with short tags "이름" and "좌석". Funnel separates accepted and rejected items. Robot points to correct sorting.
One balloon: "데이터를 묶고 조건으로 걸러!"
bottom bridge capsule: "자료구조 → 검증 규칙"
Panel 3 second row left:
heading "Day3 · 객체와 책임"
Student and robot assemble a friendly reservation desk robot made of a data box and a function gear; protected glass window shows state "남은 좌석". Tutor separates responsibilities and guards a lever.
One balloon: "상태와 동작을 함께 관리해!"
bottom bridge capsule: "객체 설계 → 상태 관리"
Panel 4 second row right:
heading "Day4 · 값의 변화"
Close-up student swapping two cards "10" and "90" on a desk with a temporary tray and two curved arrows. Tutor stops a mistaken overwrite gesture, both are thoughtful. Only swap lesson, don't imply random IDs are suitable for real service.
One balloon: "덮어쓰기 전에 원래 값을 지켜!"
bottom bridge capsule: "대입 순서 → 상태 추적"
Panel 5 third row left:
heading "Day5 · 자료 미확인"
Quiet gray-mint interlude: student and robot at a closed archive drawer with a large question mark. No invented concept, no learning content.
One balloon: "이날의 수업 자료는 아직 없어."
bottom bridge capsule: "내용 추정 없이 비워 두기"
Panel 6 third row right:
heading "Day6 · 검증과 API"
Warm active service counter labelled "FastAPI". Robot scans request envelope with a shield labelled "Pydantic". A valid ticket goes green to a small MEMORY drawer labelled "dict"; invalid envelope goes into red tray labelled "422".
One balloon: "규칙을 통과한 요청만 처리해!"
bottom bridge capsule: "Day2의 규칙 + Day3의 객체"
Panel 7 bottom row left:
heading "Day7 · 비동기 연결"
Robot places three external service request envelopes into separate tubes to clouds, with three small overlapping horizontal waiting bars rather than CPU gears. Student keeps serving another visitor while responses arrive. Small label "await · gather". No assertion of CPU parallel acceleration.
One balloon: "기다리는 동안 다른 일도 해!"
bottom bridge capsule: "API 처리 → 외부 응답 동시 대기"
Panel 8 bottom row right:
heading "Day8 · 테스트와 상태 보존"
Student with clipboard and magnifier checks reservation counter. Clear mini three-step sequence drawn on counter: "4석" → "3석 예약" → "1석". A red rejected "2석 요청" envelope is stopped BEFORE drawer changes; remaining label stays "1석". Tutor gives thumbs up. This panel is crucial: rejected request must leave 1 seat unchanged.
One balloon: "실패한 요청은 상태를 바꾸면 안 돼!"
bottom bridge capsule: "문서·응답·상태를 함께 검증"
Bottom full-width clear ribbon with simple arrow flow and exact text:
"입력 → 규칙 → 객체 → 검증 → API → 비동기 → 테스트"
Small footer exact:
"수업 개념을 연결한 설명용 비유 · Day5 자료 미확인"
Hierarchy: large title, readable panel headings, medium balloons, shorter bridge capsules. Maintain enough whitespace to read text. No code dumps, no gradients behind text, no watermark. All eight Days must appear exactly once as panel headings. Strong coherent illustration quality and facial storytelling.

## 웹툰 오류 코드 수정 프롬프트

Use case: text-localization. Edit the attached Korean educational webtoon with one tiny accuracy correction ONLY. Preserve the entire illustration, layout, all characters, all eight panels, text, colors and all other content unchanged. In the bottom-right Day8 panel, the rejected request red/pink rectangle currently says "거절 (422)". Change ONLY that label to "거절 (409)" with identical font, size, color, positioning. It is insufficient remaining reservation seats, an HTTP 409 conflict. IMPORTANT: keep the separate Day6 validation error "422 (거절)" in the third-row right panel unchanged. Do not confuse these. No other corrections or rearrangements. Maintain full original portrait composition and high resolution.

