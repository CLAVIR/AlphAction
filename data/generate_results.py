"""Given a video name and the gt video segmentation, we predict action names"""

import csv
import math
import os
import os.path as osp
import pickle

from lfv_dataset_translator.dataset_translator import get_physical_start_frame_index, get_start_frame

from manipulation_knowledge_base.CO_KB import ALL_GOALS, ALL_OBJECTS, BODYPARTS, INTERACTIONS, OBJECTS, TOOLS, \
    PLACES, GOALS


def parse_ground_truth(ground_truth):
    gt_action_seq = []
    with open(ground_truth, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            words_start_id = line.index('[')
            words_end_id = line.index(']')
            words = line[words_start_id + 1:words_end_id]
            obj_goal_words = set()
            person_words = set()
            word_lst = words.split(' ')
            for word in word_lst:
                if 'person' in word:
                    person_words.add(word.split('_')[0])
                else:
                    word = ' '.join(word.split('_'))
                    assert word in OBJECTS + TOOLS + PLACES + GOALS + ['transfer', 'handover', 'holding', 'egg mixture',
                                                                       'mixture']
                    obj_goal_words.add(word)
            frame_start_id = 0
            frame_end_id = line.index('[')
            frame_str = line[frame_start_id:frame_end_id]
            start_frame_str, end_frame_str = frame_str.split(',')[0], frame_str.split(',')[1]
            start_frame = int(start_frame_str)
            end_frame = int(end_frame_str)
            gt_action_seq.append((start_frame, end_frame, (obj_goal_words, person_words)))
    return gt_action_seq


def load_gt_action_seq(data_root_dir, video_name):
    # first load gt
    video_gt_path = osp.join(data_root_dir, '..', 'collaborative_manipulation_dataset', video_name, 'gt')

    return parse_ground_truth(video_gt_path)


def load_gt(data_root_dir, video_name):
    # first load gt
    video_gt_csv = osp.join(data_root_dir, '..', 'collaborative_manipulation_dataset', video_name,
                            'lfv_{}_val.csv'.format(video_name))

    gt = dict()

    with open(video_gt_csv, newline='') as csvfile:
        video_gt_csv_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in video_gt_csv_reader:
            _, tid, x_min, y_min, x_max, y_max, aid, pid = row[0].split(',')
            x_min = float(x_min)
            y_min = float(y_min)
            x_max = float(x_max)
            y_max = float(y_max)

            if tid not in gt:
                gt[tid] = {(x_min, y_min, x_max, y_max): (aid, pid)}
            else:
                # print(tid)
                # assert (x_min, y_min, x_max, y_max) not in gt[tid]
                gt[tid][(x_min, y_min, x_max, y_max)] = (aid, pid)

    return gt


def load_det_res(data_root_dir, video_name, gt):
    # first load detection results
    video_result = dict()

    video_result_csv = osp.join(data_root_dir, 'output', 'resnet50_4x16f_baseline_{}'.format(video_name),
                                'inference', 'lfv_{}_val_ava_video'.format(video_name),
                                'result.csv')

    with open(video_result_csv, newline='') as csvfile:
        video_result_csv_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in video_result_csv_reader:
            _, tid, x_min, y_min, x_max, y_max, aid, score = row[0].split(',')
            x_min = float(x_min)
            y_min = float(y_min)
            x_max = float(x_max)
            y_max = float(y_max)
            score = float(score)

            assert tid in gt
            print(x_min, y_min, x_max, y_max)
            print(tid)
            assert (x_min, y_min, x_max, y_max) in gt[tid]

            # first we get the corresponding pid
            pid = gt[tid][(x_min, y_min, x_max, y_max)][1]

            assert pid in ['0', '1']

            if tid not in video_result:
                video_result[tid] = {pid: [(aid, score)]}
            else:
                if pid not in video_result[tid]:
                    video_result[tid][pid] = [(aid, score)]
                else:
                    video_result[tid][pid].append((aid, score))

    return video_result


def format_tid(int_tid):
    """Convert int tid to string tid."""
    str_tid = str(10000 + int_tid)
    return str_tid[1:]


def get_action(action_det_lst, thres=0.1, action_size=13):
    max_conf = 0
    detected_action = None

    for action_id, action_conf in action_det_lst:
        if int(action_id) > action_size:
            break
        if action_conf < thres:
            continue
        if action_conf > max_conf:
            max_conf = action_conf
            detected_action = action_id
    return detected_action


def create_seg_det_results(video_seg, video_result, action_id_name_map, video_name):
    final_results = {}
    video2delta = {'peixe': 7, 'massa': 56, 'rissois': 38, 'rita': 51, 'robalo': 7, 'sal': 7}
    for seg_start, seg_end in video_seg:
        seg_start_tid_int = math.ceil(seg_start / 25)
        seg_end_tid_int = math.ceil(seg_end / 25)

        # for each person, we find the action he is performing in this segmentation
        for pid in ['0', '1']:
            max_count_action = 0
            pid_action = None
            action_count = {}
            for seg_tid_int in range(seg_start_tid_int, seg_end_tid_int + 1):
                seg_tid_str = format_tid(seg_tid_int)
                if seg_tid_str in video_result:
                    if pid in video_result[seg_tid_str]:
                        action = get_action(video_result[seg_tid_str][pid])
                        if action is None:
                            continue
                        if action in action_count:
                            action_count[action] += 1
                        else:
                            action_count[action] = 1
                        if action_count[action] > max_count_action:
                            max_count_action = action_count[action]
                            pid_action = action
            if pid_action is not None:
                if (
                        seg_start - 25 * video2delta[video_name],
                        seg_end - 25 * video2delta[video_name]) not in final_results:
                    final_results[(seg_start - 25 * video2delta[video_name],
                                   seg_end - 25 * video2delta[video_name])] = {pid: action_id_name_map[pid_action]}
                else:
                    final_results[(seg_start - 25 * video2delta[video_name],
                                   seg_end - 25 * video2delta[video_name])][pid] = action_id_name_map[pid_action]
    return final_results


class DetAction(object):
    def __init__(self, predicate, if_col):
        self.predicate = predicate
        self.if_col = if_col
        self.id = None


def can_merge(tree_a, tree_b):
    # tree_a is the tree that belongs to an existing group
    # tree_b is not
    if tree_a.predicate[1] == tree_b.predicate[1] and tree_a.predicate[2] == tree_b.predicate[2]:
        return True
    return False


def merge_seg_det_results(seg_det_results):
    person_ids = ['0', '1']
    seg_det_lst = []
    for i, (start_frame, end_frame) in enumerate(seg_det_results):
        action_lst = []
        if_col = False
        predicate_lst = []
        for j, pid in enumerate(seg_det_results[(start_frame, end_frame)]):
            predicate = (
                (start_frame, end_frame), {'person{}'.format(pid)}, {seg_det_results[(start_frame, end_frame)][pid]})
            predicate_lst.append(predicate)
            action_lst.append(DetAction(predicate, False))
            if 'holding' in seg_det_results[(start_frame, end_frame)][pid] or \
                    'handover' in seg_det_results[(start_frame, end_frame)][pid]:
                if_col = True
        if if_col and len(person_ids) == len(action_lst):  # we merge two actions
            col_predicate = ((start_frame, end_frame), predicate_lst[0][1].union(predicate_lst[1][1]),
                             predicate_lst[0][2].union(predicate_lst[1][2]))
            col_action_lst = [DetAction(col_predicate, True)]
            seg_det_lst.append(col_action_lst)
        else:
            seg_det_lst.append(action_lst)
    merge_window = 100
    num_group = 0
    action_dict = {}
    for i, tree_lst in enumerate(seg_det_lst):
        for j, tree in enumerate(tree_lst):
            if not tree.if_col:
                continue
            if tree.id is not None:
                continue
            tree.id = num_group
            action_dict[tree.id] = [tree]
            num_group += 1
            # 1. go forward
            # check in the same time segment
            for k in range(j + 1, len(tree_lst), 1):
                # check if two trees can be merged
                if can_merge(tree, tree_lst[k]):
                    tree_lst[k].id = tree.id
                    action_dict[tree.id].append(tree_lst[k])

            num_empty = 0
            # check in the later time groups
            for k in range(i + 1, len(seg_det_lst), 1):
                if k > i + merge_window:
                    break
                if_added = False
                for later_tree in seg_det_lst[k]:
                    if later_tree.id is not None:
                        continue
                    if can_merge(tree, later_tree):
                        later_tree.id = tree.id
                        action_dict[tree.id].append(later_tree)
                        if_added = True
                if not if_added:
                    num_empty += 1
                if not if_added and (len(seg_det_lst[k]) > 0 or num_empty > 1):
                    break

            # 2. go backward
            # check in the same time segment
            for k in range(j - 1, -1, -1):
                if can_merge(tree, tree_lst[k]):
                    tree_lst[k].id = tree.id
                    action_dict[tree.id].append(tree_lst[k])
            num_empty = 0
            # check in the previous time groups
            for k in range(i - 1, -1, -1):
                if k < i - merge_window:
                    break
                if_added = False
                for previous_tree in seg_det_lst[k]:
                    if previous_tree.id is not None:
                        continue
                    if can_merge(tree, previous_tree):
                        previous_tree.id = tree.id
                        action_dict[tree.id].append(previous_tree)
                        if_added = True
                if not if_added:
                    num_empty += 1
                if not if_added and (len(seg_det_lst[k]) > 0 or num_empty > 1):
                    break
    # then we want to merge single mani trees
    for i, tree_lst in enumerate(seg_det_lst):
        for j, tree in enumerate(tree_lst):
            if tree.id is not None:
                continue
            tree.id = num_group
            action_dict[tree.id] = [tree]
            num_group += 1
            for k in range(j + 1, len(tree_lst), 1):
                if can_merge(tree, tree_lst[k]):
                    tree_lst[k].id = tree.id
                    action_dict[tree.id].append(tree_lst[k])
            # check in the later time groups
            num_empty = 0
            for k in range(i + 1, len(seg_det_lst), 1):
                if k > i + merge_window:
                    break
                if_added = False
                for later_tree in seg_det_lst[k]:
                    if later_tree.id is not None:
                        continue
                    if can_merge(tree, later_tree):
                        later_tree.id = tree.id
                        action_dict[tree.id].append(later_tree)
                        if_added = True
                if not if_added:
                    num_empty += 1
                if not if_added and (len(seg_det_lst[k]) > 0 or num_empty > 1):
                    break
    return recover_action_seq(action_dict)


def recover_action_seq(action_dict):
    action_seq = []
    for grp_id in action_dict:
        min_time = 10000
        max_time = 0
        final_tree = None
        max_complex = 0
        for tree in action_dict[grp_id]:
            if tree.predicate[0][0] < min_time:
                min_time = tree.predicate[0][0]
            if tree.predicate[0][1] > max_time:
                max_time = tree.predicate[0][1]
            if len(tree.predicate[2]) > max_complex:
                final_tree = tree
                max_complex = len(tree.predicate[2])
        action_seq.append((min_time, max_time, (final_tree.predicate[1], final_tree.predicate[2])))
    # now we sort action sequence based on start time
    sorted_action_seq = sorted(action_seq, key=lambda x: x[0])
    for action in sorted_action_seq:
        print('start time: {}, end time: {}, representative tree: {}'.format(action[0], action[1], action[2]))

    return sorted_action_seq


def load_our_video_segmentation(video_seg_path, root, video_name, frame_rate=25):
    video2delta = {'peixe': 7, 'massa': 56, 'rissois': 38, 'rita': 51, 'robalo': 7, 'sal': 7}

    our_video_segmentation = pickle.load(open(video_seg_path, 'rb'))

    print("old: ", our_video_segmentation)

    aligned_our_video_segmentation = []

    last_bp = 0 + video2delta[video_name] * 25
    for waypoint in our_video_segmentation:
        aligned_our_video_segmentation.append((last_bp, waypoint + video2delta[video_name] * 25))
        last_bp = waypoint + video2delta[video_name] * 25

    return aligned_our_video_segmentation


def compute_accuracy(gt_action_seq, detected_action_seq):
    num_gt_trees = len(gt_action_seq)
    num_detected_trees = len([detected_action[1] for detected_action in
                              detected_action_seq if detected_action[2][1] != {'none'}])

    print("Number of gt trees: {}".format(num_gt_trees))
    print("Number of detected trees: {}".format(num_detected_trees))

    # then compute precision
    num_correct_det = 0
    for det_action in detected_action_seq:
        det_start, det_end, det_info = det_action
        is_correct = False
        for gt_action in gt_action_seq:
            gt_start, gt_end, gt_info = gt_action
            if gt_start > det_end or det_start > gt_end:
                continue
            if det_info[0] == gt_info[1] and len(det_info[1] - gt_info[0]) == 0:
                num_correct_det += 1
                is_correct = True
                break
        if not is_correct:
            print("Not correct: ", det_action)

    print("Precision: {} / {} = {}".format(num_correct_det, num_detected_trees, num_correct_det / num_detected_trees))
    print("Recall: {} / {} = {}".format(num_correct_det, num_gt_trees, num_correct_det / num_gt_trees))


def generate_results(data_root_dir, video_name, action_id_name_map):
    """Try to generate action detection results for each video segment."""

    gt_action_seq = load_gt_action_seq(data_root_dir, video_name)

    gt = load_gt(data_root_dir, video_name)

    video_result = load_det_res(data_root_dir, video_name, gt)

    video_segmentation_path = osp.join('/root/learning-from-videos/collaborative_manipulation_dataset',
                                       video_name, 'segmentation.pkl')

    video_segmentation = load_our_video_segmentation(video_segmentation_path, data_root_dir, video_name)

    seg_det_results = create_seg_det_results(video_segmentation, video_result, action_id_name_map, video_name)

    merged_seg_det_results = merge_seg_det_results(seg_det_results)

    compute_accuracy(gt_action_seq, merged_seg_det_results)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--video_name', type=str, required=True)

    args = parser.parse_args()

    data_root_dir = osp.dirname(osp.abspath(__file__))

    action_types_file = osp.join(data_root_dir, 'action_types.txt')

    # also load action types
    action_id_name_map = {}
    with open(action_types_file) as f:
        lines = f.readlines()
        for line in lines:
            action_name, action_id = line.strip().split(':')
            action_id_name_map[action_id] = action_name

    generate_results(data_root_dir, args.video_name, action_id_name_map)
