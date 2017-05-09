from wardmetrics.core_methods import eval_segments
from wardmetrics.visualisations import *
from wardmetrics.utils import *

ground_truth_test = [
    (40, 60),
    (70, 75),
    (90, 100),
    (125, 135),
    (150, 157),
    (187, 220),
]

detection_test = [
    (10, 20),
    (45, 52),
    (65, 80),
    (120, 180),
    (195, 200),
    (207, 213),
]

eval_start = 2
eval_end = 241

# Calculate segment results:
twoset_results, segments_with_scores, segment_counts, normed_segment_counts = eval_segments(ground_truth_test, detection_test, eval_start, eval_end)

# Print results:
print_detailed_segment_results(segment_counts)
print_detailed_segment_results(normed_segment_counts)
print_twoset_segment_metrics(twoset_results)

# Access segment results in other formats:
print("\nAbsolute values:")
print("----------------")
print(detailed_segment_results_to_list(segment_counts)) # segment scores as basic python list
print(detailed_segment_results_to_string(segment_counts)) # segment scores as string line
print(detailed_segment_results_to_string(segment_counts, separator=";", prefix="(", suffix=")\n")) # segment scores as string line

print("Normed values:")
print("--------------")
print(detailed_segment_results_to_list(normed_segment_counts)) # segment scores as basic python list
print(detailed_segment_results_to_string(normed_segment_counts)) # segment scores as string line
print(detailed_segment_results_to_string(normed_segment_counts, separator=";", prefix="(", suffix=")\n")) # segment scores as string line

# Access segment metrics in other formats:
print("2SET metrics:")
print("-------------")
print(twoset_segment_metrics_to_list(twoset_results)) # twoset_results as basic python list
print(twoset_segment_metrics_to_string(twoset_results)) # twoset_results as string line
print(twoset_segment_metrics_to_string(twoset_results, separator=";", prefix="(", suffix=")\n")) # twoset_results as string line

# Visualisations:
plot_events_with_segment_scores(segments_with_scores, ground_truth_test, detection_test)
plot_segment_counts(segment_counts)
plot_twoset_metrics(twoset_results)