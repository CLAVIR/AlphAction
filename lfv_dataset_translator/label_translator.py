import os


def get_sorted_file_ids(path, exclude_files=None):
    if exclude_files is None:
        exclude_files = []
    labels = []
    label_names = os.listdir(path)
    for label_name in label_names:
        info = label_name.split('.')
        if info[0] not in exclude_files:
            labels.append(int(info[0]))
    labels.sort()
    return labels


def get_split_data(data, label='\n'):
    temp = data.split(label)
    while "" in temp:
        temp.remove("")
    return temp


def split_person_actions(person_split, actions):
    handover_flag = False
    person_acts = []
    for i, person_line in enumerate(person_split):
        if not handover_flag:
            for act in actions:
                if act + " " in person_line:
                    if act != 'handover':
                        person_acts.append([person_line[0], act])
                    else:
                        person_acts.append([person_line[0], act])
                        person_acts.append([person_split[i + 1][0], act])
                        handover_flag = True
        else:
            handover_flag = False
    return person_acts


def translate_label(data_dir, video_name, time_delta, frame_rate=25, frame_size=(1280, 720)):
    '''
    :param video_name: req which video you want to translate
    :param frame_rate: opt default is 25
    :param frame_size: opt default is 1280x720
    '''

    body_path = os.path.join(data_dir, 's_body_bb')

    bodies = get_sorted_file_ids(body_path, ['classes'])

    with open('action_types.txt', 'r') as f:
        raw_actions = get_split_data(f.read())
    actions = {}
    for line in raw_actions:
        info = line.split(":")
        actions[info[0]] = int(info[1])

    with open(os.path.join(data_dir, 'gt'), 'r') as f:
        raw_gt_info = get_split_data(f.read())

    gt_info = []
    for line in raw_gt_info:
        info = line.split(" [")
        raw_time_stamp = info[0]
        str_time_stamps = get_split_data(raw_time_stamp, ',')
        time_stamps = []
        for ts in str_time_stamps:
            time_stamps.append(int(ts))

        action_info = info[1].rstrip(']')
        person_split = get_split_data(action_info, 'person')
        person_acts = split_person_actions(person_split, actions)
        gt_info.append([time_stamps, person_acts])

    total_lst = []
    for gt_line in gt_info:
        start, end = gt_line[0]
        person_acts = gt_line[1]

        for i in range(start, end + 1):
            if i % frame_rate == 0 and i in bodies:
                file_name = '{}.txt'.format(i)
                frame_body_path = os.path.join(body_path, file_name)
                with open(frame_body_path, 'r') as f:
                    body_lines = get_split_data(f.read())
                for body_line in body_lines:
                    info = get_split_data(body_line, ' ')
                    person_id = info[0].replace('person', "")
                    aabb = []
                    for j in range(4):
                        aabb.append(int(info[j + 1]) / float(frame_size[j % 2]))
                    for pl in person_acts:
                        pid, act = pl
                        if person_id == pid:
                            total_lst.append(
                                [video_name, int(i / frame_rate) + time_delta, aabb, actions[act], person_id])

    with open(os.path.join(data_dir, 'lfv_data_set.csv'), 'w') as f:
        for line in total_lst:
            f.write('{},{:04d},{:.3f},{:.3f},{:.3f},{:.3f},{},{}\n'.format(
                line[0], line[1], line[2][0], line[2][1], line[2][2], line[2][3],
                line[3], line[4]
            ))


if __name__ == '__main__':
    import argparse

    ap = argparse.ArgumentParser()

    # for synchronizing the time
    video2delta = {'peixe': 7, 'massa': 56, 'rissois': 38, 'rita': 51, 'robalo': 7, 'sal': 7}

    ap.add_argument('-v', '--video_name', type=str, required=True)

    args = ap.parse_args()

    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            'collaborative_manipulation_dataset',
                            args.video_name)
    translate_label(data_dir, args.video_name, video2delta[args.video_name])
