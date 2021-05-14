import time

import edgeiq
from contraband_summary import ContrabandSummary

"""
Detect items that are considered contraband for working or learning from home,
namely cell phones, headphones, books, etc.

This example app uses two detection models in order to increase the number of
detections as well as the types of detections. The models this app uses are
"alwaysai/ssd_mobilenet_v2_oidv4" and
"alwaysai/ssd_inception_v2_coco_2018_01_28".

Additionally, this app uses a object tracker to reduce instances where the same
object is detected as a new object.

To change the computer vision model, the engine and accelerator, and add
additional dependencies read this guide:
https://alwaysai.co/docs/application_development/configuration_and_packaging.html
"""


def main():
    # if you would like to test an additional model, add one to the list below:
    models = [
            "alwaysai/ssd_mobilenet_v2_oidv4",
            "alwaysai/ssd_inception_v2_coco_2018_01_28"]

    # include any labels that you wish to detect from any models (listed above
    # in 'models') here in this list
    contraband_labels = [
            "Pen", "cell phone", "backpack", "book", "Book",
            "Ring binder", "Headphones", "Calculator", "Mobile phone",
            "Telephone", "Microphone", "Ipod", "Remote control"]

    # load all the models (creates a new object detector for each model)
    detectors = []
    for model in models:

        # start up a first object detection model
        obj_detect = edgeiq.ObjectDetection(model)
        obj_detect.load(engine=edgeiq.Engine.DNN)

        # track the generated object detection items by storing them
        # in detectors
        detectors.append(obj_detect)

        # print the details of each model to the console
        print("Model:\n{}\n".format(obj_detect.model_id))
        print("Engine: {}".format(obj_detect.engine))
        print("Accelerator: {}\n".format(obj_detect.accelerator))
        print("Labels:\n{}\n".format(obj_detect.labels))

    fps = edgeiq.FPS()
    contraband_summary = ContrabandSummary()

    def handle_detected_contraband(object_id, prediction):
        print('Detected {}!'.format(prediction.label))
        contraband_summary.update_contraband(prediction.label)

    tracker = edgeiq.CorrelationTracker(
            max_objects=5,
            deregister_frames=30,
            enter_cb=handle_detected_contraband)

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:

            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()
                contraband_summary.update_image(frame)
                predictions = []

                # gather data from the all the detectors
                for i in range(0, len(detectors)):
                    results = detectors[i].detect_objects(
                        frame, confidence_level=.2)
                    filtered_predictions = edgeiq.filter_predictions_by_label(
                            results.predictions, contraband_labels)

                    # append each prediction
                    predictions.extend(filtered_predictions)

                tracked_contraband = tracker.update(predictions, frame)
                tracked_predictions = [prediction for (object_id, prediction) in tracked_contraband.items()]

                # mark up the frame with the predictions for the contraband objects
                frame = edgeiq.markup_image(
                        frame, tracked_predictions, show_labels=True,
                        show_confidences=False, colors=obj_detect.colors)

                # send the collection of contraband detection points (string and video frame) to the streamer
                text = contraband_summary.get_contraband_string()

                streamer.send_data(frame, text)
                fps.update()

                if streamer.check_exit():
                    break

    finally:
        fps.stop()
        print("Contraband Summary:\n{}".format(contraband_summary.get_summary()))
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))
        print("Program Ending")


if __name__ == "__main__":
    main()
