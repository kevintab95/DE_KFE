import cv2

# Write location for the extracted webcam feed.
# NOTE: '_' is included because of the naming convention
# used for the images eg. _20.jpg, _21.jpg etc...
WRITE_BUFFER_LOCATION = "/path/to/location/_"

NUMBER_OF_FRAMES = 300

cap = cv2.VideoCapture(0)
# Capture first frame.
ret0, frame0 = cap.read()
init_gray = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
cv2.imwrite(WRITE_BUFFER_LOCATION + str(0) + ".jpg", init_gray)
i = 1

for j in range(0, NUMBER_OF_FRAMES):
    # Capture second frame.
    ret, frame1 = cap.read()

    # Convert frames to grayscale. (ie. previous and current frames)
    gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # Display the current frame.
    cv2.imshow('frame1',gray1)
    cv2.imwrite(WRITE_BUFFER_LOCATION + str(i) + ".jpg", gray1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Set previous frame.
    ret0, frame0 = cap.read()
    i += 1

# When everything done, release the capture

cap.release()
cv2.destroyAllWindows()

