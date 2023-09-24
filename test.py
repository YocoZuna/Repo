import os
dupa = []
dupa2 = []
iterator = -1

for i in range(0,128):
    dupa.append(i)
    dupa2.append(i)
for i in range (-33,-0):
    dupa2.insert(iterator+1,dupa[i])
print(dupa2)