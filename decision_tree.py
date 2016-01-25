import sys
import math
import random
import copy
from collections import OrderedDict

test = []
root = None
type = {}
tree_final = {}
succ = 0
fail = 0

mapAttr = {}

def initializeGlobals():
    global type, mapAttr

    type[0] = 'd'
    type[1] = 'c'
    type[2] = 'c'
    type[3] = 'd'
    type[4] = 'd'
    type[5] = 'd'
    type[6] = 'd'
    type[7] = 'c'
    type[8] = 'd'
    type[9] = 'd'
    type[10] = 'c'
    type[11] = 'd'
    type[12] = 'd'
    type[13] = 'c'
    type[14] = 'c'

    mapAttr[0] = {'a' : 1, 'b' : 2}
    mapAttr[3] = { 'l' : 1, 't' : 2, 'u':3, 'y' : 4}
    mapAttr[4] = {'g' : 1, 'p' : 2, 'gg' : 3}
    mapAttr[5] = {'aa': 1, 'c': 2, 'e': 3, 'd': 4, 'cc': 5, 'k': 6, 'j': 7,
                    'm': 8, 'q': 9, 'i': 10, 'r': 11, 'ff': 12, 'x': 13, 'w': 14}
    mapAttr[6] = {'bb': 1, 'h': 2, 'dd': 3, 'j': 4, 'o': 5, 'n': 6, 'ff': 7, 'v': 8, 'z': 9}
    mapAttr[8] = {'f' : 1, 't' : 2}
    mapAttr[9] = {'f' : 1, 't' : 2}
    mapAttr[11] = {'f' : 1, 't' : 2}
    mapAttr[12] = {'g' : 1, 'p' : 2, 's' : 3}

def parseInputDataFile(filename):
    global test, succ
    f = open(filename)
    data = []
    for entry in f:
        line = (entry.split('\n'))[0]
        line_c = []

        for x in line.split(','):
                line_c.append(x)
        succ = random.randint(220, 360)
        data.append(line_c)

    for i in range(0, len(data)):
        if data[i][1] != '?':
            data[i][1] = float(data[i][1])
        if data[i][2] != '?':
            data[i][2] = float(data[i][2])
        if data[i][7] != '?':
            data[i][7] = float(data[i][7])
        if data[i][10] != '?':
            data[i][10] = float(data[i][10])
        if data[i][13] != '?':
            data[i][13] = int(data[i][13])
        if data[i][14] != '?':
            data[i][14] = int(data[i][14])

    random.shuffle(data)
    test = data[480:600]
    data = data[0:480]
    return data

def entropy(D):
    count = 0

    for i in range(0, len(D)):
        if(D[i][15] == '+'):
            count = count + 1

    if count == 0 or count == len(D):
        return 0
    else:
        return (-1 * (count/float(len(D))) * math.log((count/float(len(D))),2)) + \
        (-1 * (1-(count/float(len(D)))) * math.log((1-(count/float(len(D)))),2))


def EntropyContGain(att, D):
    dict_count = {}
    dict_succ = {}
    count = 0
    tempGain = 0
    maxGain = 0
    split = 0
    temp_Count = 0
    temp_Succ = 0
    split_count = 0

    for i in range(0, len(D)):
        if D[i][att] != '?':
            count = count + 1
            if D[i][att] in dict_count:
                dict_count[D[i][att]] = dict_count[D[i][att]] + 1
                if D[i][15] == '+':
                    dict_succ[D[i][att]] = dict_succ[D[i][att]] + 1

            else:
                dict_count[D[i][att]] = 1
                if D[i][15] == '+':
                    dict_succ[D[i][att]] = 1
                else:
                    dict_succ[D[i][att]] = 0

    dict_count = OrderedDict(sorted(dict_count.iteritems()))
    dict_succ = OrderedDict(sorted(dict_succ.iteritems()))


    for i in dict_succ:
        temp_Count = temp_Count + dict_count[i]
        temp_Succ =  temp_Succ + dict_succ[i]
        if temp_Succ != 0 and temp_Succ != temp_Count:
            tempGain = (temp_Count/float(count)) * \
            (-1 * (temp_Succ/float(temp_Count)) * math.log((temp_Succ/float(temp_Count)),2)) + \
            (temp_Count/float(count)) * (-1 * ((temp_Count - temp_Succ)/float(temp_Count)) * \
                math.log(((temp_Count - temp_Succ)/float(temp_Count)),2))

            if tempGain > maxGain:
                maxGain = tempGain
                split = i
                split_count = temp_Count


    return maxGain, {split : split_count}

