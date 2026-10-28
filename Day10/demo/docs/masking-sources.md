# 초기 마스킹 규칙 조사

조회·검토일: **2026-10-27**. 최신 접근 가능한 자료를 직접 확인해 초기 규칙을 선정했다. 모든 최신 신조어를 수집하거나 혐오 표현을 완전히 탐지했다는 뜻은 아니다.

## 사용한 원자료

- [LDNOOBW 기여자들의 한국어 원본 목록](https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/ko)
- [실제로 읽은 원문 파일](https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/ko)
- [원본 라이선스](https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/LICENSE): Creative Commons Attribution 4.0 International. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

저작자 표시: LDNOOBW / List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words contributors. 원자료에서 19개 한국어 표현만 선별하고 나머지를 제외한 변형 목록이다. 원자료 제공자가 이 프로젝트를 보증한다는 의미는 아니다. 목록은 보증 없이 제공된다. 출처·라이선스·변형 사실은 `seed/masking-rules.json`에도 기록했다.

## 선택과 제외 기준

직접적인 욕설·모욕 표현 중 2자 이상인 일부를 초기 규칙으로 선택했다. 원문의 성별·국적·장애 관련 표현과 성적·의학적·일상적 단어를 무조건 모두 가져오지 않았다. 짧은 단일 문자나 일반 문장에 자주 포함되는 표현은 제외했다. 세부 19개 항목은 JSON 파일에서 확인할 수 있다.

예를 들어 `새끼`, `보지`, `미친`, `씹`을 일반 부분 문자열 규칙으로 넣으면 동물의 새끼·“보지 못한 풍경”·“영향을 미친”·음식을 씹는 문장을 오탐할 수 있다. “개새끼”처럼 선택한 합성 표현만 적용하고, 정상 문장 예시는 자동 테스트에서 확인한다. 선택한 표현도 인용·교육·문학 맥락에서는 오탐할 수 있다.

키워드는 정규식 코드가 아닌 리터럴 문자로 검색한다. 영문 대소문자는 구분하지 않고 겹치는 구간을 병합한다. 관리자 화면에서 추가·삭제하며 DB에 저장한다. 규칙 변경은 다음 조회부터 기존 글에도 적용되고 서버 재시작으로 되돌아가지 않는다.

공백 삽입·자모 분해·변형 철자·문맥 기반 괴롭힘은 이 방식으로 모두 탐지할 수 없다. 관리자 피드백으로 필요한 규칙을 보완해야 한다. [BEEP! 연구](https://aclanthology.org/2020.socialnlp-1.4/)도 단순 용어 매칭의 오탐·미탐 한계를 설명한다. 연구 데이터셋 자체는 복제하거나 배포하지 않았다.

자료 조사와 규칙 가져오기는 개발·초기 설정 단계에서만 수행한다. 배포된 무료 PythonAnywhere 앱은 외부 인터넷 검색을 호출하지 않는다.
