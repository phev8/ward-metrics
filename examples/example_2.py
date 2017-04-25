from core_methods import eval_events
from visualisations import *

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


gt_event_scores, det_event_scores = eval_events(ground_truth_test, detection_test, 3, 260)
plot_events_with_event_scores(gt_event_scores, det_event_scores, ground_truth_test, detection_test)