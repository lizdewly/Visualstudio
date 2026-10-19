# Git 저장소를 다른 로컬 드라이브에 내려받기

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |
| 폴더 URL로 clone할 때 오류 | [후속 질문 보기](#후속-질문과-답변) |
| 기존 폴더와 Day_4를 함께 유지하기 | [안내 정정](#안내-정정과-복구) |

- 최초 기록일: 2026-10-19
- 수정일: 2026-10-19
- 분류: Coding
- 핵심 용어: Git, 저장소, clone, 로컬 경로, pull

## 질문

Git에 올라간 파일을 다른 로컬 드라이브의 파일/폴더 안에 내려받으려면 어떻게 하나요?

## 답변

GitHub 같은 원격 저장소의 프로젝트 전체를 다른 드라이브에 받으려면 `git clone 저장소주소 "대상폴더경로"`를 사용합니다. 대상은 파일이 아니라 폴더입니다. 작업 중인 터미널이 C 드라이브에 있어도 D 드라이브 경로를 지정할 수 있습니다.

저장소 주소를 복사한 뒤 PowerShell 또는 VS Code 터미널에서 실행합니다. 대상 폴더는 아직 없거나 비어 있어야 합니다. 기존 파일이 있는 폴더 안에 받으려면 새로운 하위 폴더를 대상으로 지정합니다. 비공개 저장소는 접근 권한과 인증이 필요합니다.

## 예제

다음은 실행하지 않은 설명용 예시입니다. 저장소 주소와 드라이브 및 폴더 이름은 실제 값으로 바꿉니다.

```powershell
git clone https://github.com/사용자명/저장소명.git "D:\공부\python-project"
```

이 명령은 `D:\공부\python-project`에 저장소 파일과 Git 이력을 받습니다. 이후 이 복사본에서 원격 변경 내용을 가져와 현재 브랜치에 반영하려면 다음과 같이 실행합니다.

```powershell
cd "D:\공부\python-project"
git pull
```

`git pull`은 일반적인 clone 직후의 추적 브랜치 설정을 전제로 합니다. 로컬 수정 사항이 있으면 충돌하거나 실행이 중단될 수 있습니다.

## 헷갈리기 쉬운 점

- Git은 버전 관리 도구이고, GitHub는 저장소를 올려 두는 서비스 중 하나입니다.
- `clone`은 처음 복사본을 만들 때, `pull`은 이미 받은 저장소에서 원격 변경을 반영할 때 사용합니다.
- 파일만 필요하면 GitHub에서 ZIP을 받아 원하는 폴더에 압축을 풀 수도 있습니다. ZIP에는 Git 이력이 없어 그대로 `git pull`할 수 없습니다.
- 특정 파일 하나만 필요하면 해당 파일의 원본을 다운로드해 원하는 폴더에 저장할 수 있습니다. `git clone`은 기본적으로 저장소 전체를 대상으로 합니다.
- 원격 저장소에 올라가지 않은 파일은 내려받을 수 없습니다. `.gitignore`에 의해 제외되어 업로드하지 않은 파일도 포함되지 않습니다. 이미 추적 중인 파일은 `.gitignore`에 추가하는 것만으로 추적이 해제되지 않습니다.

## 후속 질문과 답변

### 2026-10-19: 폴더 URL로 clone하면 repository not found가 발생해요

질문: `https://github.com/lizdewly/ai_orc_4/tree/26e9cac76cd2d7732947cb20d0d2c6d9c1f05797/Day_4`를 `git clone`에 넣었더니 `repository not found` 오류가 발생했습니다.

답변: `/tree/커밋번호/Day_4`는 특정 시점의 폴더를 보여 주는 GitHub 웹페이지 경로입니다. `git clone`에는 저장소 주소인 `https://github.com/lizdewly/ai_orc_4.git`을 넣습니다. 로컬 대상 폴더 이름을 `Day_4`로 정해도 원격의 해당 폴더만 선택되는 것은 아닙니다.

다음은 실행하지 않은 안내용 명령입니다. 두 방법 중 하나를 선택하며, clone 대상 폴더는 없거나 비어 있어야 합니다.

전체 저장소를 받는 방법:

```powershell
git clone https://github.com/lizdewly/ai_orc_4.git "C:\Users\김세원\김세원2\AI4_git_trial"
```

기본 브랜치에 `Day_4`가 있다면 `AI4_git_trial\Day_4`에서 확인할 수 있습니다.

작업 폴더에 `Day_4`를 선택해서 펼치는 방법:

**안내 정정:** 아래 sparse-checkout 방법은 기존 Day_1 등의 폴더를 유지하면서 Day_4를 추가하려는 사용자 목적에 맞지 않았습니다. 선택하지 않은 추적 파일은 작업 폴더에서 제외됩니다. 전체 복사본을 유지하려면 sparse-checkout을 사용하지 않고 기존 저장소에서 pull로 업데이트합니다.

```powershell
git clone --filter=blob:none --sparse https://github.com/lizdewly/ai_orc_4.git "C:\Users\김세원\김세원2\AI4_git_trial"
cd "C:\Users\김세원\김세원2\AI4_git_trial"
git sparse-checkout set Day_4
```

이 방식도 Git 저장소를 만들며, 기본 cone 모드에서는 저장소 최상위 파일도 표시됩니다. `--filter=blob:none`은 파일 내용을 필요할 때 받도록 합니다.

위 명령은 기본 브랜치의 최신 상태를 받습니다. URL에 있던 커밋 시점이 꼭 필요하다면 복제한 저장소 안에서 `git switch --detach 26e9cac76cd2d7732947cb20d0d2c6d9c1f05797`로 이동할 수 있습니다. 해당 커밋이 복제된 저장소에서 접근 가능해야 하며, 이 상태는 브랜치에서 벗어난 과거 버전 확인 상태입니다. 이번 답변에서는 원격 커밋의 존재 여부를 확인하거나 clone을 실행하지 않았습니다.

### 2026-10-19: 대상 폴더가 이미 있고 비어 있지 않다는 오류

질문: `fatal: destination path 'C:\Users\김세원\김세원2\AI4_git_trial' already exists and is not an empty directory.`가 표시됩니다.

답변: clone은 비어 있지 않은 기존 폴더에 저장소를 덮어쓰지 않습니다. 실제로 대상 폴더를 읽기 전용으로 확인한 결과, 이미 `.git`이 있고 원격 주소도 `https://github.com/lizdewly/ai_orc_4.git`으로 설정된 저장소였습니다. `main` 브랜치에 로컬 변경이 없었으며 sparse-checkout에는 `Day_4`가 선택되어 있었습니다. 따라서 clone을 반복할 필요가 없습니다.

다만 확인 당시 이 복사본의 최신 커밋은 `7178026 first commit`이었고 그 커밋에는 `Day_4` 아래 파일이 없었습니다. 실제 `Day_4` 폴더도 비어 있었습니다. 로컬의 `origin/main` 표시는 마지막으로 받아 둔 정보이므로 현재 GitHub와 같다는 보장은 아닙니다.

기존 복사본에서 최신 커밋을 받으려면 다음을 실행합니다. 아래 명령은 안내용이며 이번 진단에서는 실행하지 않았습니다.

```powershell
cd "C:\Users\김세원\김세원2\AI4_git_trial"
git pull --ff-only
```

`--ff-only`는 이력이 갈라진 경우 자동 병합하지 않고 중단합니다. GitHub의 해당 브랜치에 `Day_4/test.py`가 커밋되어 올라와 있다면 업데이트 후 파일을 받을 수 있습니다. 기존 폴더를 삭제할 필요는 없습니다.

## 안내 정정과 복구

### 2026-10-19: 기존 폴더에 Day_4만 추가하고 싶었어요

질문: 안내대로 했더니 AI4_git_trial에서 Day_1 등의 폴더가 사라지고 Day_4만 남았습니다. 원한 것은 기존 폴더를 유지하면서 GitHub에 추가한 Day_4를 받아 전체 폴더 버전을 업데이트하는 것이었습니다.

답변: 앞선 sparse-checkout 안내가 사용자 목적에 맞지 않았습니다. `git sparse-checkout set Day_4`는 선택 경로를 Day_4로 제한하므로 다른 추적 파일을 작업 폴더에서 제외합니다. Git 커밋에서 삭제하는 것은 아닙니다. pull만 실행해도 이 제한은 유지됩니다.

복구 전 확인 결과 현재 커밋에는 Day_1, Day_2_am, Day_2_pm, Day_3, Day_4 등 기존 폴더가 모두 남아 있었고 로컬 변경 사항은 없었습니다. 작업 공간 밖 경로 변경 승인을 받아 다음 명령을 실제 실행했으며 성공했습니다.

```powershell
git -C "C:\Users\김세원\김세원2\AI4_git_trial" sparse-checkout disable
```

이 명령은 경로 선택 제한을 해제하고 현재 커밋의 전체 파일을 작업 폴더에 복원합니다. 이후 이 복사본을 GitHub의 브랜치 상태로 업데이트할 때는 해당 폴더에서 `git pull --ff-only`를 사용합니다. pull은 Day_4만 선택하여 추가하는 명령이 아니라 해당 브랜치의 변경 사항 전체를 반영합니다. 원격 변경이 Day_4 추가뿐이면 그 추가분이 반영됩니다.

## 참고 자료

- [Git 공식 문서: git clone](https://git-scm.com/docs/git-clone)
- [Git 공식 문서: git sparse-checkout](https://git-scm.com/docs/git-sparse-checkout)
