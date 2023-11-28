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
