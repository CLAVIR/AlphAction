import os
import cv2
import json


def draw_aabb(frame, x1, y1, x2, y2):
    xs = int(x1 * frame.shape[1])
    xe = int(x2 * frame.shape[1])
    ys = int(y1 * frame.shape[0])
    ye = int(y2 * frame.shape[0])
    if ye == frame.shape[0]:
        ye = ye - 1
    if xe == frame.shape[1]:
        xe = xe - 1
    frame[ys:ye, [xs, xe], :] = [0, 0, 255]
    frame[[ys, ye], xs:xe, :] = [0, 0, 255]
    return frame


def main2():
    cap = cv2.VideoCapture("-5KQ66BBWC4.mkv")
    for i in range(903 * 30):
        ret, frame = cap.read()

    for i in range(30):
        ret, frame = cap.read()
        # frame = draw_aabb(frame, 0.077, 0.151, 0.283, 0.811)
        # frame = draw_aabb(frame, 0.226, 0.032, 0.366, 0.497)
        # frame = draw_aabb(frame, 0.332, 0.194, 0.481, 0.891)
        # frame = draw_aabb(frame, 0.505, 0.105, 0.653, 0.780)
        # frame = draw_aabb(frame, 0.626, 0.146, 0.805, 0.818)
        frame = draw_aabb(frame, 0.059, 0.108, 0.214, 0.638)

        cv2.imshow('temp', frame)
        cv2.waitKey(int(1 / 29.97 * 1000))
        a = 1

    a = 1


def get_people_aabbs(frame_index, body_bb_path, frame_size):
    with open(os.path.join(body_bb_path, str(frame_index) + '.txt'), 'r') as f:
        data = f.read()
        lines = data.split("\n")
        while "" in lines:
            lines.remove("")

    people_dict = {}
    for line in lines:
        info = line.split(" ")
        person_id = int(info[0].replace("person", ""))
        pos = []
        for i in range(1, len(info)):
            pos.append(float(info[i]) / frame_size[int((i + 1) % 2)])
        people_dict[person_id] = pos
    return people_dict


def transform_to_ava_dataset_form(video_name, root, start_frame, frame_rate, frame_size, action_dict):
    classes = action_dict
    treebank = os.listdir(root)
    segment_actions = {}
    buf = []
    for dir_name in treebank:
        # get every person's actions
        path = os.path.join(root, dir_name, 'meta.txt')
        with open(path, 'r') as f:
            data = json.loads(f.read())
        string = data['key_frame_visual_sentence']
        type_not_found = True
        action_lst = []
        for action in classes:
            if action in string:
                type_not_found = False
                action_lst.append(action)
        person_action_lst = []
        for action in action_lst:
            part1 = string.split(action + " ")
            for i in range(len(part1) - 1):
                all_tmp = part1[i].split("person")
                sub_tmp = all_tmp[-1].split("_")
                person_id = int(sub_tmp[0])
                if [person_id, classes[action]] not in person_action_lst:
                    person_action_lst.append([person_id, classes[action]])

        if type_not_found:
            raise KeyError("Action type is not defined.")
        img_path = os.path.join(root, dir_name, 'images')
        imgs_name = os.listdir(img_path)
        imgs = []
        for name in imgs_name:
            imgs.append(int(name.split(".")[0]))
        imgs.sort()

        segment_actions[int(dir_name)] = [person_action_lst, int(data['start_idx']), int(data['end_idx']),
                                          imgs[0]]
        buf.append([string, dir_name])

    # format data
    result = []
    keys = list(segment_actions.keys())
    keys.sort()
    for key in keys:
        action_lst, start_id, end_id, physical_start_idx = segment_actions[key]
        sf = start_id
        ef = end_id
        segment_string_lst = []
        for i in range(sf, ef):
            phy_id = i - sf + physical_start_idx
            if phy_id % frame_rate == 0:
                people_dict = get_people_aabbs(i, '{}/s_body_bb'.format(video_name), frame_size)
                for action in action_lst:
                    person = action[0]
                    act = action[1]
                    if person not in people_dict:
                        continue
                    else:
                        pos = people_dict[person]
                    ss = video_name + ",{:04d},".format(int(phy_id / frame_rate))
                    for p in pos:
                        ss = ss + "{:.3f},".format(p)
                    ss = ss + str(act) + "," + str(person)
                    segment_string_lst.append(ss)
        result += segment_string_lst
    result.sort()
    return result


def check_img(video_name, result, start_frame):
    for line in result:
        data = line.split(",")
        frame_index = max(0, int(data[1]) * 25 - start_frame)
        frame = cv2.imread("{}/images/".format(video_name) + str(frame_index) + ".jpg")
        xs = float(data[2])
        ys = float(data[3])
        xe = float(data[4])
        ye = float(data[5])
        frame = draw_aabb(frame, xs, ys, xe, ye)
        cv2.imshow(data[1], frame)
        cv2.waitKey()
        cv2.destroyWindow(data[1])


def get_start_frame(all_frame_path, treebank_0_path):
    start_frame_img = cv2.imread(treebank_0_path)
    all_frames = os.listdir(all_frame_path)
    frames_idx = []
    for frame in all_frames:
        frames_idx.append(int(frame.split('.')[0]))
    frames_idx.sort()
    i = 0
    for idx in frames_idx:
        frame = cv2.imread(os.path.join(all_frame_path, str(idx) + '.png'))
        if (frame == start_frame_img).all():
            break
        i += 1
    return i


def get_physical_start_frame_index(root):
    first_slice_path = os.path.join(root, '0', 'images')
    temp = os.listdir(first_slice_path)
    tp2 = []
    for name in temp:
        tp2.append(int(name.split('.')[0]))
    tp2.sort()
    return tp2[0]


def main3():
    video_name = "sal"
    root = '{}/treebank'.format(video_name)
    frame_size = (1280, 720)
    frame_rate = 25
    start_frame0 = get_physical_start_frame_index(root)  # treebank 0 first picture index
    start_frame2 = get_start_frame(
        video_name + "/images_png",
        os.path.join(root, '0', 'images', str(start_frame0) + '.png')
    )
    start_frame = start_frame0 - start_frame2
    classes = {}
    with open('action_types.txt', 'r') as f:
        data = f.read()
        lines = data.split("\n")
        while "" in lines:
            lines.remove("")
        for line in lines:
            data = line.split(":")
            classes[data[0]] = int(data[1])
    result = transform_to_ava_dataset_form(video_name, root, start_frame, frame_rate, frame_size, classes)
    with open('{}_train.csv'.format(video_name), 'w') as f:
        temp = '\n'.join(result)
        f.write(temp)
    # check_img(result, start_frame)
    a = 1


if __name__ == '__main__':
    main3()
