import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import datetime as dt
import numpy as np

def label_days(ax, dates, i, j, calendar, pct=False):
    ni, nj = calendar.shape
    day_of_month = np.nan * np.zeros((ni, 5))
    day_of_month[i, j] = [d.day for d in dates]

    for (i, j), day in np.ndenumerate(day_of_month):
        if np.isfinite(day):
            ax.text(j - 0.4, i - 0.4, int(day), ha="center", va="center", fontsize=7)
        if np.isfinite(calendar[i][j]):
            if pct:
                ax.text(
                    j,
                    i,
                    str(int(100 * calendar[i][j])) + "%",
                    ha="center",
                    va="center",
                    fontsize=12,
                )
            else:
                ax.text(
                    j,
                    i,
                    int(calendar[i][j]),
                    ha="center",
                    va="center",
                    fontsize=12,
                )

    ax.set(xticks=np.arange(5), xticklabels=["M", "T", "W", "R", "F"])
    ax.xaxis.tick_top()


def label_months(ax, dates, i, j, calendar):
    month_labels = np.array(
        [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
    )
    months = np.array([d.month for d in dates])
    uniq_months = sorted(set(months))
    yticks = [i[months == m].mean() for m in uniq_months]
    labels = [month_labels[m - 1] for m in uniq_months]
    ax.set(yticks=yticks)
    ax.set_yticklabels(labels, rotation=90)


def calendar_array(dates, data):
    i, j = zip(*[d.isocalendar()[1:] for d in dates])
    i = np.array(i) - min(i)
    j = np.array(j) - 1
    ni = max(i) + 1

    calendar = np.nan * np.zeros((ni, 5))
    calendar[i, j] = data
    return i, j, calendar


def calendar_heatmap(ax, dates, data, pct=False):
    i, j, calendar = calendar_array(dates, data)
    # print(i, j, calendar)
    im = ax.imshow(calendar, interpolation="none", cmap="viridis")
    label_days(ax, dates, i, j, calendar, pct)
    label_months(ax, dates, i, j, calendar)
    ax.figure.colorbar(im)


def heatmap_plot(plotdata):
    # https://stackoverflow.com/questions/32485907/matplotlib-and-numpy-create-a-calendar-heatmap
    if plotdata is None:
        return None

    dates = plotdata.index.to_list()
    data = plotdata.combined.to_list()

    fig, axs = plt.subplots(1, 2, figsize=(14, 10))
    ax = axs[0]
    calendar_heatmap(ax, dates, data)
    ax.set_title("Total Absences Per Day")
    ax = axs[1]
    calendar_heatmap(ax, dates, plotdata.pctAbsent.to_list(), pct=True)
    ax.set_title("% Absent Per Day")





def label_plot(plotdata, ax, fmt_string, fntsize=8):
    for i in range(len(plotdata)):
        excused_pct = plotdata.Excused.iloc[i]
        unexcused_pct = plotdata.Unexcused.iloc[i]
        suspension_pct = plotdata.Suspension.iloc[i]
        if excused_pct > 0:
            ax.text(
                i,
                excused_pct / 2,
                fmt_string.format(excused_pct),
                fontsize=fntsize,
                ha="center",
            )
        if unexcused_pct > 0:
            ax.text(
                i,
                unexcused_pct / 2 + excused_pct,
                fmt_string.format(unexcused_pct),
                fontsize=fntsize,
                ha="center",
            )
        if suspension_pct > 0:
            ax.text(
                i,
                suspension_pct / 2 + excused_pct + unexcused_pct,
                fmt_string.format(suspension_pct),
                fontsize=fntsize,
                ha="center",
            )


def absence_grade_charts(input_data, title, label_rot=0,ha='center',label_bars=True):
    plotdata = input_data.rename(
        index={
            "Chronically Absent": "Chronic",
            "Not Chronically Absent": "Non-chronic",
        },
        columns={
            "PERCENT of Absences Excused": "Excused",
            "PERCENT of Absences Unexcused": "Unexcused",
            "PERCENT of Absences due to Suspension": "Suspension",
            "NUMBER of Excused Absences": "Excused",
            "NUMBER of Unexcused Absences": "Unexcused",
            "NUMBER of Days Suspended": "Suspension",
        },
    ).iloc[:, [2, 4, 6]]

    fig, ax = plt.subplots()
    ax.set_title(title)
    plotdata.plot(
        kind="bar", stacked=True, ax=ax, color=["#8db4e2", "#e6b8b7", "#ff6d6d"]
    )
    ax.grid(axis="y")
    ax.tick_params(axis="x", labelrotation=label_rot)
    if ha != 'center':
        plt.setp(ax.get_xticklabels(), ha=ha, rotation_mode="anchor")
    ymin, ymax = ax.get_ylim()
    ax.set_ylim([ymin, ymax * 1.05])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, 0))

    if label_bars:
        label_plot(plotdata, ax, "{0:.1%}", fntsize=6)


