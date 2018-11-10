path_list = ['year_2018/month_9/date_10/sierratradingpost.py',
             'year_2018/month_9/date_11/a1865_nevisport.py',
             'year_2018/month_9/date_11/a1866_quarkshoes.py',
             'year_2018/month_9/date_13/a1906_framesfootwear.py',
             'year_2018/month_9/date_13/test.py',
             'year_2018/month_9/date_13/test2.py',
             'year_2018/month_9/date_9/costly_style.py']

temp_list = []


def _foo(path, node):
    if '/' not in path:
        node.append(path)
        return

    root, other = path.split('/', 1)

    for item in node:
        for i in item.keys():
            if root != i:
                x = {root: []}
                node.append(x)
                _foo(other, x[root])

    if not node:
        x = {root: []}
        node.append(x)
        _foo(other, x[root])

    # _foo(other, root)


# for path in path_list:
#     _foo(path, temp_list)
# print(temp_list)

x = []

"""
for path in path_list:
    f1, o1 = path.split('/', 1)

    if not x:
        x1 = {f1: []}
        x.append(x1)

        f2, o2 = o1.split('/', 1)

    else:
        for xx in x:
            for item in xx.keys():
                if f1 != item:
                    x1 = {f1: []}
                    x.append(x1)

        if not x1[f1]:
            x2 = {f2: []}
            x1[f1].append(x2)

            f3, o3 = o2.split('/', 1)

        else:
            for xx in x1[f1]:
                for item in xx.keys():
                    if f1 != item:
                        x2 = {f2: []}
                        x1[f1].append(x2)

            if not x2[f2]:
                x3 = {f3: []}
                x2[f2].append(x3)

                if '/' not in o3:
                    x3[f3].append(o3)
"""


def foo(path_list):
    for i in range(len(path_list)):
        f1, o1 = path_list.pop().split('/', 1)

        if not x:
            x1 = {f1: []}
            x1[f1].append(o1)
            x.append(x1)
        else:
            for item in path_list:
                if f1 not in item.keys():
                    x1 = {f1: []}
                    x1[f1].append(o1)
                    path_list.append(x1)
                else:
                    path_list[f1].append(o1)


foo(path_list)
foo(x[0]['year_2018'])
print(x)
