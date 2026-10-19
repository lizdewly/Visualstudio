# 이중 밑줄의 사용

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 위치에 따른 의미 | [답변 보기](#답변) |
| 클래스와 직접 실행 예제 | [예제 보기](#예제) |
| 밑줄 관례와 주의점 | [주의점 보기](#헷갈리기-쉬운-점) |
| DigitalWallet의 __balance | [후속 질문 보기](#후속-질문과-답변) |

- 최초 기록일: 2026-10-16
- 수정일: 2026-10-16
- 분류: Python, Coding
- 핵심 용어: __, dunder, 특수 메서드, 이름 맹글링, __name__

## 질문

"__" (double underbar)의 사용

## 답변

**이중 밑줄은 이름의 어디에 붙는지에 따라 의미가 다릅니다.** `__` 자체가 특별한 연산자인 것은 아닙니다. 밑줄의 영어 명칭은 underscore이고, 양쪽에 이중 밑줄이 있는 이름은 흔히 dunder 이름이라고 부릅니다.

| 형태 | 의미 | 예 |
| --- | --- | --- |
| `__이름__` | 파이썬이 정한 특별한 메서드나 속성 등의 이름 | `__init__`, `__str__`, `__name__` |
| 클래스 안의 `__이름` | 이름 충돌을 줄이기 위한 이름 맹글링 | `self.__score` |
| `__`만 사용 | 문법상 일반 식별자 | `__ = 10`도 가능하나 의미 있는 이름 권장 |

## 예제

### 양쪽 이중 밑줄과 앞쪽 이중 밑줄

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.__score = 90

    def __str__(self):
        return f"학생: {self.name}"

    def get_score(self):
        return self.__score

student = Student("민수")
print(student)
print(student.get_score())
```

실제 실행 결과:

```text
학생: 민수
90
```

- `__init__`은 일반적인 인스턴스 생성 과정에서 호출되어 초기 상태를 설정합니다. 객체 자체를 만드는 역할은 `__new__`가 담당합니다.
- `__str__`은 `str(student)`나 위의 `print(student)`에서 사용할 문자열을 정의합니다.
- `__score`는 클래스 코드 안에서 `_Student__score`라는 형태로 이름이 변환됩니다. 이를 이름 맹글링(name mangling)이라고 합니다. 주로 상속 관계에서 이름이 충돌하는 것을 줄입니다.

따라서 `student.__score`로 바로 접근하면 이 예제에서는 `AttributeError`가 발생합니다. 하지만 `student._Student__score`로는 접근할 수 있고, 실제 실행하면 `90`이 나옵니다. **완전한 비공개나 보안 장치는 아닙니다.**

### 직접 실행할 때만 코드 실행

```python
def main():
    print("프로그램 시작")

if __name__ == "__main__":
    main()
```

일반적인 파이썬 파일을 직접 실행하면 모듈 변수 `__name__`의 값이 `"__main__"`이 되어 `main()`을 호출합니다. 다른 파일에서 모듈로 import하면 보통 `__name__`에 모듈 이름이 들어가므로 이 조건 안의 코드는 실행되지 않습니다. import 시 파일의 다른 최상위 코드까지 모두 건너뛰는 것은 아닙니다.

## 헷갈리기 쉬운 점

- `__init__`과 `__score`는 다른 규칙입니다. 끝에도 이중 밑줄이 있는 특수 이름에는 위의 이름 맹글링이 적용되지 않습니다.
- 클래스 안에서 밑줄 두 개 이상으로 시작하고 밑줄 두 개 이상으로 끝나지 않는 이름이 맹글링 대상입니다. 예를 들어 `__score_`도 대상입니다.
- `_name`처럼 앞에 밑줄 하나만 있으면 보통 내부 용도라는 관례입니다. 직접 접근을 막거나 이름을 바꾸지는 않습니다.
- `__name__`은 변수이며 함수나 메서드가 아닙니다. 이중 밑줄 이름이 모두 메서드인 것은 아닙니다.
- 파이썬이 정한 `__len__`, `__str__` 등을 구현할 수 있지만, 특별한 의미가 없는 새 `__myname__` 이름을 임의로 만드는 것은 피합니다.
- `len(obj)`처럼 특수 동작을 호출하는 일반 문법을 사용합니다. `__len__` 같은 메서드를 직접 호출할 필요는 보통 없습니다.

관련 학습: [객체와 클래스](2026-10-15-python-object.md), [매개변수와 인자](2026-10-16-python-parameter-argument.md)

## 후속 질문과 답변

### 2026년 10월 16일 DigitalWallet의 내부 잔액

질문: 다음 코드에서 `self.__balance = 0`의 이중 밑줄 역할은 무엇인가요?

```python
class DigitalWallet:
    def __init__(self, owner: str, initial_balance: int = 0):
        self.owner = owner
        self.__balance = 0
        self.balance = initial_balance
```

`self`는 현재 지갑 객체를 가리킵니다. `self.__balance = 0`은 그 객체의 내부 잔액 속성을 0으로 초기화합니다. 앞의 이중 밑줄 때문에 클래스 안의 `__balance` 이름이 `_DigitalWallet__balance`로 변환됩니다. 목적은 상속 시 이름 충돌과 외부에서의 우발적인 접근을 줄이는 것입니다. 암호화하거나 접근을 완전히 막지는 않습니다.

**`self.__balance`와 `self.balance`는 자동으로 연결되지 않습니다.** 제시된 코드만 있다면 서로 다른 두 속성입니다. 예를 들어 `DigitalWallet("민수", 1000)`에서는 내부의 `__balance`는 0이고 공개 속성 `balance`는 1000입니다.

다만 클래스의 나머지 부분에 `@property`와 `@balance.setter`가 있으면 `self.balance = initial_balance`가 setter를 호출할 수 있습니다. 다음은 검증 후 내부 잔액을 바꾸도록 직접 연결한 예제입니다.

```python
class DigitalWallet:
    def __init__(self, owner: str, initial_balance: int = 0):
        self.owner = owner
        self.__balance = 0
        self.balance = initial_balance  # 아래 setter 호출

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("잔액은 음수일 수 없습니다")
        self.__balance = value

wallet = DigitalWallet("민수", 1000)
print(wallet.balance)  # 예상 결과: 1000
```

이 구조에서 `__balance`는 실제 값을 저장하는 내부 속성이고, `balance`는 읽기와 변경을 처리하는 공개 프로퍼티입니다. 음수 검증은 setter의 코드가 수행하며 이중 밑줄이 자동으로 해주는 것이 아닙니다. 타입 힌트인 `: int`도 실행 중 타입을 자동으로 강제하지 않습니다.
