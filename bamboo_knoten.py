import pandas as pd

data_knoten = pd.read_csv(r'E:\python\Project_02\bamboo_Knoten.csv')

data_knoten = data_knoten.values.tolist()

# bamboo_store = [[0, 130, 260, 370, 480, 590], [0, 110, 220, 320, 410, 500]]
#
# bamboo_len = [[[130, 260, 370, 480, 590], [130, 240, 350, 460], [110, 220, 330], [110, 220], [110]], \
#               [[110, 220, 320, 410, 500], [110, 210, 300, 390], [100, 190, 280], [90, 180], [90]]]
#
# # print('First bamboo knotes:', bamboo_store[0])
# # print('First bamboo lengths:', bamboo_len[0])
#
# des_values = [130, 220, 100, 190, 210, 390, 310, 131, 256, 222, 435, 491]

class bamboo:

    def __init__(self, id, len, kPos):
        self.id = id
        self.len = len
        self.kPos = kPos

    def info(self):
        return "id: {}\nLength: {}\nKnots: {}".format(self.id, self.len, self.kPos)

    def messure(self):
        for i in range(len(self.kPos)):
            temp = []
            for j in range(len(self.kPos)):
                if j < len(self.kPos) - 1 - i:
                    temp.append(abs(self.kPos[i] - self.kPos[j + 1 + i]))
            if temp:
                messure_dic["dist{}{}".format(self.id, i)] = distances(self.id, temp)


class distances:

    def __init__(self, id, dist):
        self.id = id
        self.dist = dist

    def messure_info(self):
        return self.id, self.dist   # To get the lengths list with the bamboo id


def find_by_index(id, sub_id, num):
    if num != "ALL":
        return messure_dic["dist{}{}".format(id, sub_id)].messure_info()[1][num]
    else:
        return messure_dic["dist{}{}".format(id, sub_id)].messure_info()[1]


class solutions:
    def __init__(self, id, sub_id, item):
        self.id = id
        self.sub_id = sub_id
        self.item = item


bamboo_dic = {}
messure_dic = {}
sol_dic = {}


# for i in range(2):
#     dic["bam{}".format(i)] = bamboo(i, 590, [0, 130, 260, 370, 480, 590])

def add_bamboos():
    # creating or recreating bamboo lengths from csv file bamboo_Knoten
    # for the bamboo class you need id, total length and the coordinations of the knots
    [bamboo(id, stab[-1], stab).messure() for id, stab in enumerate(data_knoten)]

    # bam01 = bamboo(0, 590, [0, 130, 260, 370, 480, 590])
    # bam02 = bamboo(1, 500, [0, 110, 220, 320, 410, 500])
    # bam01.messure()
    # bam02.messure()


def get_longest_list(lst):
    # pick the highest values in a list
    a = []
    [a.append(len(i)) for i in lst]
    d = max(a)
    return [lst[i] for i, j in enumerate(a) if j == d], d


# +/- 8 and defining the direction
# after cutting for example +8 this will be saved in the next loop

def p_m(lst, value, saved_dir_val):
    if not saved_dir_val:
        minR = -16
        maxR = 17
    elif 0 < saved_dir_val <= 8:
        minR = -16
        maxR = 9
    elif 8 < saved_dir_val <= 16:
        minR = -16
        maxR = 0
    elif -8 < saved_dir_val <= 0:
        minR = -8
        maxR = 17
    elif -16 < saved_dir_val <= -8:
        minR = 0
        maxR = 17

    for i in lst:
        for j in range(minR, maxR):
            if i + j == value:
                if i + j > i:
                    return i + j, j, i
                elif i + j < i:
                    return i + j, j, i
                elif i + j == i:
                    return i + j, j - 2, i
            else:
                pass


# print(messure_dic["dist10"].messure_info())

# print(dic["dist{}{}".format(0,1)].messure_info()[0])

# print(find_by_index(0,0,"ALL"))
# print(find_by_index(0,0,2))

# desired_bamboo = [370, 130, 240, 100, 190, 210, 390]

pos_desired_bamboo = pd.read_csv("pos_desired_bamboo.csv")

# desired values from project
des_values_comb = pos_desired_bamboo.values.tolist()

des_values = des_values_comb[0]
total_des = len(des_values)

repeat = True
first_ind = 0
temp_sol = []
match = 0
fail = 0
s = 0
temp_dir = []

bamboo_num = 2
bamboo_pos_len = 5

add_bamboos()

while first_ind < bamboo_num and repeat == True:
    second_ind = 0
    while second_ind < bamboo_pos_len:
        # ac speichert die Längen zwischen den Knoten
        ac = messure_dic["dist{}{}".format(first_ind, second_ind)].messure_info()
        item = 0
        while item < len(des_values):
            des_item = 0
            while des_item < len(ac[1]):
                res = p_m(ac[1], des_values[item], temp_dir)
                if res != None:
                    temp_dir = res[1]
                    val_ind = ac[1].index(res[2])
                    temp_sol.append((first_ind, second_ind, des_values[item]))
                    # print(temp_sol[-1])
                    des_values.pop(item)
                    match += 1
                    if val_ind > 0:
                        for xi in range(0, val_ind):
                            messure_dic["dist{}{}".format(first_ind, xi)].messure_info()[1].clear()
                    break
                des_item += 1
            item += 1
        second_ind += 1
    first_ind += 1
    if first_ind == bamboo_num:
        # print(s, temp_sol)
        sol_dic["sol_{}".format(s)] = temp_sol
        s += 1
        if match != total_des and s < len(des_values_comb):
            fail += 1
            # print("\nFailure")
            add_bamboos()
            first_ind = 0
            des_values = des_values_comb[s]
            match = 0
            temp_sol.clear()
        else:
            print("Finished.")


print("{}/{} desired lengths were found.".format(match, total_des))

clean_sol_dic = {}

for key, value in sol_dic.items():
    if value not in clean_sol_dic.values():
        clean_sol_dic[key] = value

print(get_longest_list(list(clean_sol_dic.values()))[0])
print(get_longest_list(list(clean_sol_dic.values()))[1])
