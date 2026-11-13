import unittest
from src.features import eye_aspect_ratio,mouth_aspect_ratio
class FeatureTests(unittest.TestCase):
    def test_ear_positive(self):
        pts=[(0,5),(2,2),(4,2),(6,5),(4,8),(2,8)]
        self.assertGreater(eye_aspect_ratio(pts),0)
    def test_closed_eye_has_lower_ear(self):
        opened=[(0,5),(2,2),(4,2),(6,5),(4,8),(2,8)]
        closed=[(0,5),(2,4.8),(4,4.8),(6,5),(4,5.2),(2,5.2)]
        self.assertLess(eye_aspect_ratio(closed),eye_aspect_ratio(opened))
    def test_mar_positive(self):
        self.assertGreater(mouth_aspect_ratio((0,2),(0,8),(-5,5),(5,5)),0)
if __name__=="__main__": unittest.main()
