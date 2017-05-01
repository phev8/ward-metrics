Descriptions
============
This is a short overview of the used naming conventions. For a more detailed discussion check out for example the paper :cite:`ward2011performance`.

Ground truth events:
    actual events that were annotated and will be considered as true instancies of an activity. However depending on the annotation quality they are not always 100% true.

Detected events:
    predicted events - typically results of a classifier's prediction step

Standard scores
---------------
Can be defined on a frame-by-frame basis. To calculate score values each frame is categorized with one of the following score labels:

True positives:
    ground truth label for the current frame or segment equals the detected (predicted) label

False positives:
    current frame or segment has a detected label for a particular class however the ground truth indicates that this class is not active

False negatives:
    todo

True negatives:
    todo

Segmentation - segments are where a score doesn't change over the frames - assign standard score to the segments

Precision:
    todo

Recall:
    todo

Calculation of event-based precision and recall
...............................................
Assumption for True positive events
False positive
False negatives

TP_det, FP_det
todo: add formula

Problem: nature of the error is not well described on event basis

Detailed scores
---------------
Detailed scores for ground truth events
.......................................
C - Correct:
    todo

F - fragmented:
    todo

M - merged:
    todo

FM - fragmented and merged:
    todo

D - deletion:
    todo practically equivalent of a false negative ground truth event

Detailed scores for detection events
....................................
C - Correct
F' - fragmenting: ...
M' - merging: ...
FM' - fragmenting and merging: ...
I' - insertion: ... basically equivalent of a false positive detection event

Detailed scores for segments
............................
Assigned categories for segments:

Segment based metrics (2SET-metrics):
