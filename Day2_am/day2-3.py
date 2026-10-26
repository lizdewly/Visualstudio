class SafeProfile: #제품사양서like
    def __init__(self):
        pass
    def get(self,key):
        return True
    def set(self,key):
        return True

user_profile = SafeProfile()
print(user_profile.get('is_verified'))
#.get 객체화

user_profile = SafeProfile()
user_profile2 = SafeProfile()
user_profile3 = SafeProfile()

if user_profile:
    print('성공')
else:
    print('실패')

user_profile = None
if user_profile and user_profile.get('is_verified'): #자식 (get) 호출 전에 부모 (user_profile) 존재 여부 확인
    print('성공')
else:
    print('실패')

