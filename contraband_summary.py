import time
"""
Tracks all occurrences of contraband detections. Stores tuples of
(detection, time, frame) in a list, contraband_detections, that
can be accessed to produce a log of contraband detections, the
time they occurred, and the video frame of the incident.
"""

class ContrabandSummary:
    def __init__(self):
        self.contraband_detections = []
        self.current_image = None

    def update_contraband(self, contraband):
        detect_time = time.localtime()
        self.contraband_detections.append((contraband, detect_time))
        
    def get_summary(self):
        """
        Prints the detection to the console.

        Parameters
        -------
        contraband : string
            The label of the detected object
        """
        items = self.get_contraband_string()
        print(*items)

    def update_image(self, frame):
        self.current_image = frame

    def get_image(self):
        return self.current_image

    def get_contraband_string(self):
        """
        Returns a list of strings describing all of the detected contraband

        Returns
        -------
        contraband_string: []
            A list of text describing all of the detected contraband and the time of detection
        """
        contraband_string = [""]
        for contraband, detect_time in self.contraband_detections:
            string_time = time.strftime('%Y-%m-%d %H:%M:%S', detect_time)
            contraband_string.append(contraband + " detected at " + string_time + "\n")
        return contraband_string
