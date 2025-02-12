import os
import json


def generate_detect_bbox(
        video_name, video_idx, root, title,
        score=0.99, global_category_id=None, frame_size=None,
        frame_rate=25
):
    video2delta = {'peixe': 7, 'massa': 56, 'rissois': 38, 'rita': 51, 'robalo': 7, 'sal': 7}
    time_delta = video2delta[video_name]
    labels_path = os.path.join(root, video_name, title)
    bbox_files = os.listdir(labels_path)
    label_idx_lst = []
    for file in bbox_files:
        try:
            label_idx_lst.append(int(file.split(".")[0]))
        except ValueError:
            pass
    label_idx_lst.sort()

    detect_bbox = []
    for idx_r in label_idx_lst:
        # if (idx_r+start_frame) % frame_rate == 0:
        if idx_r % frame_rate == 0:
            idx = int(idx_r / frame_rate) + time_delta
            image_id = 10000 * video_idx + idx

            with open(os.path.join(root, video_name, title, str(idx_r) + '.txt'), 'r') as f:
                raw = f.read()
            lines = raw.split("\n")
            while "" in lines:
                lines.remove("")
            for line in lines:
                info = line.split(" ")
                if global_category_id is None:
                    category_id = int(info[0]) + 2
                else:
                    category_id = global_category_id
                bbox = []
                for i in range(1, 5):
                    if frame_size is None:
                        bbox.append(float(info[i]))
                    else:
                        bbox.append(float(info[i]) / frame_size[(i + 1) % 2])
                detect_bbox.append({
                    'image_id': image_id,
                    'score': score,
                    'bbox': bbox,
                    'category_id': category_id
                })

    return detect_bbox


def main():
    video_names = [
        'massa',
        'peixe',
        'rissois',
        'rita',
        'robalo',
        'sal'
    ]
    data_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             'collaborative_manipulation_dataset')
    all_detect_bbox_dict = {}
    all_people_bbox_dict = {}
    for i in range(len(video_names)):
        name = video_names[i]
        dbl = generate_detect_bbox(name, i, data_root, 'labels')
        pbl = generate_detect_bbox(name, i, data_root, 's_body_bb', global_category_id=1)
        all_detect_bbox_dict[name] = dbl
        all_people_bbox_dict[name] = pbl
    print("Prepare finished.")
    for name in all_detect_bbox_dict:
        train_det_obj_bbox = []
        val_det_person_bbox = all_people_bbox_dict[name]
        val_det_obj_bbox = all_detect_bbox_dict[name]
        for name2 in all_detect_bbox_dict:
            if name != name2:
                train_det_obj_bbox.extend(all_detect_bbox_dict[name2])
        output_path = os.path.join(data_root, name, 'boxes')
        with open(os.path.join(output_path, 'lfv_{}_train_det_object_bbox.json'.format(name)), 'w') as f:
            json.dump(train_det_obj_bbox, f)
        with open(os.path.join(output_path, 'lfv_{}_val_det_object_bbox.json'.format(name)), 'w') as f:
            json.dump(val_det_obj_bbox, f)
        with open(os.path.join(output_path, 'lfv_{}_val_det_person_bbox.json'.format(name)), 'w') as f:
            json.dump(val_det_person_bbox, f)
        print('LFV_{} dump finished.'.format(name))


if __name__ == '__main__':
    main()
