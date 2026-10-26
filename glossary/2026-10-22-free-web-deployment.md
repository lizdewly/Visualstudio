# 웹사이트 무료 배포 서비스와 방법

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 배포 예제 | [방법 보기](#배포-예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |
| 참고 자료 | [출처 보기](#참고-자료) |

- 최초 기록일: 2026-10-22
- 수정일: 2026-10-22
- 분류: Python, Coding
- 핵심 용어: 배포, 호스팅, 정적 사이트, GitHub Pages, Netlify, Cloudflare Pages, Vercel, Render, FastAPI

## 질문

웹사이트 무료 배포를 지원하는 사이트와 배포 방법을 알려줘.

## 답변

배포는 다른 사람이 인터넷 주소로 접속할 수 있도록 웹사이트 파일이나 서버 프로그램을 호스팅 서비스에 올리고 실행하는 과정이다.

HTML·CSS·JavaScript 파일을 제공하는 정적 사이트와 Python/FastAPI 같은 서버 프로그램을 실행하는 사이트를 구분해서 서비스를 선택한다. 브라우저 JavaScript로 계산하거나 화면을 바꾸는 사이트도 서버 코드가 필요 없다면 정적으로 배포할 수 있다.

2026-10-22 공식 자료 확인 기준:

| 서비스 | 적합한 용도 | 무료 조건과 제한 |
| --- | --- | --- |
| GitHub Pages | 개인 소개, 포트폴리오, 학습 문서 | GitHub Free에서는 공개 저장소 사용. Python 서버를 실행하지 않음. 온라인 사업·전자상거래·상용 SaaS 운영 목적 제한 |
| Netlify | HTML 사이트, 프런트엔드 | 폴더 드래그 앤 드롭 가능. 신규 무료 플랜은 월 300크레딧으로 배포·트래픽 등의 사용량을 관리 |
| Cloudflare Pages | 정적 사이트, 프런트엔드 | 정적 파일 요청은 무료·무제한. 빌드와 파일 수 등 별도 제한이 있으며 서버 함수는 별도 사용량 기준 적용 |
| Vercel | React·Next.js 개인 프로젝트 | Hobby는 개인·비상업 용도. 사용량 제한 있음 |
| Render | Python·FastAPI 웹 서버 | Free 인스턴스 선택 가능. 15분간 수신 트래픽이 없으면 절전, 다시 접속하면 기동에 약 1분 소요. 월 사용량 제한 있음 |

추천: HTML 파일을 처음 공개할 때는 Netlify 수동 업로드, GitHub와 함께 학습할 때는 GitHub Pages, 정적 사이트 운영은 Cloudflare Pages, FastAPI 서버 실습은 Render를 고려한다.

## 배포 예제

### HTML 사이트: Netlify

1. 공개할 파일만 담은 폴더를 만들고 최상위에 `index.html`을 둔다. CSS, JavaScript, 이미지도 함께 넣는다.
2. Netlify 가입 후 Projects에서 Add new project → Deploy manually를 선택한다.
3. 폴더를 업로드한다.
4. 발급된 `프로젝트명.netlify.app` 주소에서 확인한다.
5. 파일을 수정하면 새 버전을 업로드한다. GitHub를 연결하면 push 후 자동 배포하는 방식도 가능하다.

React 등 빌드가 필요한 프로젝트는 빌드 결과 폴더를 올리는 방식과 저장소를 연결해 서비스가 빌드하는 방식을 구분한다.

### HTML 사이트: GitHub Pages

1. GitHub에 공개 저장소를 만들고 `index.html`과 관련 파일을 업로드한다.
2. 저장소 Settings → Pages로 이동한다.
3. Source에서 Deploy from a branch를 선택한다.
4. `main` 브랜치와 `/(root)`를 선택하고 저장한다. 파일이 다른 브랜치나 docs 폴더에 있다면 실제 위치에 맞춘다.
5. 배포 완료 후 Pages에 표시되는 주소로 접속한다. 일반적인 프로젝트 주소는 `https://계정명.github.io/저장소명/` 형태다.

### HTML 사이트: Cloudflare Pages

Cloudflare 대시보드 Workers & Pages → Create application → Get started → Drag and drop your files에서 프로젝트 이름을 입력하고 파일 폴더를 올린 뒤 Deploy site를 선택한다. 주소는 `프로젝트명.pages.dev` 형태다. 빌드가 필요한 프로젝트는 빌드 결과물을 올린다.

### FastAPI: Render

아래는 프로젝트 루트에 `main.py`가 있고 그 안에 `app = FastAPI()`가 있는 최소 프로젝트를 가정한 설정이다. 실제 배포를 실행한 결과가 아닌 절차 예시다.

1. GitHub 저장소에 앱 파일과 `requirements.txt`를 올린다. 최소 의존성 예시는 다음과 같다. 실제 프로젝트에서 사용하는 다른 패키지도 필요하다.

```text
fastapi
uvicorn
```

2. Render에서 New → Web Service를 선택하고 저장소를 연결한다.
3. Python 환경과 Free 인스턴스를 선택한다.
4. Build Command에 다음을 입력한다.

```sh
pip install -r requirements.txt
```

5. Start Command에 다음을 입력한다.

```sh
uvicorn main:app --host 0.0.0.0 --port $PORT
```

6. 배포 후 제공되는 `프로젝트명.onrender.com` 주소를 확인한다. FastAPI 기본 문서 기능이 켜져 있다면 `/docs`에서도 확인할 수 있다.

`main:app`은 main.py의 app 객체를 뜻한다. 파일 이름이나 배포 기준 폴더가 다르면 수정해야 한다. `$PORT`는 Render 서버 환경의 포트 변수이므로 위 명령은 Render 설정란에 입력한다.

## 헷갈리기 쉬운 점

- GitHub에 코드를 push한 것과 웹사이트를 배포한 것은 다르다. Pages 설정이나 호스팅 연결이 필요하다.
- 정적 호스팅에 Python 파일을 올리는 것만으로 FastAPI 서버가 실행되지는 않는다.
- 정적 사이트도 브라우저 JavaScript로 상호작용하거나 외부 API를 호출할 수 있다.
- 기본 제공 주소로 공개하면 도메인을 별도로 살 필요가 없다. 직접 소유하는 도메인은 보통 별도 구매·갱신 비용이 든다.
- 무료 호스팅이어도 외부 AI API나 데이터베이스 등의 비용까지 무료인 것은 아니다.
- Render 무료 서버의 로컬 파일은 재시작·재배포·절전 시 유실될 수 있다. SQLite나 업로드 파일의 영구 보관용으로 사용하지 않는다.
- API 키와 비밀번호는 공개 저장소나 브라우저 JavaScript에 넣지 않고 서버 환경 변수 등으로 관리한다.
- 무료 플랜의 사용량과 정책은 변경될 수 있다.

## 참고 자료

- [GitHub Pages 배포 소스 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub Pages 제한](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [Netlify 수동 배포](https://docs.netlify.com/manage/projects/add-new-project/)
- [Netlify 크레딧 기반 플랜](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/)
- [Cloudflare Pages 직접 업로드](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Cloudflare Pages 함수 및 정적 요청 요금](https://developers.cloudflare.com/pages/functions/pricing/)
- [Vercel 이용 약관: Hobby 용도 제한](https://vercel.com/legal/terms)
- [Render 무료 서비스 제한](https://render.com/docs/free)
- [Render FastAPI 배포](https://render.com/docs/deploy-fastapi)
