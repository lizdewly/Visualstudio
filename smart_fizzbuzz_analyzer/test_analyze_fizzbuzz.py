from analyze_fizzbuzz import analyze_fizzbuzz


def run_validation():
    # 1단계: 직접 계산한 예상값으로 경계값과 각 분류를 검증한다.
    # 튜플 순서: FizzBuzz, Fizz, Buzz, Number
    cases = [
        (-100, (0, 0, 0, 0)),
        (-1, (0, 0, 0, 0)),
        (0, (0, 0, 0, 0)),
        (1, (0, 0, 0, 1)),
        (2, (0, 0, 0, 2)),
        (3, (0, 1, 0, 2)),
        (5, (0, 1, 1, 3)),
        (14, (0, 4, 2, 8)),
        (15, (1, 4, 2, 8)),
        (16, (1, 4, 2, 9)),
        (30, (2, 8, 4, 16)),
        (100, (6, 27, 14, 53)),
        (1000, (66, 267, 134, 533)),
    ]
    keys = ("FizzBuzz", "Fizz", "Buzz", "Number")

    for limit, values in cases:
        expected = dict(zip(keys, values))
        actual = analyze_fizzbuzz(limit)
        assert actual == expected, (
            f"limit={limit}: 예상={expected}, 실제={actual}"
        )
    print(f"1단계 통과: 대표 입력 {len(cases)}개")

    # 2단계: 반환 형식, 음수 카운트, 누락 또는 중복 집계를 검사한다.
    for limit in range(-10, 301):
        actual = analyze_fizzbuzz(limit)
        assert type(actual) is dict, f"limit={limit}: 반환값이 dict가 아닙니다."
        assert set(actual) == set(keys), f"limit={limit}: 반환 키가 다릅니다."
        for key in keys:
            assert type(actual[key]) is int, f"limit={limit}, {key}: 정수가 아닙니다."
            assert actual[key] >= 0, f"limit={limit}, {key}: 음수 카운트입니다."
        assert sum(actual.values()) == max(limit, 0), (
            f"limit={limit}: 전체 카운트의 합이 맞지 않습니다. 실제={actual}"
        )
    print("2단계 통과: -10~300의 반환 형식과 전체 카운트")

    # 3단계: 함수의 반복문과 다른 방법인 배수 개수 공식으로 교차 검증한다.
    # 3 또는 5의 배수 개수에서 공배수를 빼야 Fizz/Buzz 중복을 피할 수 있다.
    for limit in list(range(1, 301)) + [999, 1000, 10000]:
        common = limit // 15
        expected = {
            "FizzBuzz": common,
            "Fizz": limit // 3 - common,
            "Buzz": limit // 5 - common,
            "Number": limit - limit // 3 - limit // 5 + common,
        }
        actual = analyze_fizzbuzz(limit)
        assert actual == expected, (
            f"limit={limit}: 공식 예상={expected}, 실제={actual}"
        )
    print("3단계 통과: 공식으로 303개 입력 교차 검증")

    # 4단계: 반복 호출하거나 반환값을 수정해도 다음 호출에 영향이 없어야 한다.
    for limit in [0, 15]:
        first = analyze_fizzbuzz(limit)
        second = analyze_fizzbuzz(limit)
        assert first == second, f"limit={limit}: 반복 호출 결과가 다릅니다."
        assert first is not second, f"limit={limit}: 같은 딕셔너리를 재사용합니다."
        first["FizzBuzz"] = -1
        assert analyze_fizzbuzz(limit) == second, (
            f"limit={limit}: 이전 반환값 변경이 다음 호출에 영향을 줍니다."
        )
    print("4단계 통과: 반복 호출과 반환값 독립성")
    print("Mission 1: 모든 검증을 통과했습니다.")


if __name__ == "__main__":
    run_validation()
