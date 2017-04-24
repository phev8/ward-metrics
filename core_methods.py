

def is_segment_in_interval(segment_start, segment_end, interval_start, interval_end):
    if interval_start <= segment_start and segment_end <= interval_end:
        return True
    return False


def get_standard_category_for_segment(segment_start, segment_end, ground_truth, detected_events):
    """
    Return standard category for a single segment
    :param segment_start:
    :param segment_end:
    :param ground_truth:
    :param detected_events:
    :return: "TP", "FP", "FN", "TN"
    """
    is_part_of_ground_truth = False
    is_part_of_detection = False

    for gt in ground_truth:
        if is_segment_in_interval(segment_start, segment_end, gt[0], gt[1]):
            is_part_of_ground_truth = True
            break

    for det in detected_events:
        if is_segment_in_interval(segment_start, segment_end, det[0], det[1]):
            is_part_of_detection = True
            break

    # decide which category
    if is_part_of_ground_truth:
        if is_part_of_detection:
            category = "TP"
        else:
            category = "FN"
    else:
        if is_part_of_detection:
            category = "FP"
        else:
            category = "TN"

    return category, is_part_of_ground_truth, is_part_of_detection


def get_segments_with_standard_error_categories(ground_truth_events, detected_events, evaluation_start=None, evaluation_end=None):
    segments = []

    gt_index = 0
    det_index = 0
    last_segment = None

    # TODO: handle if no gt or no det
    # TODO: handle events with zero length

    while True:
        if gt_index >= len(ground_truth_events):
            if det_index >= len(detected_events):
                if evaluation_end is not None:
                    category, is_gt, is_det = get_standard_category_for_segment(last_segment[1], evaluation_end, ground_truth_events, detected_events)
                    if is_gt:
                        gt_i = gt_index
                    else:
                        gt_i = -1
                    if is_det:
                        det_i = det_index
                    else:
                        det_i = -1
                    last_segment = (last_segment[1], evaluation_end, gt_i, det_i, category)
                    segments.append(last_segment)
                break
        elif det_index >= len(detected_events):
            det_index = len(detected_events) - 1

        gt_start = ground_truth_events[gt_index][0]
        gt_end = ground_truth_events[gt_index][1]
        d_start = detected_events[det_index][0]
        d_end = detected_events[det_index][1]

        if last_segment is not None:
            seg_start = last_segment[1]

            values_to_consider = []
            if gt_start > seg_start:
                values_to_consider.append(gt_start)
            if d_start > seg_start:
                values_to_consider.append(d_start)
            if d_end > seg_start:
                values_to_consider.append(d_end)
            if gt_end > seg_start:
                values_to_consider.append(gt_end)
            seg_end = min(values_to_consider)

            category, is_gt, is_det = get_standard_category_for_segment(seg_start, seg_end, ground_truth_events, detected_events)
            if is_gt:
                gt_i = gt_index
            else:
                gt_i = -1
            if is_det:
                det_i = det_index
            else:
                det_i = -1

            last_segment = (seg_start, seg_end, gt_i, det_i, category)
            segments.append(last_segment)
        else:
            # Create first segment:
            if evaluation_start is None:
                seg_start = min(gt_start, d_start)
                seg_end = min(gt_end, d_end)
            else:
                seg_start = evaluation_start
                seg_end = min(gt_start, d_start)

            category, is_gt, is_det = get_standard_category_for_segment(seg_start, seg_end, ground_truth_events,
                                                                        detected_events)
            if is_gt:
                gt_i = gt_index
            else:
                gt_i = -1
            if is_det:
                det_i = det_index
            else:
                det_i = -1
            last_segment = (seg_start, seg_end, gt_i, det_i, category)
            segments.append(last_segment)

        if seg_end >= d_end:
            det_index += 1
        if seg_end >= gt_end:
            gt_index += 1

    return segments


