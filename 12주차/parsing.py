import json
import sys

with open ("S2-O1301M02959.json","r", encoding="UTF8") as f:
    data = json.load(f)

res = data["image"]["resolution"]
res_x = int(res[0])
res_y = int(res[1])

def boundingbox_normalization(bb, nb):
    nb_x = round(int(bb[0])/res_x, 4)
    nb_y = round(int(bb[1])/res_y, 4)
    nb_w = round(int(bb[2])/res_x, 4)
    nb_h = round(int(bb[3])/res_y, 4)
    nb.append([nb_x, nb_y, nb_w, nb_h])
    #print(nb)

len_data = len(data["annotations"])

bb = []
nb = []
cls = []

for i in range(len_data):
    cls.append(data["annotations"][i]["class"])
    if "box" in data["annotations"][i]:
        bb.append(data["annotations"][i]["box"])

for i in bb:
    boundingbox_normalization(i, nb)

for i in range(len(cls)):
    if int(cls[i]) < 9:
        print(i, cls[i], ":", nb[i])

out = open('S2-O1301M02959.txt', 'w')

for i in range(len(cls)):
    if int(cls[i]) < 9:
        print(i, cls[i], ":", nb[i], file=out)

out.close()

