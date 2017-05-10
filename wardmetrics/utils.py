# TODO: implement event creation out of frame based results
# TODO: implement wrappers for pandas row based events
# TODO: wrapper for multiclass case


def frame_results_to_events(frame_results, frame_times=None):
    """
    Converting frame-by-frame results into a list of events for each label. If the classifier predicts the same label in a sequence it is considers as an event. (Filtering too short events, or merge close-by events is not included here.)

    Arguments:
        frame_results (list or numpy array): list of frame class labels in an temporal order (sequential). It can contain numeric or string values e.g. ``[1, 1, 0, ...]`` or ``['class_1', 'class_1', 'class_0', ...]``
        frame_times (list or numpy array): list of timestamps (preferably as numeric values e.g. posix time) for each frame.

    Returns:
        dictionary: list of events (tuple of start and end times/indexes) for each unique label found in the frame_results. Event start value is the first occurence of the label, event end is the time or index of the next frame after the event (also the start of the next event).
    """
    if len(frame_results) < 2:
        raise ValueError("frame_results has to contain at least 2 items.")

    if frame_times is not None and len(frame_results) != len(frame_times):
        raise ValueError("Length of frame_results and frame_times has to be equal.")

    unique_labels = set(frame_results)

    # Init event lists for each label:
    results = {}
    for l in unique_labels:
        results[str(l)] = []

    event_label = frame_results[0]
    event_start_index = 0

    for index in range(1, len(frame_results)):
        if frame_results[index] != event_label:
            # close event:
            if frame_times is None:
                results[str(event_label)].append((event_start_index, index))
            else:
                results[str(event_label)].append((frame_times[event_start_index], frame_times[index]))

            # start new event:
            event_label = frame_results[index]
            event_start_index = index

    # close last event:
    if frame_times is None:
        results[str(event_label)].append((event_start_index, index+1))
    else:
        results[str(event_label)].append((frame_times[event_start_index], frame_times[-1] + float(frame_times[-1] - frame_times[0])/(len(frame_times)-1) ))

    return results


def print_standard_event_metrics(standard_event_results):
    """
    Print standard precision and recall values

    Examples:
        >>> print_standard_event_metrics(test_r)
        Standard event results:
            precision:\t0.8888888\tWeighted by length:	0.9186991
            recall:\t0.3333333\tWeighted by length:	0.2230576
    """
    print("Standard event results:")
    print("\tprecision:\t" + str(standard_event_results["precision"]) + "\tWeighted by length:\t" + str(standard_event_results["precision (weighted)"]))
    print("\trecall:\t\t" + str(standard_event_results["recall"]) + "\tWeighted by length:\t" + str(standard_event_results["recall (weighted)"]))


def standard_event_metrics_to_list(standard_event_results):
    """ Converting standard event metric results to a list (position of each item is fixed)

    Argument:
        standard_event_results (dictionary): as provided by the 4th item in the results of eval_events function

    Returns:
        list: Item order: 1. Precision, 2. Recall 3. Length weighted precision, 4. Length weighted recall
    """
    return [
        standard_event_results["precision"],
        standard_event_results["recall"],
        standard_event_results["precision (weighted)"],
        standard_event_results["recall (weighted)"]]


def standard_event_metrics_to_string(standard_event_results, separator=", ", prefix="[", suffix="]"):
    """ Converting standard event metric results to a string

    Argument:
        standard_event_results (dictionary): as provided by the 4th item in the results of eval_events function

    Keyword Arguments:
        separator (str): characters between each item
        prefix (str): string that will be added before the line
        suffix (str): string that will be added to the end of the line

    Returns:
        str: Item order: 1. Precision, 2. Recall 3. Length weighted precision, 4. Length weighted recall

    Examples:
        >>> standard_event_metrics_to_string(test_r)
        [0.88888, 0.33333, 0.918, 0.22305]
        >>> standard_event_metrics_to_string(test_r, separator="\t", prefix="/", suffix="/")
        /0.88888\t0.33333\t0.918\t0.22305/
        >>> standard_event_metrics_to_string(test_r, prefix="", suffix="\\n")
        0.88888, 0.33333, 0.918, 0.22305\\n

    """
    return prefix + separator.join(map(str, standard_event_metrics_to_list(standard_event_results))) + suffix


