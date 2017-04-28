Descriptions
============
This is a short overview of the used naming conventions. For a more detailed discussion check out for example the paper :cite:`ward2011performance`.


Ground truth events: actual events, annotations

Detected events:

Standard scores
---------------
Can be defined on a frame-by-frame basis, each sample:
True positives
False positives
False negatives
True negatives

Segmentation - segments are where a score doesn't change over the frames - assign standard score to the segments

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
C - Correct
F - fragmented: ...
M - merged: ...
FM - fragmented and merged: ...
D - deletion: ... practically equivalent of a false negative ground truth event

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
