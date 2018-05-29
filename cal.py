import random

total = 1000
mcq1=45
mcq2=20
count=0
for times in range(total):
    score=0
    for q1 in range(mcq1):
        if random.randint(1,4) == 4:
            score+=1
    for q2 in range(mcq2):
        if random.randint(1,4) == 4:
            score+=2
    score+=random.randint(6,12)
    if score >=60:
        count +=1
print (count)
print (str(count/total*100)+"%")