# Day_6을 웹툰으로 복습하기

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변과 웹툰 | [웹툰 열기](#답변) |
| 헷갈리기 쉬운 점 | [주의점](#헷갈리기-쉬운-점) |
| 참고 자료 | [출처](#참고-자료) |

- 최초 기록일: 2026-10-21
- 수정일: 2026-10-21
- 분류: Python, Coding
- 핵심 용어: Pydantic, BaseModel, Field, Validator, 중첩 모델, 직렬화, PATCH, FastAPI, CRUD

## 질문

`Day_6/`에 나온 내용을 모두 이해하기 쉽게 정리하되, 개발서가 아닌 웹툰 형식으로 만들어 주세요.

## 답변

**[데이터 학교의 신입 개발자 — 웹툰](../Day_6/webtoon/index.html)**

노란 후드의 신입 개발자 ‘하루’와 검사 로봇 ‘파이’가 데이터 학교를 운영하는 이야기로 구성했다. 실제 폴더의 ch02~ch08을 7화·42컷으로 다룬다. `index.html`을 브라우저로 열면 읽을 수 있으며 `assets/`와 나머지 파일을 같은 폴더에 둔다. 본문에는 인터넷이나 서버가 필요하지 않다.

| 회차 | 이야기 | 복습 내용 |
| --- | --- | --- |
| 1 | 입학 신청서가 말을 안 들어요! | 일반 클래스와 BaseModel, 타입 변환, 필수/기본값, Optional/Union, **, 오류, import |
| 2 | 아무나 들어올 수는 없지! | Field의 범위·길이·패턴, EmailStr, Literal, ConfigDict, strict bool |
| 3 | 규칙표에 없는 사건 | field_validator, classmethod, before/after, 전처리, 비밀번호·날짜 관계 검사 |
| 4 | 택배 상자 안에 또 상자가! | Address/OrderItem/Order, Enum, property 합계, 중첩 오류, Learner/Course |
| 5 | 지우라는 말은 안 했는데요! | model_dump/JSON, 생략과 None, exclude_unset/exclude_none, 병합·재검증 |
| 6 | 데이터 학교, 창구를 열다 | FastAPI, HTTP 요청, CRUD, PUT/PATCH, 201/204/404/422/501 |
| 7 | 하루의 첫 서비스, 개교합니다 | models/store/app 역할, 회원·작업 관계, 필터, 409, 응답 모델, 최종 TODO |

각 화에 그림, 대사, 짧은 코드 쪽지, 복습 질문과 펼쳐 보는 답을 넣었다. 원본 파일과 현재 실습 상태도 회차 끝에 연결했다. 원본 Python 실습 파일은 이 작업에서 수정하지 않았다.

## 헷갈리기 쉬운 점

- `str | None`은 None을 허용한다는 뜻이다. 입력 생략은 기본값 유무로 구분한다.
- `exclude_unset=True`는 보내지 않은 필드를 제외한다. 명시적으로 보낸 None을 지우는 `exclude_none=True`와 다르다.
- 부분 수정은 기존 데이터와 변경분을 합친 뒤 최종 모델로 다시 검사한다.
- 현재 `Signup.username`은 길이 검사 뒤 공백을 정리한다. 정리 후의 길이가 자동으로 재검사된다고 설명하지 않았다.
- ch06의 `TaskPatch`는 title/done의 명시적 None만 거부하고 due=None은 허용한다. 원본의 포괄적인 주석보다 실제 조건을 기준으로 설명했다.
- ch08의 `StrictModel`이라는 이름만으로 모든 필드에 엄격한 타입 검사가 적용되는 것은 아니다.
- ch08의 `TaskOut`은 internal_note를 응답에서 제외하지만, 저장소에서 삭제하는 것은 아니다. 로그인·권한 검사도 별개의 기능이며 현재 예제에 없다.
- `day6_3.py`에는 정의되지 않은 `MemberOut` 참조가 있다. `day6_1.py`의 user2는 실제로 NormalClass 인스턴스다. 웹툰에서 현재 상태를 구분했다.
- ch03의 exercise.py는 비어 있고, 다른 exercise/starter의 TODO도 완성 예제와 구분했다.
- 코드 쪽지의 값 변화는 원본 독해에 기반한 설명이다. 전체 실습 코드를 실행한 결과라고 주장하지 않는다.

## 참고 자료

- [Day_6 원본 폴더](../Day_6/): ch02~ch08의 모든 `.py`, `.http` 파일 확인.
- [기존 Field 학습 기록](2026-10-21-pydantic-field.md)
- [기존 Validator 학습 기록](2026-10-21-pydantic-validator-error.md)
- [기존 Enum 학습 기록](2026-10-21-python-enum.md)
- [기존 bool 학습 기록](2026-10-21-python-bool.md)
- [Pydantic 공식 문서: Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Pydantic 공식 문서: Serialization](https://docs.pydantic.dev/latest/concepts/serialization/)
- [FastAPI 공식 문서: Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)
- [삽화 제작 프롬프트](../Day_6/webtoon/image-prompts.txt): 내장 image_gen 도구 사용.
