from dataclasses import dataclass
from typing import Tuple

from wai.annotations.domain.image import Image


@dataclass
class YOLOObject:
    """
    Internal representation of a YOLO annotation.
    """
    class_index: int
    centre_x: float = None
    centre_y: float = None
    width: float = None
    height: float = None
    poly_x: list = None
    poly_y: list = None

    @classmethod
    def from_string(cls, string: str):
        """
        Attempts to parse the given string.

        :param string: the string to parse
        :type string: str
        :return: the YOLOObject or an exception if failed to parse
        :rtype: YOLOObject
        """
        parts = string.strip().split(" ")
        # bbox format: <index> <center_x> <center_y> <widht> <height>
        if len(parts) == 5:
            return cls(
                int(parts[0]),
                float(parts[1]),
                float(parts[2]),
                float(parts[3]),
                float(parts[4]),
                None,
                None,
            )
        # polygon format: <index> <x0> <y0> <x1> <y1> ...
        elif (len(parts) > 5) and (len(parts) % 2 == 1):
            px = []
            py = []
            for i in range(1, len(parts), 2):
                px.append(float(parts[i]))
                py.append(float(parts[i+1]))
            w = max(px) - min(px)
            h = max(py) - min(py)
            return cls(
                int(parts[0]),
                min(px) + w / 2,
                min(py) + h / 2,
                w,
                h,
                px,
                py,
            )
        else:
            raise Exception("Neither in bbox nor polygon format: %s" % string)

    def has_polygon(self):
        """
        Returns whether polygon information is present.

        :return: True if present
        :rtype: bool
        """
        return (self.poly_x is not None) and (self.poly_y is not None)

    def to_bbox(self):
        """
        Returns the bbox line representation.

        :return: the generated line representation
        :rtype: str
        """
        return f"{self.class_index} {self.centre_x} {self.centre_y} {self.width} {self.height}"

    def to_polygon(self):
        """
        Returns the polygon line representation.

        :return: the generated line representation
        :rtype: str
        """
        parts = ["%d" % self.class_index]
        if self.has_polygon():
            for i in range(len(self.poly_x)):
                parts.append("%f %f" % (self.poly_x[i], self.poly_y[i]))
        else:
            x = self.centre_x - self.width / 2
            y = self.centre_y - self.height / 2
            parts.append("%f %f" % (x, y))
            parts.append("%f %f" % (x + self.width, y))
            parts.append("%f %f" % (x + self.width, y + self.height))
            parts.append("%f %f" % (x, y + self.height))
        return " ".join(parts)

    def to_str(self, use_polygon):
        """
        Turns the data into a line representation.

        :param use_polygon: whether to use polygon format or bbox format
        :type use_polygon: bool
        :return: the generated line
        :rtype: str
        """
        if use_polygon:
            return self.to_polygon()
        else:
            return self.to_bbox()

    def __str__(self):
        """
        Returns the polygon representation if possible otherwise the bbox one.

        :return: the representation as singe line
        :rtype: str
        """
        if self.has_polygon():
            return self.to_polygon()
        else:
            return self.to_bbox()


YOLOODFormat = Tuple[Image, Tuple[YOLOObject]]