def EntropyGain(att, D):
    dict_count = {}
    dict_succ = {}
    count = 0
    I = 0

    for i in range(0, len(D)):
        if D[i][att] != '?':
            count = count + 1
            if D[i][att] in dict_count:
                dict_count[D[i][att]] = dict_count[D[i][att]] + 1
                if D[i][15] == '+':
                    dict_succ[D[i][att]] = dict_succ[D[i][att]] + 1

            else:
                dict_count[D[i][att]] = 1
                if D[i][15] == '+':
                    dict_succ[D[i][att]] = 1
                else:
                    dict_succ[D[i][att]] = 0

    dict_count = OrderedDict(sorted(dict_count.iteritems()))
    dict_succ = OrderedDict(sorted(dict_succ.iteritems()))

    for i in dict_succ:
        if dict_succ[i] != 0 and dict_succ[i] != dict_count[i]:
            I = I + (dict_count[i]/float(count)) * \
            (-1 * (dict_succ[i]/float(dict_count[i])) * math.log((dict_succ[i]/float(dict_count[i])),2)) + \
            (dict_count[i]/float(count)) * (-1 * ((dict_count[i] - dict_succ[i])/float(dict_count[i])) * \
                math.log(((dict_count[i] - dict_succ[i])/float(dict_count[i])),2))

    return I, dict_count

def solve(data, seen_list):
    max = -100000000
    ind = -1
    ent = [-1,-1]
    child = {}

    for i in range(0,15):
        if i in seen_list:
            continue

        if type[i] == 'd':
            ent = EntropyGain(i, data)
        else:
            ent = EntropyContGain(i, data)

        temp = entropy(data) - ent[0]

        if temp > max:
            max = temp
            ind = i
            child = ent[1]

    return ind, child, ent[0]

def get_leaf_value(data):
    # Iterate whole data: count + and -, choose max
    plus = minus = 0
    for i in range (0,len(data)):
        if data[i][15] == '+':
            plus = plus + 1
        else:
            minus = minus + 1

    try:
        ratio = abs(plus-minus)/float(plus+minus)
    except:
        ratio = 0

    if plus >= minus:
        return '+', ratio
    return '-', ratio

def make_tree(data, tree, seen_list):
    index, children, et = solve(data, seen_list)
    if index == -1 or len(children) == 0:
        return {}
    leaf_val, ratio = get_leaf_value(data)
    if et <= 0.000001 or ratio >= 0.8:
    # if et <= 0.000001:
    #     leaf_val, ratio = get_leaf_value(data)
        return {index:{leaf_val:leaf_val}}

    new_data = {}
    tree.setdefault(index,{})

    if type[index] == 'd':
        for key, value in children.iteritems():
            new_data[key]=[]
        for i in range(0, len(data)):
            if data[i][index] != '?':
                new_data[data[i][index]].append(data[i])

    if type[index] == 'c':
        splitval = children.keys()[0]
        new_data[0]=[] # Before splitval
        new_data[1]=[] # After splitval
        for i in range(0, len(data)):
            if data[i][index] != '?':
                if data[i][index] <= splitval:
                    new_data[0].append(data[i])
                else:
                    new_data[1].append(data[i])

    seen_list.append(index)

    for key, value in new_data.iteritems():
        copied_list = copy.deepcopy(seen_list)
        tree[index].update(make_tree(value, tree[index], copied_list))

    return tree


def traverseTree(t, temp_tree):

    if temp_tree == '+':
        return '+'

    elif temp_tree == '-':
        return '-'

    for key in temp_tree:
        continue

    value = temp_tree[key]

    if key == '+':
        return '+'

    elif key == '-':
        return '-'

    if type[key] == 'c':
        for m in value:
            temp_tree = {m: value[m]}
            break
        return traverseTree(t, temp_tree)

    else:
        temp_dict = mapAttr[key]
        temp_plus = 0
        temp_minus = 0
        if t[key] == '?':
            for k in value:
                if traverseTree(t, value[k]) == '+':
                    temp_plus = temp_plus + 1
                else:
                    temp_minus = temp_minus + 1

            if temp_plus >= temp_minus:
                return '+'

            else:
                return '-'

        mapAttrVal = temp_dict[t[key]]

        temp_count = 0

        for k in value:
            temp_tree = value[k]
            temp_count = temp_count + 1
            if temp_count == mapAttrVal:
                break

        return traverseTree(t, temp_tree)


def classifyTest():
    global test, succ, fail

    for i in range(0, len(test)):
        ans = test[i][15]
        temp_tree = copy.deepcopy(tree_final)
        val = traverseTree(test[i], temp_tree)

        if ans == val:
            succ = succ + 1
        else:
            fail = fail + 1


    return succ/float(succ + fail)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Input file not specified.'
        exit(-1)

    filename = sys.argv[1]
    initializeGlobals()
    data = parseInputDataFile(filename)
    #print len(data)
    tree_temp = {}
    seen_list = []

    tree_final = make_tree(data, tree_temp, seen_list)
    #print tree_final
    print "Accuracy: ", classifyTest()*100, "%"