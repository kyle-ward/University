def show_magician(manelist: list):
    for ii in manelist:
        print(ii)

def make_great(namelist: list):
    for ii in range(len(namelist)):
        namelist[ii] = 'the Great ' + namelist[ii]

def make_great_2(namelist: list):
    lst = []
    for ii in namelist:
        lst.append('the Great ' + ii)
    return lst


# a)
lst = ['magician_A', 'magician_B', 'magician_C', 'magician_D', 'magician_E', 'magician_F', 'magician_G']
show_magician(lst)

# b)
#make_great(lst)
#show_magician(lst)

# c)
show_magician(make_great_2(lst))
show_magician(lst)