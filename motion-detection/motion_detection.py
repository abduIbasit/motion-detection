import cv2
import imutils
import datetime
import time

def main(video_source=0, min_area=500, num_frames=20):
    vs = cv2.VideoCapture(video_source)
    time.sleep(2.0)

    frame_buffer = []

    # Initialize the background subtractor
    back_sub = cv2.createBackgroundSubtractorMOG2()

    while True:
        _, frame = vs.read()
        if frame is None:
            break

        frame = imutils.resize(frame, width=500)

        if len(frame_buffer) < num_frames:
            frame_buffer.append(frame)
            continue
        else:
            frame_buffer.pop(0)
            frame_buffer.append(frame)

        # Compute the average frame
        averaged_frame = cv2.addWeighted(frame_buffer[-1], 0.5, frame_buffer[0], 0.5, 0)

        # Apply the background subtractor to get the foreground mask
        fg_mask = back_sub.apply(frame)

        # Apply some morphological operations to remove noise and fill gaps
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

        # Find the contours of the foreground regions
        contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) < min_area:
                continue

            (x, y, w, h) = cv2.boundingRect(contour)

            # Filter contours based on aspect ratio
            aspect_ratio = float(w) / h
            if 0.2 < aspect_ratio < 2.5:  # Adjust these values based on your scenario
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion_detected = True

        text = "MOTION DETECTED!" if motion_detected else "NO MOTION"

        cv2.putText(frame, "STATUS: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # Change text color to red
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        cv2.imshow("Motion Detection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    vs.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(video_source=0, min_area=500, num_frames=20)






# import imutils
# from imutils.video import VideoStream
# import argparse
# import datetime
# import time
# import cv2

# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
# ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
# ap.add_argument("-n", "--num-frames", type=int, default=20, help="number of frames for rolling average")
# args = vars(ap.parse_args())

# vs = VideoStream(src=0).start()
# time.sleep(2.0)

# # Initialize frames buffer for rolling average
# frame_buffer = []

# while True:
#     frame = vs.read()
#     frame = frame if args.get("video", None) is None else frame[1]
#     text = "STATIONARY"

#     if frame is None:
#         break

#     frame = imutils.resize(frame, width=500)

#     # Update the frame buffer
#     if len(frame_buffer) < args["num_frames"]:
#         frame_buffer.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
#         continue
#     else:
#         frame_buffer.pop(0)
#         frame_buffer.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

#     # Compute the average frame
#     averaged_frame = cv2.addWeighted(frame_buffer[-1], 0.5, frame_buffer[0], 0.5, 0)

#     frameDelta = cv2.absdiff(averaged_frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
#     thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

#     thresh = cv2.dilate(thresh, None, iterations=2)
#     cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = imutils.grab_contours(cnts)

#     for c in cnts:
#         if cv2.contourArea(c) < args["min_area"]:
#             continue

#         (x, y, w, h) = cv2.boundingRect(c)
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         text = "MOTION!"

#     # print("Text:", text)  # Add print statement to check the text value
#     # print("Timestamp:", datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"))

#     cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#     cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
#                 (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

#     # Convert grayscale images to BGR for better visualization
#     thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
#     frameDelta_bgr = cv2.cvtColor(frameDelta, cv2.COLOR_GRAY2BGR)

#     cv2.imshow("Security Feed", frame)
#     cv2.imshow("Thresh", thresh_bgr)
#     cv2.imshow("Frame Delta", frameDelta_bgr)

#     # print("Press any key to continue...")
#     # cv2.waitKey(0)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord("q"):
#         break

# vs.stop() if args.get("video", None) is None else vs.release()
# cv2.destroyAllWindows()




# # import the necessary packages
# import imutils
# from imutils.video import VideoStream
# import argparse
# import datetime
# import time
# import cv2
# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
# ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
# args = vars(ap.parse_args())
# # if the video argument is None, then we are reading from webcam
# if args.get("video", None) is None:
# 	vs = VideoStream(src=0).start()
# 	time.sleep(2.0)
# # otherwise, we are reading from a video file
# else:
# 	vs = cv2.VideoCapture(args["video"])
# # initialize the first frame in the video stream
# firstFrame = None

# # loop over the frames of the video
# while True:
# 	# grab the current frame and initialize the occupied/unoccupied
# 	# text
# 	frame = vs.read()
# 	frame = frame if args.get("video", None) is None else frame[1]
# 	text = "STATIONARY"
# 	# if the frame could not be grabbed, then we have reached the end
# 	# of the video
# 	if frame is None:
# 		break
# 	# resize the frame, convert it to grayscale, and blur it
# 	frame = imutils.resize(frame, width=500)
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	gray = cv2.GaussianBlur(gray, (21, 21), 0)
# 	# if the first frame is None, initialize it
# 	if firstFrame is None:
# 		firstFrame = gray
# 		continue

# 	# compute the absolute difference between the current frame and
# 	# first frame
# 	frameDelta = cv2.absdiff(firstFrame, gray)
# 	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
# 	# dilate the thresholded image to fill in holes, then find contours
# 	# on thresholded image
# 	thresh = cv2.dilate(thresh, None, iterations=2)
# 	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
# 		cv2.CHAIN_APPROX_SIMPLE)
# 	cnts = imutils.grab_contours(cnts)
# 	# loop over the contours
# 	for c in cnts:
# 		# if the contour is too small, ignore it
# 		if cv2.contourArea(c) < args["min_area"]:
# 			continue
# 		# compute the bounding box for the contour, draw it on the frame,
# 		# and update the text
# 		(x, y, w, h) = cv2.boundingRect(c)
# 		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
# 		text = "MOTION!"

# 		# draw the text and timestamp on the frame
# 		cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
# 			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
# 		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
# 			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
# 		# show the frame and record if the user presses a key
# 		cv2.imshow("Security Feed", frame)
# 		cv2.imshow("Thresh", thresh)
# 		cv2.imshow("Frame Delta", frameDelta)
# 		key = cv2.waitKey(1) & 0xFF
# 		# if the `q` key is pressed, break from the lop
# 		if key == ord("q"):
# 			break

# # cleanup the camera and close any open windows
# vs.stop() if args.get("video", None) is None else vs.release()
# cv2.destroyAllWindows()