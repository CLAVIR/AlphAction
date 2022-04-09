import os

names = [
    'massa',
    'peixe',
    'rissois',
    'rita',
    'robalo',
    'sal'
]

for key0 in names:
    lines = []
    for key1 in names:
        if key0 != key1:
            with open(key1 + '_train.csv', 'r') as f:
                raw = f.read()
                temp = raw.split("\n")
                while "" in temp:
                    temp.remove("")
                lines += temp
    with open('lfv_' + key0 + '.csv', 'w') as f:
        f.write('\n'.join(lines))
