i = 1
print(f"2 X {i} = {2 * i}")
i = 2
print(f"2 X {i} = {2 * i}")
i = 3
print(f"2 X {i} = {2 * i}")
i = 4
print(f"2 X {i} = {2 * i}")

#range 에서 끝은 4가 아니라 5로 해야 4까지 출력됨 (n-1)
for i in range(1,10): 
    print(f"2 X {i} = {2 * i}")

for dan in range(2,10): # 2~9단까지 출력
    print(f"{dan}단")
    for i in range(1,10):
        print(f"{dan} X {i} = {dan * i}")
    print("============") # 단과 단 사이에 줄바꿈


#2 X 1 = 2 3 X 1 = 3 4 X 1 = 4 5 X 1 = 5 6 X 1 = 6 7 X 1 = 7 8 X 1 = 8 9 X 1 = 9
#2 X 2 = 4 3 X 2 = 6 4 X 2 = 8 5 X 2 = 10 6 X 2 = 12 7 X 2 = 14 8 X 2 = 16 9 X 2 = 18
#2 X 3 = 6 3 X 3 = 9 4 X 3 = 12 5 X 3 = 15 6 X 3 = 18 7 X 3 = 21 8 X 3 = 24 9 X 3 = 27
for dan in range (2,9):
    for i in range (1,10):
        print(f"{dan} X {i} = {dan * i}", end='\t')
    print ("\n=============") # 단과 단 사이에 줄바꿈

for i in range (2,10):
    for dan in range (1,10):
        print(f"{i} X {dan} = {i * dan}", end='\t')
    print ("\n=============") # 단과 단 사이에 줄바꿈