def print_detailed_event_metrics(detailed_event_results):
    """
    Print totals for each event category

    Example:
        >>> print_detailed_event_metrics(test_r)
        Detailed event results:
             Actual events:
                 deletions:\t\t1	12.50% of actual events
                 merged:\t\t3	37.50% of actual events
                 fragmented:\t\t1	12.50% of actual events
                 frag. and merged:\t1	12.50% of actual events
                 correct:\t\t2	25.00% of actual events
            Detected events:
                 insertions:\t\t1	11.11% of detected events
                 merging:\t\t1	11.11% of detected events
                 fragmenting:\t\t4	44.44% of detected events
                 frag. and merging:\t1	11.11% of detected events
                 correct:\t\t2	22.22% of detected events

    """
    print("Detailed event results:")
    print("\tActual events:")
    print("\t\tdeletions:\t\t\t" + str(detailed_event_results["D"]) + "\t" + "{0:.2f}".format(detailed_event_results["D"]*100/detailed_event_results["total_gt"]) + "% of actual events")
    print("\t\tmerged:\t\t\t\t" + str(detailed_event_results["M"]) + "\t" + "{0:.2f}".format(detailed_event_results["M"]*100/detailed_event_results["total_gt"]) + "% of actual events")
    print("\t\tfragmented:\t\t\t" + str(detailed_event_results["F"]) + "\t" + "{0:.2f}".format(detailed_event_results["F"]*100/detailed_event_results["total_gt"]) + "% of actual events")
    print("\t\tfrag. and merged:\t" + str(detailed_event_results["FM"]) + "\t" + "{0:.2f}".format(detailed_event_results["FM"]*100/detailed_event_results["total_gt"]) + "% of actual events")
    print("\t\tcorrect:\t\t\t" + str(detailed_event_results["C"]) + "\t" + "{0:.2f}".format(detailed_event_results["C"]*100/detailed_event_results["total_gt"]) + "% of actual events")

    print("\tDetected events:")
    print("\t\tinsertions:\t\t\t" + str(detailed_event_results["I'"]) + "\t" + "{0:.2f}".format(detailed_event_results["I'"]*100/detailed_event_results["total_det"]) + "% of detected events")
    print("\t\tmerging:\t\t\t" + str(detailed_event_results["M'"]) + "\t" + "{0:.2f}".format(detailed_event_results["M'"]*100/detailed_event_results["total_det"]) + "% of detected events")
    print("\t\tfragmenting:\t\t" + str(detailed_event_results["F'"]) + "\t" + "{0:.2f}".format(detailed_event_results["F'"]*100/detailed_event_results["total_det"]) + "% of detected events")
    print("\t\tfrag. and merging:\t" + str(detailed_event_results["FM'"]) + "\t" + "{0:.2f}".format(detailed_event_results["FM'"]*100/detailed_event_results["total_det"]) + "% of detected events")
    print("\t\tcorrect:\t\t\t" + str(detailed_event_results["C"]) + "\t" + "{0:.2f}".format(detailed_event_results["C"]*100/detailed_event_results["total_det"]) + "% of detected events")
    #print("\trecall:\t\t" + str(standard_event_results["recall"]) + "\tWeighted by length:\t" + str(standard_event_results["recall (weighted)"]))


def detailed_event_metrics_to_list(detailed_event_results):
    """ Converting detailed event metric results to a list (position of each item is fixed)

    Argument:
        detailed_event_results (dictionary): as provided by the 3rd item in the results of eval_events function

    Returns:
        list: Item order: 0. correct, 1. deletions 2. merged, 3. fragmented, 4. fragmented and merged, 5. fragmenting, 6. merging, 7. fragmenting and merging, 8. insertions, 9. total of actual events, 10. total of detected events
    """
    return [
        detailed_event_results["C"],
        detailed_event_results["D"],
        detailed_event_results["M"],
        detailed_event_results["F"],
        detailed_event_results["FM"],
        detailed_event_results["F'"],
        detailed_event_results["M'"],
        detailed_event_results["FM'"],
        detailed_event_results["I'"],
        detailed_event_results["total_gt"],
        detailed_event_results["total_det"],
        ]


