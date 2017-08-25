import math
import cv2
import numpy as np
from DataModel.enums import Size


class SizeDetector:

    def __init__(self):
        self.horizontal_fov = None
        self.vertical_fov = None
        self.tiny_bounds = None
        self.small_bounds = None
        self.medium_bounds = None
        self.big_bounds = None

    def assume_size_from_contour(self, distance, contour, image_resolution):
        """
        Assumes width and height of object and discretizes its values
        :param distance: distance from objects scene - this value should be read from sensor
        :param contour: contour of object which size is calculated
        :param image_resolution: resolution of camera image
        :return: tuple representing discrete values of width and height of object
        """
        if distance is None or distance <= 0:
            return Size.NONE, Size.NONE
        box = cv2.minAreaRect(contour)
        box = cv2.boxPoints(box)
        box = np.int0(box)
        object_width_pixels = self._euclidean_distance(box[0], box[1])
        object_height_pixels = self._euclidean_distance(box[1], box[2])
        result = self.assume_size(distance, (object_width_pixels, object_height_pixels), image_resolution)
        return result

    def assume_size(self, distance, object_size_pixels, image_resolution):
        """
        Assumes width and height of object and discretizes its values
        :param distance: distance from objects scene - this value should be read from sensor
        :param object_size_pixels: tuple representing width and height of object in pixels
        :param image_resolution: resolution of camera image
        :return: tuple representing discrete values of width and height of object
        """

        horizontal_ratio = self._calculate_pixel_per_metrics_ratio(distance, image_resolution[0], self.horizontal_fov)
        vertical_ratio = self._calculate_pixel_per_metrics_ratio(distance, image_resolution[1], self.vertical_fov)

        real_width = object_size_pixels[0] * horizontal_ratio
        real_height = object_size_pixels[1] * vertical_ratio

        discrete_width = self._size_discretization(real_width)
        discrete_height = self._size_discretization(real_height)

        return discrete_width, discrete_height

    @staticmethod
    def _calculate_pixel_per_metrics_ratio(real_distance, resolution, fov):
        """
        Calculates pixel per metric ration
        :param real_distance: distance from objects scene - this value should be read from sensor
        :param resolution: resolution of camera image
        :param fov: camera field of view
        :return: pixel per metric ration
        """
        image_length_in_metrics = 2 * real_distance * math.sin(math.radians(fov / 2))
        return image_length_in_metrics / resolution

    def _size_discretization(self, size):
        """
        Converts continuous values of size to discrete values
        :param size: continuous value of size
        :return: discrete value of size
        """

        if size is None:
            return Size.NONE
        if self.tiny_bounds[0] < size <= self.tiny_bounds[1]:
            return Size.TINY
        if self.small_bounds[0] < size <= self.small_bounds[1]:
            return Size.SMALL
        if self.medium_bounds[0] < size <= self.medium_bounds[1]:
            return Size.MEDIUM
        if self.big_bounds[0] < size <= self.big_bounds[1]:
            return Size.BIG
        if size > self.big_bounds[1]:
            return Size.LARGE

    @staticmethod
    def _euclidean_distance(p_1, p_2):
        """
        Calculates euclidean distance between two points
        :param p_1: tuple with two members representing first point
        :param p_2: tuple with two members representing second point
        :return: euclidean distance of two given points
        """
        return math.sqrt(math.pow(p_1[0] - p_2[0], 2) + math.pow(p_1[1] - p_2[1], 2))
