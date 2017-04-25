import matplotlib.pyplot as plt


def plot_events_with_segment_scores(segment_results, ground_truth_events, detected_events, use_datetime_x=False, show=True):
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
        plt.text((s[1]+s[0])/2 - 1, 0.8, s[2])
        plt.text((s[1]+s[0])/2 - 1, 0.2, s[3])
        plt.text((s[1]+s[0])/2 - 2, 0.5, s[5])
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
        plt.text((d[1] + d[0]) / 2, 0.2, detected_event_scores[i])

    for i in range(len(ground_truth_events)):
        gt = ground_truth_events[i]
        plt.axvspan(gt[0], gt[1], 0.5, 1)
        plt.text((gt[1] + gt[0]) / 2, 0.8, gt_event_scores[i])

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


# TODO: plot event graph
def plot_event_analysis_diagram(event_results):
    fig = plt.figure(figsize=(10, 2))

    total = event_results["total_gt"] + event_results["total_det"] - event_results["C"]
    print(total)


    y_min = 0.2
    y_max = 0.8
    width = 0.02
    text_x_offset = 0.01
    text_y_pos_1 = 0.6
    text_y_pos_2 = 0.4

    current_score = "D"
    current_x_start = 0
    current_x_end = event_results[current_score]
    plt.axvspan(current_x_start, current_x_end, y_min, y_max, color="red")
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]))


    current_score = "F"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color="yellow")
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]))


    current_score = "FM"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color="orange")
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]))


    current_score = "M"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color="darkgreen")
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]))


    current_score = "C"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color="lightgreen")
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]))

    current_score = "M'"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end,  y_min, y_max, color="darkgreen")
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]))


    current_score = "FM'"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end, y_min, y_max, color="orange")
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]))


    current_score = "F'"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end, y_min, y_max, color="yellow")
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]))

    current_score = "I'"
    current_x_start = current_x_end
    current_x_end += event_results[current_score]
    plt.axvspan(current_x_start, current_x_end, y_min, y_max, color="red")
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_1, current_score)
    plt.text((current_x_start + current_x_end) / 2 - text_x_offset, text_y_pos_2, str(event_results[current_score]))

    # Draw line for total events:
    plt.axvspan(0, event_results["total_gt"], y_max, y_max + width, color="black")
    plt.axvspan( total - event_results["total_det"], total, y_min, y_min - width, color="black")

    # TODO: add percentage values

    plt.tight_layout()
    plt.show()

