def deletebond(c1, c2):
    Edit = False
    btitle = False
    with open("data.file", "r") as f:
        lines = f.readlines()
    f.close()

    with open("data.file", "w") as f:
        for line in lines:
            if line.strip("\n") == c1:
                break
            f.write(line)
    f.close()

    with open("data.file", "a") as f:
        for line in lines:
            if line.strip("\n") == c1:
                Edit = True
            word = line.split(" ")[0]
            if ((word != c2) & Edit):
                f.write(line)  #bond removed
            elif ((word == c2) & Edit):
                btitle = True
                out = line

    f.close()

    if btitle == True:
        with open("data.file", "r") as f:
            line = f.readlines()
        f.close()

        with open("data.file", "w") as f:
            for i in range(len(line)):
                if i == 4:
                    nbonds = str(int(line[i].split(" ")[0]) - 1) + ' bonds\n'
                    f.write(nbonds)  #bond headline -1
                else:
                    f.write(line[i])
        f.close()
        return out

    if btitle == False:
        echo = "PASS"
        return echo


#print(deletebond("Bonds","10"))


def resumebond(temdeleted):

    if temdeleted == "PASS":
        pass

    else:
        with open("data.file", "a") as f:  #resume
            f.write(temdeleted)
        f.close()

        with open("data.file", "r") as f:
            line = f.readlines()
        f.close()

        with open("data.file", "w") as f:
            for i in range(len(line)):
                if i == 4:
                    nbonds = str(int(line[i].split(" ")[0]) + 1) + ' bonds\n'
                    f.write(nbonds)  #bond headline +1
                else:
                    f.write(line[i])
        f.close()
