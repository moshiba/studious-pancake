import itertools

groups = []
uniquekeys = []
with open("data.file", "r") as f:
    lines = f.readlines()
    for k, g in itertools.groupby(lines, (lambda x: x == "\n")):
        groups.append(list(g))
        uniquekeys.append(k)

ll = filter((lambda x: x[0] is False), zip(uniquekeys, groups))

ll = list(zip(*ll))[1]

print(f"got {len(ll)} groups")

for x in ll:
    l = x[0].strip('\n')
    print(f"\n---\n{l}\n---", end='')
    # for i in y:
    #    print(i, end='')
