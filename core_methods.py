

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


def compute_detailed_error_categories(segments):
    new_segments = []
    index_of_cat = 4
    # TODO: what happens if only one segment

    # handle first segment:
    new_category = "error"
    if segments[0][index_of_cat] == "TP":
        new_category = "TP"
    elif segments[0][index_of_cat] == "TN":
        new_category = "TN"
    elif segments[0][index_of_cat] == "FP":
        if segments[1][index_of_cat] == "TN" or segments[1][2] == "FN":
            new_category = "I"
        elif segments[1][index_of_cat] == "TP":
            new_category = "Os"
        else:
            print("FP follows FP. This shouldn't happen.")
    elif segments[0][index_of_cat] == "FN":
        if segments[1][index_of_cat] == "TN" or segments[1][2] == "FP":
            new_category = "D"
        elif segments[1][index_of_cat] == "TP":
            new_category = "Us"
        else:
            print("FN follows FN. This shouldn't happen.")
    else:
        print(segments[0])
    n_seg = segments[0] + (new_category,)
    new_segments.append(n_seg)


    # Handle segments in the middle:
    for i in range(1, len(segments) - 1):
        s_index = i
        new_category = "error"
        if segments[s_index][index_of_cat] == "TP":
            new_category = "TP"
        elif segments[s_index][index_of_cat] == "TN":
            new_category = "TN"
        elif segments[s_index][index_of_cat] == "FP":
            if (segments[s_index - 1][index_of_cat] == "TN" or segments[s_index - 1][index_of_cat] == "FN") and \
                    (segments[s_index + 1][index_of_cat] == "TN" or segments[s_index + 1][index_of_cat] == "FN"):
                new_category = "I"
            elif segments[s_index - 1][index_of_cat] == "TP" and segments[s_index + 1][index_of_cat] == "TP":
                new_category = "M"
            elif (segments[s_index - 1][index_of_cat] == "TN" or segments[s_index - 1][index_of_cat] == "FN") and segments[s_index + 1][index_of_cat] == "TP":
                new_category = "Os"
            elif segments[s_index - 1][index_of_cat] == "TP" and (segments[s_index + 1][index_of_cat] == "TN" or segments[s_index + 1][index_of_cat] == "FN"):
                new_category = "Oe"
            else:
                print("FP follows FP. This shouldn't happen.")
        elif segments[s_index][index_of_cat] == "FN":
            if (segments[s_index - 1][index_of_cat] == "TN" or segments[s_index - 1][index_of_cat] == "FP") and (segments[s_index + 1][index_of_cat] == "TN" or segments[s_index + 1][index_of_cat] == "FP"):
                new_category = "D"
            elif segments[s_index - 1][index_of_cat] == "TP" and segments[s_index + 1][index_of_cat] == "TP":
                new_category = "F"
            elif (segments[s_index - 1][index_of_cat] == "TN" or segments[s_index - 1][index_of_cat] == "FP") and segments[s_index + 1][index_of_cat] == "TP":
                new_category = "Us"
            elif segments[s_index - 1][index_of_cat] == "TP" and (segments[s_index + 1][index_of_cat] == "TN" or segments[s_index + 1][index_of_cat] == "FP"):
                new_category = "Ue"
            else:
                print("FN follows FN. This shouldn't happen.")
        else:
            print(segments[s_index])

        n_seg = segments[s_index] + (new_category,)
        new_segments.append(n_seg)

    # handle last segment:
    s_index = -1
    if segments[s_index][index_of_cat] == "TP":
        new_category = "TP"
    elif segments[s_index][index_of_cat] == "TN":
        new_category = "TN"
    elif segments[s_index][index_of_cat] == "FP":
        if segments[s_index-1][index_of_cat] == "TN" or segments[s_index-1][index_of_cat] == "FN":
            new_category = "I"
        elif segments[s_index-1][index_of_cat] == "TP":
            new_category = "Oe"
        else:
            print("FP follows FP. This shouldn't happen.")
    elif segments[s_index][index_of_cat] == "FN":
        if segments[s_index-1][index_of_cat] == "TN" or segments[s_index - 1][index_of_cat] == "FP":
            new_category = "D"
        elif segments[s_index-1][index_of_cat] == "TP":
            new_category = "Ue"
        else:
            print("FN follows FN. This shouldn't happen.")

    n_seg = segments[s_index] + (new_category,)
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
    segments_with_detailed_categories = compute_detailed_error_categories(segments_with_category)

    segment_counts, normed_segment_counts = count_segment_categories(segments_with_detailed_categories)
    twoset_results = twoset_metrics(segment_counts)

    return twoset_results, segments_with_detailed_categories, segment_counts, normed_segment_counts


def eval_events(ground_truth_events, detected_events, evaluation_start, evaluation_end):
    segments_with_category = get_segments_with_standard_error_categories(ground_truth_events, detected_events, evaluation_start, evaluation_end)
    segments_with_detailed_categories = compute_detailed_error_categories(segments_with_category)

    # TODO: calculate statistics

    # TODO: return accumulated statistics as dictonary, segments with categories
    return None, segments_with_detailed_categories