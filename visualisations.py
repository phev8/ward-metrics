import matplotlib.pyplot as plt


def plot_segment_results(segment_results, ground_truth_events, detected_events, use_datetime_x=False, show=True):
    fig = plt.figure(figsize=(10, 3))

    # TODO: convert times to datetime if flag is set

    # TODO: write y axis labels for ground truth and detections

    for d in detected_events:
        plt.axvspan(d[0], d[1], 0, 0.5)

    for gt in ground_truth_events:
        plt.axvspan(gt[0], gt[1], 0.5, 1)

    for s in segment_results:
        color = "black"
        if s[2] == "TP":
            color = "green"
        elif s[2] == "FP":
            color = "red"
        elif s[2] == "FN":
            color = "yellow"
        elif s[2] == "TN":
            color = "blue"

        # TODO: format text nicely
        plt.text((s[1]+s[0])/2 - 2, 0.5, s[3])
        plt.axvspan(s[0], s[1], 0.4, 0.6, color=color)
        plt.axvline(s[0], color="black")
        plt.axvline(s[1], color="black")

    plt.tight_layout()

    if show:
        plt.show()
    else:
        plt.draw()