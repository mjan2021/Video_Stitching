# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
import numpy as np
import imutils

class Stitcher:
    def __init__(self):
        # determine if we are using OpenCV v3.X and initialize the
        # cached homography matrix
        # self.isv3 = imutils.is_cv3()
        self.cachedH = None

    def detectAndDescribe(self, image):
        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # check to see if we are using OpenCV 3.X
        if self.isv3:
            # detect and extract features from the image
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(image, None)
        # otherwise, we are using OpenCV 2.4.X
        else:
            # detect keypoints in the image
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)
            # extract features from the image
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)
        # convert the keypoints from KeyPoint objects to NumPy
        # arrays
        kps = np.float32([kp.pt for kp in kps])
        # return a tuple of keypoints and features
        return (kps, features)

    def stitch(self, images, ratio=0.75, reprojThresh=4.0):
        # unpack the images
        (imageB, imageA) = images
        # if the cached homography matrix is None, then we need to
        # apply keypoint matching to construct it
        if self.cachedH is None:
            # detect keypoints and extract
            (kpsA, featuresA) = self.detectAndDescribe(imageA)
            (kpsB, featuresB) = self.detectAndDescribe(imageB)
            # match features between the two images
            M = self.matchKeypoints(kpsA, kpsB,
                                    featuresA, featuresB, ratio, reprojThresh)
            # if the match is None, then there aren't enough matched
            # keypoints to create a panorama
            if M is None:
                return None
            # cache the homography matrix
            self.cachedH = M[1]
        # apply a perspective transform to stitch the images together
        # using the cached homography matrix
        result = cv2.warpPerspective(imageA, self.cachedH,
                                     (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
        # return the stitched image
        return result

def print_hi(name):

    img1 = cv2.imread('img1.jpg')
    img2 = cv2.imread('img2.jpg')

    print(f'Img1: {img1.shape}, img2: {img2.shape}')
    dim = (img1.shape[0], img1.shape[1])
    # left = cv2.imread('Left.jpg', cv2.IMREAD_COLOR)
    img1 = cv2.resize(img1, (1024, 768), interpolation=cv2.INTER_AREA)  # ReSize to (1024,768)
    # right = cv2.imread('Right.jpg', cv2.IMREAD_COLOR)
    img2 = cv2.resize(img2, (1024, 768), interpolation=cv2.INTER_AREA)  # ReSize to (1024,768)

    print(f'Resized::Img1: {img1.shape}, img2: {img2.shape}')
    images = []
    images.append(img1)
    images.append(img2)

    print(f'Image Shapes Appended: {np.asarray(images).shape}')
    # stitcher = cv2.createStitcher()
    stitcher = cv2.Stitcher_create()
    (ret, pano) = stitcher.stitch(images)

    # result = stitch(images=images)
    print(f'Type Pano: {type(pano)}')
    cv2.imshow('Panorama', pano)
    cv2.waitkey(0)
    # print(pano)
    if ret == cv2.STITCHER_OK:
        cv2.imshow('Panorama', pano)
        cv2.waitKey()
        cv2.destroyAllWindows()
    else:
        print("Error during Stitching")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/