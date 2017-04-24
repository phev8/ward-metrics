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