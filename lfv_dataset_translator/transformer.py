import json

with open("lfv_action_list.pbtxt", 'r') as f:
    raw = f.read()
lines = raw.split("\n")
names = []
label_ids = []
for line in lines:
    if "name:" in line:
        temp = line.split(":")
        names.append(temp[-1])

    if "label_id:" in line:
        temp = line.split(":")
        label_ids.append(temp[-1])

# with open("lfv_action_list_formed.pbtxt", 'w') as f:
#     for i in range(len(names)):
#         string = "item {\n  name:" + names[i] + '\n  id:' + label_ids[i] + "\n}\n"
#         f.write(string)

with open("action_types.txt", 'w') as f:
    for i in range(len(names)):
        name = (names[i].replace('"', "").lstrip()).split(" ")[0]
        string = name + ":" + label_ids[i].lstrip() + '\n'
        f.write(string)
a = 1
