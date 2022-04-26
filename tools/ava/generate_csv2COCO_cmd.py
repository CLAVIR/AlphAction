head = 'python tools/ava/csv2COCO.py'


def generate_cmd(video_name, title):
    arg0 = 'data/temp/lfv_{}/annotations/lfv_{}_{}.csv'
    arg1 = 'data/temp/lfv_{}/annotations/lfv_file_names_trainval.txt'
    arg2 = 'data/temp/lfv_{}/keyframes/trainval_{}'
    return arg0.format(video_name, video_name, title), arg1.format(video_name), arg2.format(video_name, video_name)
