import wardmetrics
from wardmetrics.core_methods import eval_events
from wardmetrics.utils import *
from wardmetrics.visualisations import *

ground_truth_test = [
    (40, 60),
    (73, 75),
    (90, 100),
    (125, 135),
    (150, 157),
    (190, 215),
    (220, 230),
    (235, 250),
]

detection_test = [
    (10, 20),
    (45, 52),
    (70, 80),
    (120, 180),
    (195, 200),
    (207, 213),
    (221, 237),
    (239, 243),
    (245, 250),
]

print("Using version",  wardmetrics.__version__)

# Run event-based evaluation:
gt_event_scores, det_event_scores, detailed_scores, standard_scores = eval_events(ground_truth_test, detection_test)

# Print results:
print_standard_event_metrics(standard_scores)
print_detailed_event_metrics(detailed_scores)

# Access results in other formats:
print(standard_event_metrics_to_list(standard_scores)) # standard scores as basic python list, order: p, r, p_w, r_w
print(standard_event_metrics_to_string(standard_scores)) # standard scores as string line, order: p, r, p_w, r_w)
print(standard_event_metrics_to_string(standard_scores, separator=";", prefix="(", suffix=")\n")) # standard scores as string line, order: p, r, p_w, r_w

print(detailed_event_metrics_to_list(detailed_scores)) # detailed scores as basic python list
print(detailed_event_metrics_to_string(detailed_scores)) # detailed scores as string line
print(detailed_event_metrics_to_string(detailed_scores, separator=";", prefix="(", suffix=")\n")) # standard scores as string line


# Show results:
plot_events_with_event_scores(gt_event_scores, det_event_scores, ground_truth_test, detection_test, show=False)
plot_event_analysis_diagram(detailed_scores)