import matplotlib.pyplot as plt


def plot_events_with_segment_scores(segment_results, ground_truth_events, detected_events, use_datetime_x=False, show=True):
    """
    Test
    :param segment_results:
    :param ground_truth_events:
    :param detected_events:
    :param use_datetime_x:
    :param show:
    :return:
    """
    fig = plt.figure(figsize=(10, 3))

    # TODO: convert times to datetime if flag is set

    # TODO: write y axis labels for ground truth and detections

    for d in detected_events:
        plt.axvspan(d[0], d[1], 0, 0.5)

    for gt in ground_truth_events:
        plt.axvspan(gt[0], gt[1], 0.5, 1)

    for s in segment_results:
        color = "black"
        index_of_cat = 4
        if s[index_of_cat] == "TP":
            color = "green"
        elif s[index_of_cat] == "FP":
            color = "red"
        elif s[index_of_cat] == "FN":
            color = "yellow"
        elif s[index_of_cat] == "TN":
            color = "blue"

        # TODO: format text nicely
        plt.text((s[1]+s[0])/2, 0.8, s[2], horizontalalignment='center', verticalalignment='center')
        plt.text((s[1]+s[0])/2, 0.2, s[3], horizontalalignment='center', verticalalignment='center')
        plt.text((s[1]+s[0])/2, 0.5, s[5], horizontalalignment='center', verticalalignment='center')
        plt.axvspan(s[0], s[1], 0.4, 0.6, color=color)
        plt.axvline(s[0], color="black")
        plt.axvline(s[1], color="black")

    plt.tight_layout()

    if show:
        plt.show()
    else:
        plt.draw()


def plot_events_with_event_scores(gt_event_scores, detected_event_scores, ground_truth_events, detected_events, show=True):
    fig = plt.figure(figsize=(10, 3))
    for i in range(len(detected_events)):
        d = detected_events[i]
        plt.axvspan(d[0], d[1], 0, 0.5)
        plt.text((d[1] + d[0]) / 2, 0.2, detected_event_scores[i], horizontalalignment='center', verticalalignment='center')

    for i in range(len(ground_truth_events)):
        gt = ground_truth_events[i]
        plt.axvspan(gt[0], gt[1], 0.5, 1)
        plt.text((gt[1] + gt[0]) / 2, 0.8, gt_event_scores[i], horizontalalignment='center', verticalalignment='center')

    plt.tight_layout()

    if show:
        plt.show()
    else:
        plt.draw()


