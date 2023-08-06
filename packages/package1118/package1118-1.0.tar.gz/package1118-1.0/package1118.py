s1,s2 = input().split()
s1 = int(s1)
s2 = int(s2)
ss1 = ''
for i in range(s1):
    ss1 = ss1 + str(s2) + ' '
print(ss1)
for i in range(s1-2):
    ss = str(s2) + ' '
    for j in range(s1-2):
        ss = ss + str(s2-1) + ' '
    ss = ss + str(s2) + ' '
    print(ss)
print(ss1)