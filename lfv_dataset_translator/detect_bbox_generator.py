import os
import json
from lfv_dataset_translator.dataset_translator import get_physical_start_frame_index, get_start_frame


def generate_detect_bbox(
        video_name, video_idx, root, title,
        score=0.99, global_category_id=None, frame_size=None,
        frame_rate=25
):
    labels_path = os.path.join(root, video_name, title)
    bbox_files = os.listdir(labels_path)
    label_idx_lst = []
    for file in bbox_files:
        try:
            label_idx_lst.append(int(file.split(".")[0]))
        except ValueError:
            pass
    label_idx_lst.sort()
    physical_start_frame = get_physical_start_frame_index(os.path.join(root, video_name, 'treebank'))
    delta_frame_count = get_start_frame(
        os.path.join(root, video_name, 'images_png'),
        os.path.join(root, video_name, 'treebank', '0', 'images', str(physical_start_frame) + '.png')
    )
    start_frame = physical_start_frame - delta_frame_count

    detect_bbox = []
    for idx_r in label_idx_lst:
        if (idx_r+start_frame) % frame_rate == 0:
            idx = int((idx_r+start_frame) / frame_rate)
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
    out_root = '../data/LFV_training'
    all_detect_bbox_dict = {}
    all_people_bbox_dict = {}
    for i in range(len(video_names)):
        name = video_names[i]
        dbl = generate_detect_bbox(name, i, '.', 'labels')
        pbl = generate_detect_bbox(name, i, '.', 'body_bb', global_category_id=1)
        all_detect_bbox_dict[name] = dbl
        all_people_bbox_dict[name] = pbl
    print("Prepare finished.")
    for name in all_detect_bbox_dict:
        train_det_obj_bbox = []
        val_det_person_bbox = all_people_bbox_dict[name]
        val_det_obj_bbox = all_detect_bbox_dict[name]
        for name2 in all_detect_bbox_dict:
            if name != name2:
                train_det_obj_bbox.append(all_detect_bbox_dict[name2])
        output_path = os.path.join(out_root, 'lfv_' + name, 'boxes')
        with open(os.path.join(output_path, 'lfv_{}_train_det_object_bbox.json'.format(name)), 'w') as f:
            json.dump(train_det_obj_bbox, f)
        with open(os.path.join(output_path, 'lfv_{}_val_det_object_bbox.json'.format(name)), 'w') as f:
            json.dump(val_det_obj_bbox, f)
        with open(os.path.join(output_path, 'lfv_{}_val_det_person_bbox.json'.format(name)), 'w') as f:
            json.dump(val_det_person_bbox, f)
        print('LFV_{} dump finished.'.format(name))

    a = 1


if __name__ == '__main__':
    main()
