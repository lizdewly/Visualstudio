# LangGraph 기본 개념

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| LangGraph란 | [답변 보기](#답변) |
| 검색 후 답변하는 흐름 | [예제 보기](#예제) |
| LangChain과의 관계 | [주의점 보기](#헷갈리기-쉬운-점) |
| 공식 문서 | [참고 자료](#참고-자료) |

- 최초 기록일: 2026-10-16
- 수정일: 2026-10-16
- 분류: AI, Python, Coding
- 핵심 용어: LangGraph, 에이전트, State, Node, Edge, LangChain

## 질문

Langraph?

문맥상 `LangGraph`를 뜻하는 것으로 보고 설명합니다.

## 답변

**LangGraph는 여러 단계로 움직이는 AI 에이전트나 작업 흐름을 구성하고 실행하는 프레임워크입니다.** 각 단계의 처리와 다음 단계로 넘어가는 규칙을 연결하고, 단계 사이에 필요한 데이터를 유지합니다. 조건 분기와 반복을 포함하는 작업 흐름을 만들 수 있습니다. [공식 개요](https://docs.langchain.com/oss/python/langgraph/overview)

그래프는 여기서 막대그래프 같은 통계 그림이 아니라, 작업 단계와 연결 관계를 뜻합니다. 주요 개념은 다음 세 가지입니다. [Graph API 설명](https://docs.langchain.com/oss/python/langgraph/graph-api)

| 개념 | 쉬운 뜻 | 예 |
| --- | --- | --- |
| State 상태 | 단계 사이에 공유하는 현재 데이터 | 질문, 검색 결과, 작성한 답변 |
| Node 노드 | 실제 작업을 수행하는 단계 | 입력 확인 함수, 검색 함수, 답변 생성 함수 |
| Edge 엣지 | 다음에 실행할 단계를 정하는 연결 | 검색이 필요하면 검색으로, 아니면 답변으로 이동 |

## 예제

검색 결과를 확인하며 답변하는 챗봇을 설계한다고 생각해 봅니다. 다음은 개념 설명을 위한 흐름 예시입니다.

```text
질문 입력 → 검색 필요 여부 판단
              ├─ 필요함 → 검색 → 답변 작성
              └─ 필요 없음 ───→ 답변 작성
                                  ↓
                              답변 검토
                          ├─ 충분함 → 종료
                          └─ 부족함 → 검색으로 돌아감
```

각 작업 함수를 노드로, 이동 경로를 엣지로 정의합니다. 질문과 검색 결과 등은 상태로 전달합니다. 검색으로 돌아가는 규칙과 종료 조건은 개발자가 설계합니다. 노드는 AI 모델을 호출할 수도 있고 일반 파이썬 코드만 실행할 수도 있습니다. [Graph API 설명](https://docs.langchain.com/oss/python/langgraph/graph-api)

LangGraph는 상태 저장과 재개, 사람의 확인을 거쳐 이어서 실행하는 흐름도 지원합니다. 실제 저장과 재개를 사용하려면 체크포인터 등 관련 구성을 해야 합니다. [공식 개요](https://docs.langchain.com/oss/python/langgraph/overview)

## 헷갈리기 쉬운 점

- LangGraph 자체가 답변하는 AI 모델은 아닙니다. AI 호출과 다른 작업들의 실행 흐름을 관리하는 도구입니다.
- LangChain은 모델과 도구 연결 및 에이전트 구성 요소를 제공하고, LangGraph는 상태와 실행 흐름을 세밀하게 제어하는 기반 역할을 합니다. LangGraph를 사용하기 위해 반드시 LangChain을 함께 사용할 필요는 없습니다. [공식 개요](https://docs.langchain.com/oss/python/langgraph/overview)
- 학습 관점에서는 먼저 함수, 딕셔너리, 조건문을 이해한 뒤 “작업 함수들을 연결하고 데이터를 넘긴다”는 방식으로 접근하면 이해하기 쉽습니다.

## 참고 자료

- [LangGraph 공식 개요](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph Graph API 공식 설명](https://docs.langchain.com/oss/python/langgraph/graph-api)

공식 문서 확인일: 2026-10-16
