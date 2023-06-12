
# a)
class resturant():
    def __init__(self, resturant_name, cuisine_type):
        self.resturant_name = resturant_name
        self.cuisine_type = cuisine_type
        # b)
        self.number_served = 0

    def describe_resturant(self):
        print('resturant name is ' + self.resturant_name)
        print('our cuisine type is ' + self.cuisine_type)

    def open_resturant(self):
        print('我们正在营业中，欢迎光临！')

    # b)
    def set_number_served(self, num: int):
        self.number_served = num

    def increment_number_served(self, num: int):
        self.number_served += num


# c)
class IceCreamStand(resturant):
    def __init__(self, resturant_name, cuisine_type, flavors):
        super().__init__(resturant_name, cuisine_type)
        self.flavours = flavors

    def show(self):
        for ii in self.flavours:
            print(ii)


kfc = resturant('KFC', '开封菜')
print(kfc.number_served)
kfc.set_number_served(100)
print(kfc.number_served)
kfc.increment_number_served(2000)
print(kfc.number_served)

flavours = ['chocolate', 'milk', 'banana', 'blueberry', 'pineapple']
DairyQueen = IceCreamStand('DairyQueen', 'IceCream', flavours)
DairyQueen.describe_resturant()
DairyQueen.open_resturant()
DairyQueen.show()