def plot_twoset_metrics(results, startangle=120):
    fig1, axarr = plt.subplots(1, 2)

    # plot positive rates:
    labels_1 = ["tpr", "us", "ue", "fr", "dr"]
    values_1 = [
        results["tpr"],
        results["us"],
        results["ue"],
        results["fr"],
        results["dr"]
    ]

    axarr[0].pie(values_1, labels=labels_1, autopct='%1.0f%%', startangle=startangle)
    axarr[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # TODO: add title

    # plot negative rates:
    labels_2 = ["1-fpr", "os", "oe", "mr", "ir"]
    values_2 = [
        1-results["fpr"],
        results["os"],
        results["oe"],
        results["mr"],
        results["ir"]
    ]

    axarr[1].pie(values_2, labels=labels_2, autopct='%1.0f%%', startangle=startangle)
    axarr[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # TODO: add title

    plt.show()


def plot_segment_counts(results):
    # TODO: add title
    labels = results.keys()
    values = []
    for label in labels:
        values.append(results[label])

    #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    total = sum(values)

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct=lambda p: '{:.0f}'.format(p * total / 100), startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


def plot_event_analysis_diagram(event_results, fontsize=10, use_percentage=False):
    """ Plot the event analysis diagram (EAD) for the given results

    Visualisation of the distribution of specific error types either with the actual event count or
    showing the percentage of the total events. Elements of the plot can be adjusted (like color, fontsize etc.)

    Args:
        event_results (dictionary): Dictionary object with ...

    Keyword Arguments:
        fontsize (int): ...
        use_percentage (bool): ...
        color_merging (todo): ...

    Returns:
        ...
    """
    fig = plt.figure(figsize=(10, 2))

    total = event_results["total_gt"] + event_results["total_det"] - event_results["C"]

    # Layout settings:
    y_min = 0.3
    y_max = 0.7
    width = 0.02
    text_x_offset = 0
    text_y_pos_1 = 0.55
    text_y_pos_2 = 0.4

    # Color settings:
    cmap = plt.get_cmap("Paired")
    color_deletion = cmap(4)
    color_fragmented = cmap(6)
    color_fragmented_merged = cmap(0)
    color_merged = cmap(8)
    color_correct = cmap(3)
    color_merging = cmap(9)
    color_merging_fragmenting = cmap(1)
    color_fragmenting = cmap(7)
    color_insertion = cmap(5)

    # Show deletions:
    current_score = "D"
    current_x_start = 0
    current_x_end = event_results[current_score]
    plt.axvspan(current_x_start, current_x_end, y_min, y_max, color=color_deletion)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score, fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    if use_percentage:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, "{:.0f}".format(event_results[current_score]*100/event_results["total_gt"]) + "%",
                    fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    else:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]),
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')


    # Show fragmented events:
    current_score = "F"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color=color_fragmented)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score, fontsize=fontsize,
             horizontalalignment='center', verticalalignment='center')
    if use_percentage:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2,
                 "{:.0f}".format(event_results[current_score] * 100 / event_results["total_gt"]) + "%",
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    else:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]),
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')

    # Show fragmented and merged events:
    current_score = "FM"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color=color_fragmented_merged)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score, fontsize=fontsize,
             horizontalalignment='center', verticalalignment='center')
    if use_percentage:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2,
                 "{:.0f}".format(event_results[current_score] * 100 / event_results["total_gt"]) + "%",
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    else:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]),
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')

    # Show merged events:
    current_score = "M"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color=color_merged)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score, fontsize=fontsize,
             horizontalalignment='center', verticalalignment='center')
    if use_percentage:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2,
                 "{:.0f}".format(event_results[current_score] * 100 / event_results["total_gt"]) + "%",
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    else:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]),
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')

    # Show correct events:
    current_score = "C"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color=color_correct)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score, fontsize=fontsize,
             horizontalalignment='center', verticalalignment='center')
    if use_percentage:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2,
                 "{:.0f}".format(event_results[current_score] * 100 / event_results["total_gt"]) + "%/" + "{:.0f}".format(event_results[current_score] * 100 / event_results["total_det"]) + "%",
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    else:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]),
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')

    # Show merging detections:
    current_score = "M'"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color=color_merging)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score, fontsize=fontsize,
             horizontalalignment='center', verticalalignment='center')
    if use_percentage:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2,
                 "{:.0f}".format(event_results[current_score] * 100 / event_results["total_det"]) + "%",
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    else:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]),
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')

    # Show fragmenting and merging detections:
    current_score = "FM'"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end, y_min, y_max, color=color_merging_fragmenting)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score, fontsize=fontsize,
             horizontalalignment='center', verticalalignment='center')
    if use_percentage:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2,
                 "{:.0f}".format(event_results[current_score] * 100 / event_results["total_det"]) + "%",
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    else:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]),
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')

    # Show fragmenting detections:
    current_score = "F'"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end, y_min, y_max, color=color_fragmenting)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score, fontsize=fontsize,
             horizontalalignment='center', verticalalignment='center')
    if use_percentage:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2,
                 "{:.0f}".format(event_results[current_score] * 100 / event_results["total_det"]) + "%",
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    else:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]),
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')

    # Show insertions:
    current_score = "I'"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end, y_min, y_max, color=color_insertion)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score, fontsize=fontsize,
             horizontalalignment='center', verticalalignment='center')
    if use_percentage:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2,
                 "{:.0f}".format(event_results[current_score] * 100 / event_results["total_det"]) + "%",
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    else:
        plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]),
                 fontsize=fontsize, horizontalalignment='center', verticalalignment='center')

    # Draw line for total events:
    plt.axvspan(0, event_results["total_gt"], y_max, y_max + width, color="black")
    plt.axvspan( total - event_results["total_det"], total, y_min, y_min - width, color="black")

    plt.text((0 + event_results["total_gt"]) / 2, 0.8, "Actual events (total=" + str(event_results["total_gt"]) + ")", horizontalalignment='center',
        verticalalignment='center')
    plt.text((2*total - event_results["total_det"]) / 2, 0.2, "Detected events (total=" + str(event_results["total_det"]) + ")", horizontalalignment='center',
        verticalalignment='center')

    plt.tight_layout()
    plt.show()

