from wardmetrics.core_methods import eval_segment_results
from wardmetrics.visualisations import *

ground_truth_test = [
    (40, 60),
    (73, 75),
    (90, 100),
    (125, 135),
    (150, 157),
    (190, 215),
]

detection_test = [
    (10, 20),
    (45, 52),
    (70, 80),
    (120, 180),
    (195, 200),
    (207, 213),
]

eval_start = 2
eval_end = 241

frame_statistics, segments_results, segment_counts, normed_segment_counts = eval_segment_results(ground_truth_test, detection_test, eval_start, eval_end)

plot_events_with_segment_scores(segments_results, ground_truth_test, detection_test)
plot_segment_counts(segment_counts)
plot_twoset_metrics(frame_statistics)