def detailed_event_metrics_to_string(detailed_event_results, separator=", ", prefix="[", suffix="]"):
    """ Converting detailed event metric results to a string

    Argument:
        detailed_event_results (dictionary): as provided by the 3rd item in the results of eval_events function

    Keyword Arguments:
        separator (str): characters between each item
        prefix (str): string that will be added before the line
        suffix (str): string that will be added to the end of the line

    Returns:
        str: Item order: 0. correct, 1. deletions 2. merged, 3. fragmented, 4. fragmented and merged, 5. fragmenting, 6. merging, 7. fragmenting and merging, 8. insertions, 9. total of actual events, 10. total of detected events

    Examples:
        >>> detailed_event_metrics_to_string(test_r)
        [2, 1, 3, 1, 1, 4, 1, 1, 1, 8, 9]
        >>> detailed_event_metrics_to_string(test_r, separator=";", prefix="(", suffix=")\\n")
        (2;1;3;1;1;4;1;1;1;8;9)\\n

    """
    return prefix + separator.join(map(str, detailed_event_metrics_to_list(detailed_event_results))) + suffix


def print_detailed_segment_results(detailed_segment_results):
    """
    Print segment length for each detailed segment category. Can be used with normed values as well.

    Arguments:
        detailed_segment_results (dictionary): as provided by the 3rd or 4th item in the results of eval_segments function

    Example:
        >>> print_detailed_segment_results(test_r)
        Detailed segment results (length or frame count):
            true positive segments:\t\t40
            true negative segments:\t\t91
            insertion segments:\t\t\t10
            deletion segments:\t\t\t10
            fragmenting segments:\t\t7
            merge segments:\t\t\t15
            start overfill segments:\t\t10
            end overfill segments:\t\t28
            start underfill segments:\t\t13
            end underfill segments:\t\t15
    """
    print("Detailed segment results (length or frame count):")
    print("\ttrue positive segments:\t\t" + str(detailed_segment_results["TP"]))
    print("\ttrue negative segments:\t\t" + str(detailed_segment_results["TN"]))
    print("\tinsertion segments:\t\t\t" + str(detailed_segment_results["I"]))
    print("\tdeletion segments:\t\t\t" + str(detailed_segment_results["D"]))
    print("\tfragmenting segments:\t\t" + str(detailed_segment_results["F"]))
    print("\tmerge segments:\t\t\t\t" + str(detailed_segment_results["M"]))
    print("\tstart overfill segments:\t" + str(detailed_segment_results["Os"]))
    print("\tend overfill segments:\t\t" + str(detailed_segment_results["Oe"]))
    print("\tstart underfill segments:\t" + str(detailed_segment_results["Us"]))
    print("\tend underfill segments:\t\t" + str(detailed_segment_results["Ue"]))


def detailed_segment_results_to_list(detailed_segment_results):
    """ Converting detailed segment results to a list (position of each item is fixed). Can be used with normed values as well.

    Argument:
        detailed_segment_results (dictionary): as provided by the 3rd or 4th item in the results of eval_segments function

    Returns:
        list: Item order: 0. true posives, 1. true negatives, 2. insertions, 3. deletions, 4. fragmenting, 5. merged, 6. start overfill, 7. end overfill, 8. start underfill, 9. end underfill
    """
    return [
        detailed_segment_results["TP"],
        detailed_segment_results["TN"],
        detailed_segment_results["I"],
        detailed_segment_results["D"],
        detailed_segment_results["F"],
        detailed_segment_results["M"],
        detailed_segment_results["Os"],
        detailed_segment_results["Oe"],
        detailed_segment_results["Us"],
        detailed_segment_results["Ue"]
        ]


def detailed_segment_results_to_string(detailed_segment_results, separator=", ", prefix="[", suffix="]"):
    """ Converting detailed segment results to a string. Can be used with normed values as well.

    Argument:
        detailed_segment_results (dictionary): as provided by the 3rd or 4th item in the results of eval_segments function

    Keyword Arguments:
        separator (str): characters between each item
        prefix (str): string that will be added before the line
        suffix (str): string that will be added to the end of the line

    Returns:
        str: Item order: 0. true posives, 1. true negatives, 2. insertions, 3. deletions, 4. fragmenting, 5. merged, 6. start overfill, 7. end overfill, 8. start underfill, 9. end underfill

    Examples:
        >>> detailed_segment_results_to_string(test_r)
        [2, 1, 3, 1, 1, 4, 1, 1, 1, 8]
        >>> detailed_segment_results_to_string(test_r, separator=";", prefix="(", suffix=")\\n")
        (2;1;3;1;1;4;1;1;1;8)\\n

    """
    return prefix + separator.join(map(str, detailed_segment_results_to_list(detailed_segment_results))) + suffix


