import cv2
import os

class FaceDetect():
    def run(self, input_img):
        # Get user supplied values
        dir_path = os.path.dirname(os.path.realpath(__file__))
        casaPath = os.path.join(dir_path, "haarcascade_frontalface_default.xml")

        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(casaPath)

        # Read the image
        image = cv2.imread(input_img)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )

        faceNum = len(faces)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        name, type = os.path.splitext(input_img)
        output_img = name + '_faces' + type
        cv2.imwrite(output_img, image)

        return [faceNum, output_img]
