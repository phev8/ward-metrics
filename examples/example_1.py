from core_methods import eval_segment_results
from visualisations import plot_segment_results, plot_segment_statistics

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

segments_results, segment_statistics, normed_segment_statistics = eval_segment_results(ground_truth_test, detection_test, eval_start, eval_end)

print(segment_statistics)
print(normed_segment_statistics)

plot_segment_results(segments_results, ground_truth_test, detection_test)
plot_segment_statistics(segment_statistics)
