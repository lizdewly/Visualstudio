#논리연산자
isSucess = True
isPass = False

if isSucess and isPass:
    print('A')
else:
    print('B')

if isSucess or isPass: # 더하기 (0을 제외한 모든 숫자는 True로 간주)
    print('C')
else:
    print('D')

#단력평가 Short-circuit
#isSuccess = False
#isPass = True

#if isSuccess and isPass and isSucess: # 첫번째 조건이 False이므로 뒤에 조건은 확인하지 않고 바로 False로 판단 i.e) 0
#    print('성공')

def extensive_check():
    print("시간이 오래 걸리는 함수 실행")
    return True 
is_active = False
if is_active and extensive_check(): # 첫번째 조건이 False이므로 뒤에 조건은 확인하지 않고 바로 False로 판단 i.e) 0
    print('통과')
else:
    print('차단 (extensive_check 실행 안됨)')

def extensive_check():
    print("시간이 오래 걸리는 함수 실행")
    return True 
is_active = False
if is_active or extensive_check(): # 첫번째 조건이 False이므로 뒤에 조건은 확인하지 않고 바로 False로 판단 i.e) 0
    print('통과')
else:
    print('차단 (extensive_check 실행 안됨)')

# None 값을 방어
user_profile = None
if user_profile is not None and user_profile.get('is_verified'):
    print('인증된 사용자')
else: 
    print('비인증된 사용자')