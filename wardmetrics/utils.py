# TODO: implement event creation out of frame based results
# TODO: implement wrappers for pandas row based events
# TODO: implement pretty output printing
# TODO: wrapper for multiclass case


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

