from rsgz.the_list.rsgz_list import quchong_list

the_list = "".split(",")
the_list = [i.lower() for i in the_list]
print(len(the_list))
the_list = quchong_list(the_list)

# print(list(map(lambda x:print(x), the_list)))
for i in the_list:
    print(i)