def score_segment(previous_segment, current_segment, next_segment):
    if current_segment is None:
        raise ValueError("current_segment must not be None.")
    index_of_standard_category = 4
    current_segment_score = "no score"

    if current_segment[index_of_standard_category] == "TP":
        current_segment_score = "TP"
    elif current_segment[index_of_standard_category] == "TN":
        current_segment_score = "TN"
    else:
        # Handle error categories:
        if previous_segment is not None and next_segment is not None:
            # normal case (in the middle):
            if current_segment[index_of_standard_category] == "FP":
                if (previous_segment[index_of_standard_category] == "TN" or previous_segment[index_of_standard_category] == "FN") and \
                        (next_segment[index_of_standard_category] == "TN" or next_segment[index_of_standard_category] == "FN"):
                    current_segment_score = "I"
                elif previous_segment[index_of_standard_category] == "TP" and next_segment[index_of_standard_category] == "TP":
                    current_segment_score = "M"
                elif (previous_segment[index_of_standard_category] == "TN" or previous_segment[index_of_standard_category] == "FN") and \
                                next_segment[index_of_standard_category] == "TP":
                    current_segment_score = "Os"
                elif previous_segment[index_of_standard_category] == "TP" and (
                        next_segment[index_of_standard_category] == "TN" or next_segment[index_of_standard_category] == "FN"):
                    current_segment_score = "Oe"
            elif current_segment[index_of_standard_category] == "FN":
                if (previous_segment[index_of_standard_category] == "TN" or previous_segment[index_of_standard_category] == "FP") and (
                        next_segment[index_of_standard_category] == "TN" or next_segment[index_of_standard_category] == "FP"):
                    current_segment_score = "D"
                elif previous_segment[index_of_standard_category] == "TP" and next_segment[index_of_standard_category] == "TP":
                    current_segment_score = "F"
                elif (previous_segment[index_of_standard_category] == "TN" or previous_segment[index_of_standard_category] == "FP") and \
                                next_segment[index_of_standard_category] == "TP":
                    current_segment_score = "Us"
                elif previous_segment[index_of_standard_category] == "TP" and (
                        next_segment[index_of_standard_category] == "TN" or next_segment[index_of_standard_category] == "FP"):
                    current_segment_score = "Ue"
                    
        elif previous_segment is None and next_segment is not None:
            # start case (for the first segment):
            if current_segment[index_of_standard_category] == "FP":
                if next_segment[index_of_standard_category] == "TN" or next_segment[index_of_standard_category] == "FN":
                    current_segment_score = "I"
                elif next_segment[index_of_standard_category] == "TP":
                    current_segment_score = "Os"
            elif current_segment[index_of_standard_category] == "FN":
                if next_segment[index_of_standard_category] == "TN" or next_segment[index_of_standard_category] == "FP":
                    current_segment_score = "D"
                elif next_segment[index_of_standard_category] == "TP":
                    current_segment_score = "Us"

        elif previous_segment is not None and next_segment is None:
            # end case (for the last segment):
            if current_segment[index_of_standard_category] == "FP":
                if previous_segment[index_of_standard_category] == "TN" or previous_segment[index_of_standard_category] == "FN":
                    current_segment_score = "I"
                elif previous_segment[index_of_standard_category] == "TP":
                    current_segment_score = "Oe"
            elif current_segment[index_of_standard_category] == "FN":
                if previous_segment[index_of_standard_category] == "TN" or previous_segment[index_of_standard_category] == "FP":
                    current_segment_score = "D"
                elif previous_segment[index_of_standard_category] == "TP":
                    current_segment_score = "Ue"

        elif previous_segment is None and next_segment is None:
            # if only one segment is given (exceptional case):
            if current_segment[index_of_standard_category] == "FP":
                current_segment_score = "I"
            elif current_segment[index_of_standard_category] == "FN":
                current_segment_score = "D"

    return current_segment_score


def compute_detailed_segment_scores(segments):
    new_segments = []

    # Handle special case if only one segment exists:
    if len(segments) == 1:
        seg_score = score_segment(None, segments[0], None)
        n_seg = segments[0] + (seg_score,)  # Create new tuple (append to the end)
        new_segments.append(n_seg)
        return new_segments

    # handle first segment:
    seg_score = score_segment(None, segments[0], segments[1])
    n_seg = segments[0] + (seg_score,) # Create new tuple (append to the end)
    new_segments.append(n_seg)

    # Handle segments in the middle:
    for i in range(1, len(segments) - 1):
        seg_score = score_segment(segments[i-1], segments[i], segments[i+1])
        n_seg = segments[i] + (seg_score,)  # Create new tuple (append to the end)
        new_segments.append(n_seg)

    # handle last segment:
    seg_score = score_segment(segments[-2], segments[-1], None)
    n_seg = segments[-1] + (seg_score,)  # Create new tuple (append to the end)
    new_segments.append(n_seg)

    return new_segments


def count_segment_categories(segments):
    categories = ["TP", "TN", "I", "D", "F", "M", "Os", "Oe", "Us", "Ue"]
    results = {}

    # Init values:
    for c in categories:
        results[c] = 0

    # Calculate total segment length for each category
    for s in segments:
        results[s[5]] += s[1] - s[0]

    # Calculate normed values:
    eval_length = segments[-1][1] - segments[0][0]
    results_normed = {}
    for c in categories:
        results_normed[c] = results[c]/eval_length

    return results, results_normed


def twoset_metrics(segment_counts):
    P = segment_counts["D"] + segment_counts["F"] + segment_counts["Us"] + segment_counts["Ue"] + segment_counts["TP"]
    N = segment_counts["I"] + segment_counts["M"] + segment_counts["Os"] + segment_counts["Oe"] + segment_counts["TN"]

    dr = segment_counts["D"]/P
    fr = segment_counts["F"]/P
    us = segment_counts["Us"] / P
    ue = segment_counts["Ue"] / P
    tpr = 1 - (dr + fr + us + ue)

    ir = segment_counts["I"]/N
    mr = segment_counts["M"] / N
    o_s = segment_counts["Os"] / N
    oe = segment_counts["Oe"] / N
    fpr = ir + mr + o_s + oe

    results = {"dr": dr, "fr": fr, "us": us, "ue": ue, "tpr": tpr,
               "ir": ir, "mr": mr, "os": o_s, "oe": oe, "fpr": fpr }
    return results


def eval_segment_results(ground_truth_events, detected_events, evaluation_start, evaluation_end):
    segments_with_category = get_segments_with_standard_error_categories(ground_truth_events, detected_events,
                                                                         evaluation_start, evaluation_end)
    segments_with_detailed_categories = compute_detailed_segment_scores(segments_with_category)

    segment_counts, normed_segment_counts = count_segment_categories(segments_with_detailed_categories)
    twoset_results = twoset_metrics(segment_counts)

    return twoset_results, segments_with_detailed_categories, segment_counts, normed_segment_counts


def eval_events(ground_truth_events, detected_events, evaluation_start, evaluation_end):
    segments_with_category = get_segments_with_standard_error_categories(ground_truth_events, detected_events, evaluation_start, evaluation_end)
    segments_with_detailed_categories = compute_detailed_segment_scores(segments_with_category)

    # TODO: calculate statistics

    # TODO: return accumulated statistics as dictonary, segments with categories
    return None, segments_with_detailed_categories