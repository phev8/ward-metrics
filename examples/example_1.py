from core_methods import ward_eval
from visualisations import plot_segment_results

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

total_results, segments_results = ward_eval(ground_truth_test, detection_test, eval_start, eval_end)

plot_segment_results(segments_results, ground_truth_test, detection_test)