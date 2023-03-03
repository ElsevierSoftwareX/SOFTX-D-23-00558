from pathlib import Path
from .types import FrameFile
import logging

logger = logging.getLogger(__name__)


def get_frame_meta(frame_list_file, ifo, label=".gwf"):
    # read the frame list file
    frame_list = []

    with open(frame_list_file, 'r') as f:
        for frame_path in f.readlines():
            if frame_path.startswith("#"):
                continue

            # remove header created with gw_data_find
            frame_path = frame_path.replace("framefile=", "")
            frame_path = frame_path.replace("file://localhost", "")
            frame_path = frame_path.replace("gsiftp://ldr.aei.uni-hannover.de:15000", "")

            # if frame_path contains label
            if frame_path.find(label) != -1:
                # test if file exists
                # if not Path(frame_path).is_file():
                #     logger.error("Frame file not found: %s", frame_path)
                #     raise FileNotFoundError("Frame file not found: {}".format(frame_path))

                # get the file name without the extension with pathlib
                frame_name = Path(frame_path).stem
                # get the gps time and duration with int type
                gps_start, duration = [int(i) for i in frame_name.split("-")[-2:]]

                # if gps start smaller than the gps time 2015-01-01 or duration is smaller than 1,
                # throw an error of bad format
                if gps_start < 1104105616 or duration < 1:
                    raise ValueError("Frame file name format is not correct: {}".format(frame_path))

                # append the frame file to the list
                frame_list.append(FrameFile(ifo, frame_path, gps_start, duration))

    return frame_list


def select_frame_list(frame_list, start, stop, seg_edge):
    seg_start = start - seg_edge
    seg_stop = stop + seg_edge

    frame_list = [frame for frame in frame_list
              if frame.start_time < seg_stop and frame.start_time + frame.duration > seg_start]
    return frame_list


