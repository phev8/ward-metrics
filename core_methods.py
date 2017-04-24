

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

    return category


def get_segments_with_standard_error_categories(ground_truth_events, detected_events, evaluation_start=None, evaluation_end=None):
    segments = []

    gt_index = 0
    det_index = 0
    last_segment = None

    # TODO: handle if no gt or no det

    while True:
        if gt_index >= len(ground_truth_events):
            if det_index >= len(detected_events):
                if evaluation_end is not None:
                    category = get_standard_category_for_segment(last_segment[1], evaluation_end, ground_truth_events, detected_events)
                    last_segment = (last_segment[1], evaluation_end, category)
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

            category = get_standard_category_for_segment(seg_start, seg_end, ground_truth_events, detected_events)
            last_segment = (seg_start, seg_end, category)
            segments.append(last_segment)
        else:
            if evaluation_start is None:
                seg_start = min(gt_start, d_start)
                seg_end = min(gt_end, d_end)
            else:
                seg_start = evaluation_start
                seg_end = min(gt_start, d_start)

            category = get_standard_category_for_segment(seg_start, seg_end, ground_truth_events, detected_events)
            last_segment = (seg_start, seg_end, category)
            segments.append(last_segment)

        if seg_end >= d_end:
            det_index += 1
        if seg_end >= gt_end:
            gt_index += 1

    return segments


def compute_detailed_error_categories(segments):
    new_segments = []

    # TODO: what happens if only one segment

    # handle first segment:
    if segments[0][2] == "TP":
        n_seg = (segments[0][0], segments[0][1], segments[0][2], "TP")
    elif segments[0][2] == "TN":
        n_seg = (segments[0][0], segments[0][1], segments[0][2], "TN")
    elif segments[0][2] == "FP":
        if segments[1][2] == "TN" or segments[1][2] == "FN":
            n_seg = (segments[0][0], segments[0][1], segments[0][2], "I")
        elif segments[1][2] == "TP":
            n_seg = (segments[0][0], segments[0][1], segments[0][2], "Os")
        else:
            print("FP follows FP. This shouldn't happen.")
    elif segments[0][2] == "FN":
        if segments[1][2] == "TN" or segments[1][2] == "FP":
            n_seg = (segments[0][0], segments[0][1], segments[0][2], "D")
        elif segments[1][2] == "TP":
            n_seg = (segments[0][0], segments[0][1], segments[0][2], "Us")
        else:
            print("FN follows FN. This shouldn't happen.")
    new_segments.append(n_seg)


    # Handle segments in the middle:
    for i in range(1, len(segments) - 1):
        s_index = i
        if segments[s_index][2] == "TP":
            n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "TP")
        elif segments[s_index][2] == "TN":
            n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "TN")
        elif segments[s_index][2] == "FP":
            if (segments[s_index - 1][2] == "TN" or segments[s_index - 1][2] == "FN") and \
                    (segments[s_index + 1][2] == "TN" or segments[s_index + 1][2] == "FN"):
                n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "I")
            elif segments[s_index - 1][2] == "TP" and segments[s_index + 1][2] == "TP":
                n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "M")
            elif (segments[s_index - 1][2] == "TN" or segments[s_index - 1][2] == "FN") and segments[s_index + 1][2] == "TP":
                n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "Os")
            elif segments[s_index - 1][2] == "TP" and (segments[s_index + 1][2] == "TN" or segments[s_index + 1][2] == "FN"):
                n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "Oe")
            else:
                print("FP follows FP. This shouldn't happen.")
        elif segments[s_index][2] == "FN":
            if (segments[s_index - 1][2] == "TN" or segments[s_index - 1][2] == "FP") and (segments[s_index + 1][2] == "TN" or segments[s_index + 1][2] == "FP"):
                n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "D")
            elif segments[s_index - 1][2] == "TP" and segments[s_index + 1][2] == "TP":
                n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "F")
            elif (segments[s_index - 1][2] == "TN" or segments[s_index - 1][2] == "FP") and segments[s_index + 1][2] == "TP":
                n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "Us")
            elif segments[s_index - 1][2] == "TP" and (segments[s_index + 1][2] == "TN" or segments[s_index + 1][2] == "FP"):
                n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "Ue")
            else:
                print("FN follows FN. This shouldn't happen.")
        new_segments.append(n_seg)

    # handle last segment:
    s_index = -1
    if segments[s_index][2] == "TP":
        n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "TP")
    elif segments[s_index][2] == "TN":
        n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "TN")
    elif segments[s_index][2] == "FP":
        if segments[s_index-1][2] == "TN" or segments[s_index-1][2] == "FN":
            n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "I")
        elif segments[s_index-1][2] == "TP":
            n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "Oe")
        else:
            print("FP follows FP. This shouldn't happen.")
    elif segments[s_index][2] == "FN":
        if segments[s_index-1][2] == "TN" or segments[s_index - 1][2] == "FP":
            n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "D")
        elif segments[s_index-1][2] == "TP":
            n_seg = (segments[s_index][0], segments[s_index][1], segments[s_index][2], "Ue")
        else:
            print("FN follows FN. This shouldn't happen.")
    new_segments.append(n_seg)

    return new_segments


def ward_eval(ground_truth_events, detected_events, evaluation_start, evaluation_end):
    segments_with_category = get_segments_with_standard_error_categories(ground_truth_events, detected_events, evaluation_start, evaluation_end)
    segments_with_detailed_categories = compute_detailed_error_categories(segments_with_category)

    # TODO: calculate statistics

    # TODO: return accumulated statistics as dictonary, segments with categories
    return None, segments_with_detailed_categories