def absence_gender_charts(input_data, label_rot=0):
    plotdata_ = input_data.rename(
        index={
            "Chronically Absent Students": "Chronically Absent",
            "Non-chronically Absent Students": "Non-chronically Absent",
        },
        columns={
            "PERCENT of Absences Excused": "Excused",
            "PERCENT of Absences Unexcused": "Unexcused",
            "PERCENT of Absences due to Suspension": "Suspension",
            "NUMBER of Excused Absences": "Excused",
            "NUMBER of Unexcused Absences": "Unexcused",
            "NUMBER of Days Suspended": "Suspension",
        },
    )
    plotdata = plotdata_.iloc[:, [2, 4, 6]]

    fig, axs = plt.subplots(1, 2)
    fig.suptitle(
        "How does the breakdown of absences differ based on whether students were chronically absent or not?"
    )
    ax = axs[0]
    plotdata.plot(
        kind="bar", stacked=True, ax=ax, color=["#8db4e2", "#e6b8b7", "#ff6d6d"]
    )
    ax.grid(axis="y")
    # ax.set_title()
    ax.tick_params(axis="x", labelrotation=label_rot)
    ymin, ymax = ax.get_ylim()
    ax.set_ylim([ymin, ymax * 1.15])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, 0))

    label_plot(plotdata, ax, "{0:.1%}")

    plotdata = plotdata_.iloc[:, [1, 3, 5]]

    ax = axs[1]
    plotdata.plot(
        kind="bar", stacked=True, ax=ax, color=["#8db4e2", "#e6b8b7", "#ff6d6d"]
    )
    ax.grid(axis="y")
    # ax.set_title()
    ax.tick_params(axis="x", labelrotation=label_rot)
    ymin, ymax = ax.get_ylim()
    ax.set_ylim([ymin, ymax * 1.1])
    label_plot(plotdata, ax, "{0:,}")


def race_grade_charts(input_data):
    plotdata = (
        input_data.rename(
            columns={"PERCENT ALL chronic absence (severe + moderate)": "All Chronic"}
        )
        .loc[:, ["All Chronic"]]
        .swaplevel()
        .unstack()
        .droplevel(0, axis=1)
    )
    plotdata.columns.name = ""
    fig, ax = plt.subplots()
    plotdata.plot(
        kind="line",
        ax=ax,
        style=["o-", "^-", "*-", "s-", ".-", ">-"],
    )
    ax.grid(axis="y")
    ax.set_title(
        "What percentage of students are chronically absent by race/ethnicity and grade?"
    )
    ax.tick_params(axis="x", labelrotation=0)
    ymin, ymax = ax.get_ylim()
    ax.set_ylim([ymin, ymax * 1.1])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, 0))


