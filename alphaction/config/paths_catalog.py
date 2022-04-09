"""Centralized catalog of paths."""

import os


class DatasetCatalog(object):
    DATA_DIR = "data"
    DATASETS = {
        "ava_video_train_v2.2": {
            "video_root": "AVA/clips/trainval",
            "ann_file": "AVA/annotations/ava_train_v2.2_min.json",
            "box_file": "",
            "eval_file_paths": {
                "csv_gt_file": "AVA/annotations/ava_train_v2.2.csv",
                "labelmap_file": "AVA/annotations/ava_action_list_v2.2_for_activitynet_2019.pbtxt",
                "exclusion_file": "AVA/annotations/ava_train_excluded_timestamps_v2.2.csv",
            },
            "object_file": "AVA/boxes/ava_train_det_object_bbox.json",
        },
        "ava_video_val_v2.2": {
            "video_root": "AVA/clips/trainval",
            "ann_file": "AVA/annotations/ava_val_v2.2_min.json",
            "box_file": "AVA/boxes/ava_val_det_person_bbox.json",
            "eval_file_paths": {
                "csv_gt_file": "AVA/annotations/ava_val_v2.2.csv",
                "labelmap_file": "AVA/annotations/ava_action_list_v2.2_for_activitynet_2019.pbtxt",
                "exclusion_file": "AVA/annotations/ava_val_excluded_timestamps_v2.2.csv",
            },
            "object_file": "AVA/boxes/ava_val_det_object_bbox.json",
        },

        'lfv_massa_train_ava_video': {
            "video_root": "lfv_massa/clips/trainval",
            "ann_file": "lfv_massa/annotations/lfv_massa_train_min.json",
            "box_file": "",
            "eval_file_paths": {
                "csv_gt_file": "lfv_massa/annotations/lfv_massa_train.csv",
                "labelmap_file": "lfv_massa/annotations/lfv_action_list.pbtxt",
                # "exclusion_file": "data/lfv_massa/annotations/ava_train_excluded_timestamps_v2.2.csv",
            },
            "object_file": "lfv_massa/boxes/lfv_massa_train_det_object_bbox.json",
        },
        'lfv_massa_val_ava_video': {
            "video_root": "lfv_massa/clips/trainval",
            "ann_file": "lfv_massa/annotations/lfv_massa_val_min.json",
            "box_file": "lfv_massa/boxes/lfv_massa_val_det_person_bbox.json",
            "eval_file_paths": {
                "csv_gt_file": "lfv_massa/annotations/lfv_massa_val.csv",
                "labelmap_file": "lfv_massa/annotations/lfv_action_list.pbtxt",
                # "exclusion_file": "data/lfv_massa/annotations/ava_val_excluded_timestamps_v2.2.csv",
            },
            "object_file": "lfv_massa/boxes/lfv_massa_val_det_object_bbox.json",
        },
        'lfv_peixe_train_ava_video': {
            "video_root": "lfv_peixe/clips/trainval",
            "ann_file": "lfv_peixe/annotations/lfv_peixe_train_min.json",
            "box_file": "",
            "eval_file_paths": {
                "csv_gt_file": "lfv_peixe/annotations/lfv_peixe_train.csv",
                "labelmap_file": "lfv_peixe/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_peixe/boxes/lfv_peixe_train_det_object_bbox.json",
        },
        'lfv_peixe_val_ava_video': {
            "video_root": "lfv_peixe/clips/trainval",
            "ann_file": "lfv_peixe/annotations/lfv_peixe_val_min.json",
            "box_file": "lfv_peixe/boxes/lfv_peixe_val_det_person_bbox.json",
            "eval_file_paths": {
                "csv_gt_file": "lfv_peixe/annotations/lfv_peixe_val.csv",
                "labelmap_file": "lfv_peixe/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_peixe/boxes/lfv_peixe_val_det_object_bbox.json",
        },
        'lfv_rissois_train_ava_video': {
            "video_root": "lfv_rissois/clips/trainval",
            "ann_file": "lfv_rissois/annotations/lfv_rissois_train_min.json",
            "box_file": "",
            "eval_file_paths": {
                "csv_gt_file": "lfv_rissois/annotations/lfv_rissois_train.csv",
                "labelmap_file": "lfv_rissois/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_rissois/boxes/lfv_rissois_train_det_object_bbox.json",
        },
        'lfv_rissois_val_ava_video': {
            "video_root": "lfv_rissois/clips/trainval",
            "ann_file": "lfv_rissois/annotations/lfv_rissois_val_min.json",
            "box_file": "lfv_rissois/boxes/lfv_rissois_val_det_person_bbox.json",
            "eval_file_paths": {
                "csv_gt_file": "lfv_rissois/annotations/lfv_rissois_val.csv",
                "labelmap_file": "lfv_rissois/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_rissois/boxes/lfv_rissois_val_det_object_bbox.json",
        },
        'lfv_rita_train_ava_video': {
            "video_root": "lfv_rita/clips/trainval",
            "ann_file": "lfv_rita/annotations/lfv_rita_train_min.json",
            "box_file": "",
            "eval_file_paths": {
                "csv_gt_file": "lfv_rita/annotations/lfv_rita_train.csv",
                "labelmap_file": "lfv_rita/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_rita/boxes/lfv_rita_train_det_object_bbox.json",
        },
        'lfv_rita_val_ava_video': {
            "video_root": "lfv_rita/clips/trainval",
            "ann_file": "lfv_rita/annotations/lfv_rita_val_min.json",
            "box_file": "lfv_rita/boxes/lfv_rita_val_det_person_bbox.json",
            "eval_file_paths": {
                "csv_gt_file": "lfv_rita/annotations/lfv_rita_val.csv",
                "labelmap_file": "lfv_rita/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_rita/boxes/lfv_rita_val_det_object_bbox.json",
        },
        'lfv_robalo_train_ava_video': {
            "video_root": "lfv_robalo/clips/trainval",
            "ann_file": "lfv_robalo/annotations/lfv_robalo_train_min.json",
            "box_file": "",
            "eval_file_paths": {
                "csv_gt_file": "lfv_robalo/annotations/lfv_robalo_train.csv",
                "labelmap_file": "lfv_robalo/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_robalo/boxes/lfv_robalo_train_det_object_bbox.json",
        },
        'lfv_robalo_val_ava_video': {
            "video_root": "lfv_robalo/clips/trainval",
            "ann_file": "lfv_robalo/annotations/lfv_robalo_val_min.json",
            "box_file": "lfv_robalo/boxes/lfv_robalo_val_det_person_bbox.json",
            "eval_file_paths": {
                "csv_gt_file": "lfv_robalo/annotations/lfv_robalo_val.csv",
                "labelmap_file": "lfv_robalo/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_robalo/boxes/lfv_robalo_val_det_object_bbox.json",
        },
        'lfv_sal_train_ava_video': {
            "video_root": "lfv_sal/clips/trainval",
            "ann_file": "lfv_sal/annotations/lfv_sal_train_min.json",
            "box_file": "",
            "eval_file_paths": {
                "csv_gt_file": "lfv_sal/annotations/lfv_sal_train.csv",
                "labelmap_file": "lfv_sal/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_sal/boxes/lfv_sal_train_det_object_bbox.json",
        },
        'lfv_sal_val_ava_video': {
            "video_root": "lfv_sal/clips/trainval",
            "ann_file": "lfv_sal/annotations/lfv_sal_val_min.json",
            "box_file": "lfv_sal/boxes/lfv_sal_val_det_person_bbox.json",
            "eval_file_paths": {
                "csv_gt_file": "lfv_sal/annotations/lfv_sal_val.csv",
                "labelmap_file": "lfv_sal/annotations/lfv_action_list.pbtxt",
            },
            "object_file": "lfv_sal/boxes/lfv_sal_val_det_object_bbox.json",
        },
    }

    @staticmethod
    def get(name):
        if "ava_video" in name:
            data_dir = DatasetCatalog.DATA_DIR
            attrs = DatasetCatalog.DATASETS[name]
            if attrs["box_file"] == "":
                box_file = ""
            else:
                box_file = os.path.join(data_dir, attrs["box_file"])
            args = dict(
                video_root=os.path.join(data_dir, attrs["video_root"]),
                ann_file=os.path.join(data_dir, attrs["ann_file"]),
                box_file=box_file,
                eval_file_paths={key: os.path.join(data_dir, attrs["eval_file_paths"][key]) for key in
                                 attrs["eval_file_paths"]},
                object_file=os.path.join(data_dir, attrs["object_file"]),
            )
            return dict(
                factory="AVAVideoDataset",
                args=args
            )
        raise RuntimeError("Dataset not available: {}".format(name))
