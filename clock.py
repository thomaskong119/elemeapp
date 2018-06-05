import random

clocka = 1
clockb = 11
clockc = 0
steps = 100
log = ""
tempsteps = 0

def action(flag,a,b,c):
    if flag == 1:
        a += 1
        b -= 1
    if flag == 2:
        b += 1
        c -= 1
    if flag == 3:
        a -= 1
        c += 1
    if a == 13:
        a = 1
    if a == 0:
        a = 12
    if b == 13:
        b = 1
    if b == 0:
        b = 12
    if c == 13:
        c = 1
    if c == 0:
        c = 12
    return a,b,c

for times in range(1,13):
    if times-clocka < 0:
        if abs(times-clocka+12) > 6:
            res = action(1,clocka,clockb,clockc)
            clocka = res[0]
            clockb = res[1]
            clockc = res[2]


# for times in range(10000):
#     templog = ""
#     while True:
#         act = random.randint(1,3)
#         res = action(act,clocka,clockb,clockc)
#         clocka = res[0]
#         clockb = res[1]
#         clockc = res[2]
#         tempsteps += 1
#         diff = abs(clocka-clockb) + abs(clockb-clockc)
#         templog += str(act)
#         # print (diff)
#         if diff == 0:
#             break
#     if steps > tempsteps:
#         steps = tempsteps
#         log = templog

print (log)
print (steps)
