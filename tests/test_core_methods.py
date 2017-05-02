import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from wardmetrics.core_methods import *
import unittest


class TestCoreMethods(unittest.TestCase):
    ground_truth_events_0 = []
    ground_truth_events_1 = []
    ground_truth_events_2 = []
    ground_truth_events_3 = []

    detected_events_0 = []
    detected_events_1 = []
    detected_events_2 = []
    detected_events_3 = []

    def test_is_segment_in_interval(self):
        self.assertTrue(is_segment_in_interval(0, 10, -5, 20))
        self.assertFalse(is_segment_in_interval(0, 10, -5, -1))
        self.assertFalse(is_segment_in_interval(0, 10, 11, 15))
        self.assertFalse(is_segment_in_interval(0, 10, 10, 15))
        self.assertFalse(is_segment_in_interval(0, 10, -10, 0))
        self.assertFalse(is_segment_in_interval(0, 10, 1, 9))

    #def test_get_standard_category_for_segment(self):
    #    # TODO
    #    pass

    def test_score_segment(self):
        TP_segment = (0, 0, 0, 0, "TP")
        FP_segment = (0, 0, 0, 0, "FP")
        TN_segment = (0, 0, 0, 0, "TN")
        FN_segment = (0, 0, 0, 0, "FN")

        self.assertRaises(ValueError, score_segment, None, None, None)
        self.assertEqual(score_segment(TP_segment, TP_segment, TP_segment), "TP")
        self.assertEqual(score_segment(TN_segment, TN_segment, TN_segment), "TN")

        self.assertEqual(score_segment(FN_segment, FN_segment, FN_segment), "no score")
        self.assertEqual(score_segment(FN_segment, FN_segment, TP_segment), "no score")
        self.assertEqual(score_segment(FN_segment, FN_segment, FP_segment), "no score")
        self.assertEqual(score_segment(FN_segment, FN_segment, TN_segment), "no score")
        self.assertEqual(score_segment(TP_segment, FN_segment, FN_segment), "no score")
        self.assertEqual(score_segment(FP_segment, FN_segment, FN_segment), "no score")
        self.assertEqual(score_segment(TN_segment, FN_segment, FN_segment), "no score")

        self.assertEqual(score_segment(FP_segment, FP_segment, FP_segment), "no score")
        self.assertEqual(score_segment(FP_segment, FP_segment, FN_segment), "no score")
        self.assertEqual(score_segment(FP_segment, FP_segment, TP_segment), "no score")
        self.assertEqual(score_segment(FP_segment, FP_segment, TN_segment), "no score")
        self.assertEqual(score_segment(TP_segment, FP_segment, FP_segment), "no score")
        self.assertEqual(score_segment(FN_segment, FP_segment, FP_segment), "no score")
        self.assertEqual(score_segment(TN_segment, FP_segment, FP_segment), "no score")

        self.assertEqual(score_segment(TN_segment, FN_segment, TN_segment), "D")
        self.assertEqual(score_segment(FP_segment, FN_segment, TN_segment), "D")
        self.assertEqual(score_segment(TN_segment, FN_segment, FP_segment), "D")
        self.assertEqual(score_segment(FP_segment, FN_segment, FP_segment), "D")
        self.assertEqual(score_segment(None, FN_segment, FP_segment), "D")
        self.assertEqual(score_segment(None, FN_segment, TN_segment), "D")
        self.assertEqual(score_segment(FP_segment, FN_segment, None), "D")
        self.assertEqual(score_segment(TN_segment, FN_segment, None), "D")

        self.assertEqual(score_segment(TN_segment, FP_segment, TN_segment), "I")
        self.assertEqual(score_segment(FN_segment, FP_segment, TN_segment), "I")
        self.assertEqual(score_segment(TN_segment, FP_segment, FN_segment), "I")
        self.assertEqual(score_segment(FN_segment, FP_segment, FN_segment), "I")
        self.assertEqual(score_segment(None, FP_segment, FN_segment), "I")
        self.assertEqual(score_segment(None, FP_segment, TN_segment), "I")
        self.assertEqual(score_segment(FN_segment, FP_segment, None), "I")
        self.assertEqual(score_segment(TN_segment, FP_segment, None), "I")

        self.assertEqual(score_segment(TP_segment, FN_segment, TP_segment), "F")

        self.assertEqual(score_segment(TP_segment, FP_segment, TP_segment), "M")

        self.assertEqual(score_segment(TN_segment, FP_segment, TP_segment), "Os")
        self.assertEqual(score_segment(FN_segment, FP_segment, TP_segment), "Os")
        self.assertEqual(score_segment(TP_segment, FP_segment, TN_segment), "Oe")
        self.assertEqual(score_segment(TP_segment, FP_segment, FN_segment), "Oe")
        self.assertEqual(score_segment(None, FP_segment, TP_segment), "Os")
        self.assertEqual(score_segment(TP_segment, FP_segment, None), "Oe")

        self.assertEqual(score_segment(TN_segment, FN_segment, TP_segment), "Us")
        self.assertEqual(score_segment(FP_segment, FN_segment, TP_segment), "Us")
        self.assertEqual(score_segment(TP_segment, FN_segment, TN_segment), "Ue")
        self.assertEqual(score_segment(TP_segment, FN_segment, FP_segment), "Ue")
        self.assertEqual(score_segment(None, FN_segment, TP_segment), "Us")
        self.assertEqual(score_segment(TP_segment, FN_segment, None), "Ue")


if __name__ == '__main__':
    unittest.main()
