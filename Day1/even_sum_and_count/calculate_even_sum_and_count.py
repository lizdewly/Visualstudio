def calculate_even_sum_and_count(n):
    total = 0
    count = 0

    if n < 1:
        return {"Sum": 0, "Count": 0}

    for i in range(1, n + 1):
        if i % 2 == 0:
            total += i  # 짝수의 합
            count += 1  # 짝수의 개수

    return {"Sum": total, "Count": count}


if __name__ == "__main__":
    #n = int(input("정수 n을 입력하세요: "))
    #print(calculate_even_sum_and_count(n))
    assert calculate_even_sum_and_count(100) == {"Sum": 2250, "Count": 50}, 'Test 1 Failed'
    assert calculate_even_sum_and_count(1) == {"Sum": 0, "Count": 0}, 'Test 2 Failed'
    assert calculate_even_sum_and_count(-5) == {"Sum": 0, "Count": 0}, 'Test 3 Failed'
    print('모든 테스트 케이스가 성공했습니다.')     