def sp_eng_fre_charts(input_data, chart_titles, label_rot=0):

    fig, axs = plt.subplots(1, 2)
    ax = axs[0]
    plotdata = input_data.iloc[:-1, [1, 3]].rename(
        columns={
            "PERCENT severe chronic absence": "Severe Chronic",
            "PERCENT moderate chronic absence": "Moderate",
        }
    )
    plotdata.plot(kind="bar", stacked=True, ax=ax, color=["#ffc000", "#ffcc99"])

    ax.grid(axis="y")
    ax.set_title(chart_titles[0])
    ax.tick_params(axis="x", labelrotation=label_rot)
    ymin, ymax = ax.get_ylim()
    ax.set_ylim([ymin, ymax * 1.1])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, 0))

    for i in range(len(plotdata)):
        severe_pct = plotdata["Severe Chronic"].iloc[i]
        severe_cnt = input_data["NUMBER severe chronic absence"].iloc[i]
        if severe_pct > 0:
            ax.text(
                i,
                severe_pct,
                "{0:.1%}\n{1}".format(severe_pct, severe_cnt),
                fontsize=10,
                ha="center",
            )
        moderate_pct = plotdata["Moderate"].iloc[i]
        moderate_cnt = input_data["NUMBER moderate chronic absence"].iloc[i]
        if moderate_pct > 0:
            ax.text(
                i,
                moderate_pct + severe_pct,
                "{0:.1%}\n{1}".format(moderate_pct, moderate_cnt),
                fontsize=10,
                ha="center",
            )

    plotdata = input_data.iloc[0, [4, 6, 8]]
    ax = axs[1]
    keys = [
        "PERCENT ALL\nchronic absence",
        "PERCENT at-risk\nattendance",
        "PERCENT satisfactory\nattendance",
    ]
    numbers = plotdata.tolist()
    explode = [0.1, 0, 0]
    plt.pie(
        numbers,
        labels=keys,
        colors=["#ff6d6d", "#ffff99", "#c3d69b"],
        autopct="%.1f%%",
        explode=explode,
    )

    ax.set_title(chart_titles[1])


def grade_race_gender_charts(input_data, chart_titles, label_rot=0):

    fig, axs = plt.subplots(1, 2)
    ax = axs[0]
    plotdata = input_data.iloc[:-1, [1, 3]].rename(
        columns={
            "PERCENT severe chronic absence": "Severe Chronic",
            "PERCENT moderate chronic absence": "Moderate",
        }
    )
    plotdata.plot(kind="bar", stacked=True, ax=ax, color=["#ffc000", "#ffcc99"])

    ax.grid(axis="y")
    ax.set_title(chart_titles[0])
    ax.tick_params(axis="x", labelrotation=label_rot)
    ymin, ymax = ax.get_ylim()
    ax.set_ylim([ymin, ymax * 1.1])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, 0))

    for i in range(len(plotdata)):
        fontsz = -0.5 * len(plotdata) + 14
        severe_pct = plotdata["Severe Chronic"].iloc[i]
        severe_cnt = input_data["NUMBER severe chronic absence"].iloc[i]
        if severe_pct > 0:
            ax.text(
                i,
                severe_pct,
                "{0:.1%}\n{1}".format(severe_pct, severe_cnt),
                fontsize=fontsz,
                ha="center",
            )
        moderate_pct = plotdata["Moderate"].iloc[i]
        moderate_cnt = input_data["NUMBER moderate chronic absence"].iloc[i]
        if moderate_pct > 0:
            ax.text(
                i,
                moderate_pct + severe_pct,
                "{0:.1%}\n{1}".format(moderate_pct, moderate_cnt),
                fontsize=fontsz,
                ha="center",
            )

    plotdata = input_data.iloc[:-1, 9]
    ax = axs[1]
    plotdata.plot(kind="bar", ax=ax, color=["#c3d69b"])
    ax.grid(axis="y")
    ax.set_title(chart_titles[1])
    ax.tick_params(axis="x", labelrotation=label_rot)
    ymin, ymax = ax.get_ylim()
    ax.set_ylim([ymin, ymax * 1.1])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, 0))

    for i in range(len(plotdata)):
        fontsz = -0.5 * len(plotdata) + 14
        ax.text(
            i,
            plotdata.iloc[i],
            "{0:.1%}\n{1}".format(
                plotdata.iloc[i], input_data["NUMBER satisfactory attendance"].iloc[i]
            ),
            fontsize=fontsz,
            ha="center",
        )
