''' Prosze mi tego pliku nie zmieniac ~ Kucu, 2017 '''

import cv2
import cv2
#import Agent.database as db
from ImageProcessing.ObjectDetector import ObjectDetector
from DataModel.enums import Color
import ImageProcessing.parameters_loader as loader



cam = cv2.VideoCapture(0)
print cam.get(cv2.CAP_PROP_POS_FRAMES)

od = ObjectDetector()
loader.load_all_from_file(od)
for i in range(20):
    cam.read()

while True:
    images = []
    _, im = cam.read()
    #for i in range(1,10):
        #_, im = cam.read()
        #images.append(im)
    #im = pt.merge_pictures(images, ColorSpace.BGR, True)

    print 'start'
    x = od.detect_objects(im, None, False)
    print 'end'

    for obj in x:
        print obj.to_string()

    print ' '
    print ' '
    for single_contour in od.detected_contours:
        draw_color = (0, 0, 0)
        if single_contour[0] is Color.RED:
            draw_color = (0, 0, 255)
        elif single_contour[0] is Color.YELLOW:
            draw_color = (40, 244, 255)
        elif single_contour[0] is Color.GREEN:
            draw_color = (0, 255, 0)
        elif single_contour[0] is Color.BLUE:
            draw_color = (255, 0, 0)
        elif single_contour[0] is Color.VIOLET:
            draw_color = (188, 0, 105)
        cv2.drawContours(im, [single_contour[1]], -1, draw_color, 2)
    od.clear_contours()
    cv2.imshow('detected_objects', im)
    cv2.waitKey(1)





