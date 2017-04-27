import wardmetrics
from wardmetrics.core_methods import eval_events
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
    (275, 292),
    (340, 368),
    (389, 410),
    (455, 468),
    (487, 512),
    (532, 546),
    (550, 568),
    (583, 612),
    (632, 645),
    (655, 690),
    (710, 754),
    (763, 785),
    (791, 812),
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

gt_event_scores, det_event_scores, detailed_scores, standard_scores = eval_events(ground_truth_test, detection_test)

print(standard_scores)

plot_events_with_event_scores(gt_event_scores, det_event_scores, ground_truth_test, detection_test, show=False)

plot_event_analysis_diagram(detailed_scores, fontsize=8, use_percentage=True)
#plot_event_analysis_diagram(results)