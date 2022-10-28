'''
This program will use a camera to read QR codes and export the QR code data to the clipboard.
It relies on the opencv module.
We tested it using a raspberry pi 4 with a ArduCam.

Opens a display window showing the camara view and overlays the the QR data
as well as bounding box. Also, when detected, messages are printed out.


INPUT: hold a QR code in front of camera.
OUTPUT: data gets copied to the clipboard.

https://docs.opencv.org/4.x/de/dc3/classcv_1_1QRCodeDetector.html
'''
import cv2
import pyperclip

# set up camera object
cap = cv2.VideoCapture(0)

# QR code detection object
detector = cv2.QRCodeDetector()

while True:
    # get the image
    _, img = cap.read()
    
    # get bounding box coords and data
    '''
    cv.QRCodeDetector.detectAndDecode(img[, points[, straight_qrcode]])
        -> retval, points, straight_qrcode
     img: grayscale or color (BGR) image containing QR code.
     points: optional output array of vertices of the found QR code quadrangle. Will be
             empty if not found.
     straight_qrcode: The optional output image containing rectified and binarized QR code
    '''
    data, bbox, _ = detector.detectAndDecode(img)
    
    # if there is a bounding box, draw one, along with the data

    if(bbox is not None):
        print('QR CODE FOUND! ')
        print('bbox count: ', len(bbox))
        if data:
            print("data found: ", data)
            pyperclip.copy(data) # copy to clipboard
        else:
            data = 'NO DATA'
        print(bbox)
    
        for i in range(4):
            curx = int(bbox[0][i][0])
            cury = int(bbox[0][i][1])
            nextx = int(bbox[0][(i+1) % 4][0])
            nexty = int(bbox[0][(i+1) % 4][1])
            
            cv2.line(img,
                     (curx,cury), 
                     (nextx,nexty),
                     color=(255,0, 255), thickness=2)

            printx = int(bbox[0][0][0])
            printy = int(bbox[0][0][1])
        cv2.putText(img,
                    data,
                    (printx, printy  - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                     (0, 255, 0),
                    2)
    # display the image preview
    cv2.imshow("code detector", img)
    if(cv2.waitKey(1) == ord("q")):
        break
# free camera  object and exit
cap.release()
cv2.destroyAllWindows()