def print_twoset_segment_metrics(twoset_metrics_results):
    """
    Print 2SET metric results

    Argument:
        twoset_metrics_results (dictionary): as provided by the 1st item in the results of eval_events function

    Example:
        >>> print_twoset_segment_metrics(test_r)
        2SET metrics:
            true positive rate:\t\t0.471
            deletion rate:\t\t0.118
            fragmenting rate:\t\t0.082
            start underfill rate:\t0.153
            end underfill rate:\t\t0.176
            1 - false positive rate:\t0.591
            insertion rate:\t\t0.065
            merge rate:\t\t\t0.097
            start overfill rate:\t0.065
            end overfill rate:\t\t0.182
    """
    print("2SET metrics:")
    print("\ttrue positive rate:\t\t\t" + "{0:.3f}".format(twoset_metrics_results["tpr"]))
    print("\tdeletion rate:\t\t\t\t" + "{0:.3f}".format(twoset_metrics_results["dr"]))
    print("\tfragmenting rate:\t\t\t" + "{0:.3f}".format(twoset_metrics_results["fr"]))
    print("\tstart underfill rate:\t\t" + "{0:.3f}".format(twoset_metrics_results["us"]))
    print("\tend underfill rate:\t\t\t" + "{0:.3f}".format(twoset_metrics_results["ue"]))

    print("\n\t1 - false positive rate:\t" + "{0:.3f}".format(1 - twoset_metrics_results["fpr"]))
    print("\tinsertion rate:\t\t\t\t" + "{0:.3f}".format(twoset_metrics_results["ir"]))
    print("\tmerge rate:\t\t\t\t\t" + "{0:.3f}".format(twoset_metrics_results["mr"]))
    print("\tstart overfill rate:\t\t" + "{0:.3f}".format(twoset_metrics_results["os"]))
    print("\tend overfill rate:\t\t\t" + "{0:.3f}".format(twoset_metrics_results["oe"]))


def twoset_segment_metrics_to_list(twoset_metrics_results):
    """ Converting detailed event metric results to a list (position of each item is fixed)

    Argument:
        twoset_metrics_results (dictionary): as provided by the 1st item in the results of eval_events function

    Returns:
        list: Item order: 0. true positive rate, 1. deletion rate 2. fragmenting rate, 3. start underfill rate, 4. end underfill rate, 5. 1 - false positive rate, 6. insertion rate, 7. merge rate, 8. start overfill rate, 9. end overfill rate
    """
    return [
        twoset_metrics_results["tpr"],
        twoset_metrics_results["dr"],
        twoset_metrics_results["fr"],
        twoset_metrics_results["us"],
        twoset_metrics_results["ue"],
        1-twoset_metrics_results["fpr"],
        twoset_metrics_results["ir"],
        twoset_metrics_results["mr"],
        twoset_metrics_results["os"],
        twoset_metrics_results["oe"]
        ]


def twoset_segment_metrics_to_string(twoset_metrics_results, separator=", ", prefix="[", suffix="]"):
    """ Converting detailed event metric results to a string

    Argument:
        twoset_metrics_results (dictionary): as provided by the 1st item in the results of eval_events function

    Keyword Arguments:
        separator (str): characters between each item
        prefix (str): string that will be added before the line
        suffix (str): string that will be added to the end of the line

    Returns:
        str: Item order: 0. true positive rate, 1. deletion rate 2. fragmenting rate, 3. start underfill rate, 4. end underfill rate, 5. 1 - false positive rate, 6. insertion rate, 7. merge rate, 8. start overfill rate, 9. end overfill rate

    Examples:
        >>> twoset_segment_metrics_to_string(test_r)
        [0.47058823529411764, 0.11764705882352941, 0.08235294117647059, 0.15294117647058825, 0.17647058823529413, 0.5909090909090909, 0.06493506493506493, 0.09740259740259741, 0.06493506493506493, 0.18181818181818182]
        >>> twoset_segment_metrics_to_string(test_r, separator=";", prefix="(", suffix=")\\n")
        (0.47058823529411764;0.11764705882352941;0.08235294117647059;0.15294117647058825;0.17647058823529413;0.5909090909090909;0.06493506493506493;0.09740259740259741;0.06493506493506493;0.18181818181818182)\\n

    """
    return prefix + separator.join(map(str, twoset_segment_metrics_to_list(twoset_metrics_results))) + suffix
