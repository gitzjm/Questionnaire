list=[]
dict={"a":None}
for i in range(3):
    dict["a"]=i
    list.append(dict)
print(list)