import cv2

# Start capturing video from the camera
cap = cv2.VideoCapture(0)  # 0 is typically the device index for the first cameral

width = 640; height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/pi/output.avi', fourcc, 20.0, (width, height))

if not cap.isOpened():
    print("Cannot open camera")
    exit()

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Write the flipped frame
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
finally:
    # When everything done, release the capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()