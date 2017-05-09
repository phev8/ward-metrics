import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from wardmetrics.utils import *
import unittest


class TestUtils(unittest.TestCase):
    def test_standard_event_metrics_to_list(self):
        values = [0.1, 0.2, 0.3, 0.4]
        standard_metrics = {
            "precision": values[0],
            "recall": values[1],
            "precision (weighted)": values[2],
            "recall (weighted)": values[3]
        }

        self.assertEqual(standard_event_metrics_to_list(standard_metrics), values)
        values[2] = 0.5
        self.assertNotEqual(standard_event_metrics_to_list(standard_metrics), values)

    def test_standard_event_metrics_to_string(self):
        values = [0.1, 0.2, 0.3, 0.4]
        standard_metrics = {
            "precision": values[0],
            "recall": values[1],
            "precision (weighted)": values[2],
            "recall (weighted)": values[3]
        }
        result_1 = "[0.1, 0.2, 0.3, 0.4]"
        result_2 = "[0.1\t0.2\t0.3\t0.4]"
        result_3 = "0.1, 0.2, 0.3, 0.4"
        self.assertEqual(standard_event_metrics_to_string(standard_metrics), result_1)
        self.assertEqual(standard_event_metrics_to_string(standard_metrics, separator="\t"), result_2)
        self.assertEqual(standard_event_metrics_to_string(standard_metrics, prefix="", suffix=""), result_3)

    def test_detailed_event_metrics_to_list(self):
        values = [1, 2, 3, 4, 5, 6,  7, 8, 9, 10, 11]
        metrics = {
            "C": values[0], "D": values[1],
            "M": values[2], "F": values[3],
            "FM": values[4], "I'": values[8],
            "F'": values[5], "M'": values[6],
            "FM'": values[7], "total_gt": values[9],
            "total_det": values[10]
        }

        self.assertEqual(detailed_event_metrics_to_list(metrics), values)
        values[2] += 3
        self.assertNotEqual(detailed_event_metrics_to_list(metrics), values)

    def test_detailed_event_metrics_to_string(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        metrics = {
            "C": values[0], "D": values[1],
            "M": values[2], "F": values[3],
            "FM": values[4], "I'": values[8],
            "F'": values[5], "M'": values[6],
            "FM'": values[7], "total_gt": values[9],
            "total_det": values[10]
        }

        result_1 = "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]"
        result_2 = "[1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11]"
        result_3 = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"
        self.assertEqual(detailed_event_metrics_to_string(metrics), result_1)
        self.assertEqual(detailed_event_metrics_to_string(metrics, separator="\t"), result_2)
        self.assertEqual(detailed_event_metrics_to_string(metrics, prefix="", suffix=""), result_3)

    def test_detailed_segment_results_to_list(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        segment_counts = {
            "TP": values[0], "TN": values[1], "I": values[2], "D": values[3],
            "F": values[4], "M": values[5], "Os": values[6], "Oe": values[7],
            "Us": values[8], "Ue": values[9]
        }
        self.assertEqual(detailed_segment_results_to_list(segment_counts), values)
        values[2] += 3
        self.assertNotEqual(detailed_segment_results_to_list(segment_counts), values)

    def test_detailed_segment_results_to_string(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        segment_counts = {
            "TP": values[0], "TN": values[1], "I": values[2], "D": values[3],
            "F": values[4], "M": values[5], "Os": values[6], "Oe": values[7],
            "Us": values[8], "Ue": values[9]
        }

        result_1 = "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
        result_2 = "[1\t2\t3\t4\t5\t6\t7\t8\t9\t10]"
        result_3 = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
        self.assertEqual(detailed_segment_results_to_string(segment_counts), result_1)
        self.assertEqual(detailed_segment_results_to_string(segment_counts, separator="\t"), result_2)
        self.assertEqual(detailed_segment_results_to_string(segment_counts, prefix="", suffix=""), result_3)

    def test_twoset_segment_metrics_to_list(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        twoset_metrics = {
            "tpr": values[0], "dr": values[1], "fr": values[2], "us": values[3], "ue": values[4],
            "fpr": 1-values[5], "ir": values[6], "mr": values[7], "os": values[8], "oe": values[9]
        }

        self.assertEqual(twoset_segment_metrics_to_list(twoset_metrics), values)
        values[2] += 3
        self.assertNotEqual(twoset_segment_metrics_to_list(twoset_metrics), values)

    def test_twoset_segment_metrics_to_string(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        twoset_metrics = {
            "tpr": values[0], "dr": values[1], "fr": values[2], "us": values[3], "ue": values[4],
            "fpr": 1 - values[5], "ir": values[6], "mr": values[7], "os": values[8], "oe": values[9]
        }

        result_1 = "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
        result_2 = "[1\t2\t3\t4\t5\t6\t7\t8\t9\t10]"
        result_3 = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
        self.assertEqual(twoset_segment_metrics_to_string(twoset_metrics), result_1)
        self.assertEqual(twoset_segment_metrics_to_string(twoset_metrics, separator="\t"), result_2)
        self.assertEqual(twoset_segment_metrics_to_string(twoset_metrics, prefix="", suffix=""), result_3)

if __name__ == '__main__':
    unittest.main()
