import json


class WaveSegment:
    """
    Class to store the metadata of a wave segment for analysis, which contains the index of the segment,
    the start and end time of the segment, and the list of frame files that are within the segment.

    :param index: index of the segment
    :type index: int
    :param start_time: start time of the segment
    :type start_time: float
    :param end_time: end time of the segment
    :type end_time: float
    :param frames: list of frame files that are within the segment, defaults to None
    :type frames: list[FrameFile], optional
    """
    __slots__ = ('index', 'start_time', 'end_time', 'frames')

    def __init__(self, index, start_time, end_time, frames=None):
        #: index of the segment
        self.index = index
        #: start time of the segment
        self.start_time = float(start_time)
        #: end time of the segment
        self.end_time = float(end_time)
        #: list of frame files that are within the segment
        self.frames = frames or []

    def __repr__(self):
        return f"WaveSegment(index={self.index}, start_time={self.start_time}, " \
               f"end_time={self.end_time}, frames={len(self.frames)})"

    def to_dict(self):
        """
        Convert the WaveSegment object to a dictionary.

        :return: dictionary of the WaveSegment object
        :rtype: dict
        """
        return {
            'index': self.index,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'frames': [{
                'ifo': frame.ifo,
                'path': frame.path,
                'start_time': frame.start_time,
                'duration': frame.duration
            } for frame in self.frames]
        }


class SLag:
    """
    Class to store the metadata of a SLag, which contains the job id, the slag id, and the segment id.

    :param job_id: job id
    :type job_id: int
    :param slag_id: slag id vector, [0]=jobId - [1]=1/0 1=header slag - [2,..,nIFO+1] ifo slag
    :type slag_id: list[int]
    :param seg_id: segment id vector, [0,..,nIFO-1] ifo segment number
    :type seg_id: list[int]
    """
    __slots__ = ('job_id', 'slag_id', 'seg_id')

    def __init__(self, job_id, slag_id, seg_id):
        #: job id
        self.job_id = job_id
        #: slag id vector : [0]=jobId - [1]=1/0 1=header slag - [2,..,nIFO+1] ifo slag
        self.slag_id = slag_id
        #: seg id vector : [0,..,nIFO-1] ifo segment number
        self.seg_id = seg_id

    def __repr__(self):
        return f"SLag(job_id={self.job_id}, slag_id={self.slag_id}, seg_id={self.seg_id})"


class FrameFile:
    """
    Class to store the metadata of a frame file, which contains the ifo, the path, the start time, and the duration.

    :param ifo: name of the interferometer
    :type ifo: str
    :param path: path of the frame file
    :type path: str
    :param start_time: start time of the frame file
    :type start_time: float
    :param duration: duration of the frame file
    :type duration: float
    """
    __slots__ = ('ifo', 'path', 'start_time', 'duration')

    def __init__(self, ifo, path, start_time, duration):
        #: name of the interferometer
        self.ifo = ifo
        #: path of the frame file
        self.path = path
        #: start time of the frame file
        self.start_time = start_time
        #: duration of the frame file
        self.duration = duration

    def __repr__(self):
        return f"FrameFile(ifo={self.ifo}, path={self.path}, " \
               f"start_time={self.start_time}, duration={self.duration})"

    @property
    def end_time(self):
        """
        Get the end time of the frame file.
        :return: end time of the frame file
        :rtype: float
        """
        return self.start_time + self.duration
