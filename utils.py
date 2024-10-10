from shiny import render

reports = {
    "By Grade Current": "bygrade",
    "By Grade Prior": "bygrade_prior",
    "By Grade Two Yr Prior": "bygrade_two_yr_prior",
    "By Grade Past 3 Years": "bygrade3yrs",
    "By School": "byschool",
    "By Race-Ethnicity": "byrace",
    "By Gender": "bygender",
    "By Race & Gender": "byracegender",
    "By Race & Grade": "byracegrade",
    "By Sp Needs Status": "byIEP",
    "By Eng Learner": "byEngLearner",
    "By Lunch Status": "byFreeReduced",
    "By Zip Code": "byzipcode",
    "By District": "bydistrict",
    "Suspensions in Each School": "by_suspension_school",
    "Absence Types": "absence_types",
    "Absence By School": "absence_by_school",
    "Absence By Gender": "absence_by_gender",
    "Absence By Grade": "absence_by_grade",
    "Absence By Race-Ethnicity": "absence_by_race",
    "By Race-Eth & Gender Chronic": "absence_by_racegender",
    "By Race-Eth & Gender Not Chronic": "absence_by_racegender_not",
    "Part 1 Notifications": "part1_notifications",
    "Part 2 Notifications": "part2_notifications",
    "Part 3 Notifications": "part3_notifications",
    "Part 1 Notifications By Grade": "part1_grade_notifications",
    "Part 2 Notifications By Grade": "part2_grade_notifications",
    "Part 3 Notifications By Grade": "part3_grade_notifications",
    "Part 1 Notifications By School": "part1_school_notifications",
    "Part 2 Notifications By School": "part2_school_notifications",
    "Part 3 Notifications By School": "part3_school_notifications",
    'Calendar Absence Heatmap':'heatmap',
}


# put in the same order as the report titles
question_titles = [
    "How many students are at risk based on their attendance? How does this break down by grade level?",
    "How many students were at risk based on their attendance during the same time window last year?",
    "How many students were at risk based on their attendance during the same time window two years ago?",
    "Have district-wide attendance patterns changed over time?",
    "What are the attendance patterns of each school in the district? How does each school's average daily attendance compare to its rates of chronic absence?",
    "How many students in different racial/ethnic groups at at risk based on their attendance?",
    "How many boys and girls are at risk based on their attendance?",
    "How many students are at risk based on their attendance, by race and gender?",
    "How many students are at risk based on their attendance, by race and grade?",
    "To what extent are students with and without special needs at risk based on attendance?",
    "To what extent are English Learner and non-English Learner students at risk based on attendance?",
    "To what extent are students with and without free/reduced lunch status at risk based on attendance?",
    "How many students in each zip code are at risk based on their attendance?",
    "How many students in each district are at risk based on their attendance? (Only relevant if El Dorado County is selected)",
    "What are the suspension patterns of each school in the district? How does each school's suspension rate compare to its rates of chronic absence?",
    "How much school did students miss due to excused absences, unexcused absences, or suspensions?",
    "How much school did students miss due to excused absences ,unexcused absences, or suspensions, at each school?",
    "Does the breakdown of absence types (excused, unexcused, suspensions) differ by gender?",
    "Do the breakdowns of absence types (excused, unexcused, suspensions) differ by grade level?",
    "How much school did students miss due to excused absences, unexcused absences, or suspensions, by ethnicity?",
    "Does the breakdown of absence types (excused, unexcused, suspensions) differ by race/ethnicity and gender for chronically absent students?",
    "By comparison, does the breakdown of absence types (excused, unexcused, suspensions) differ by race/ethnicity and gender for non-chronically absent students?",
    "How many chronically absent students were notified about absence issues?",
    "How many times did chronically absent students receive a Notice of Truancy (0-3 or more)?",
    "What percentage of chronically absent students were sent an excessive absence letter?",
    "How many chronically absent students were notified about absence issues, by GRADE? ",
    "How many times did chronically absent students receive a Notice of Truancy (0-3 or more), by GRADE?",
    "What percentage of chronically absent students were sent an excessive absence letter, by GRADE?",
    "How many chronically absent students were notified about absence issues, by SCHOOL?",
    "How many times did chronically absent students receive a Notice of Truancy (0-3 or more), by SCHOOL?",
    "What percentage of chronically absent students were sent an excessive absence letter, by SCHOOL?",
    "What days are the worst for attendance?"
]


question_titles = dict(zip(list(reports.keys()), question_titles))


districts = {
    "El Dorado County": "all_county",
    "Black Oak Mine Unified": "black_oak_mine_unified",
    "Camino Unified": "camino_unified",
    "Edcoe Charter": "EDCOE_charter",
    "Edcoe Sped": "EDCOE_sped",
    "El Dorado Union High": "el_dorado_union_high",
    "Gold Oak Union Elementary": "gold_oak_union_elementary",
    "Gold Trail Union Elementary": "gold_trail_union_elementary",
    "Lake Tahoe Unified": "lake_tahoe_unified",
    "Latrobe": "latrobe",
    "Mother Lode Union Elementary": "mother_lode_union_elementary",
    "Pioneer Union Elementary": "pioneer_union_elementary",
    "Placerville Union Elementary": "placerville_union_elementary",
    "Pollock Pines Elementary": "pollock_pines_elementary",
    "Rescue Union Elementary": "rescue_union_elementary",
    "Silver Fork Elementary": "silver_fork_elementary",
}


def style_dataframe(df):

    new_df = df.copy()

    green_styles = [
        {
            "rows": [2, 4],
            "cols": [2, 4],
            "style": {
                "background-color": "mediumspringgreen",
            },
        },
    ]
    columns_to_convert = [
        "PERCENT of Students Receiving Free/Reduced Lunch",
        "Average Daily Attendance (ADA)",
        "PERCENT severe chronic absence",
        "PERCENT moderate chronic absence",
        "PERCENT ALL chronic absence (severe + moderate)",
        "PERCENT at-risk attendance",
        "PERCENT satisfactory attendance",
        "PERCENT of total students with at least one suspension",
        "PERCENT of total students with two or more suspension",
        "PERCENT ALL chronic absense with at least one suspension",
        "PERCENT ALL chronic absense with two or more suspensions",
        "PERCENT NOT chronically absent with at least one suspension",
        "PERCENT NOT chronically absent with two or more suspensions",
        "PERCENT of Absences Excused",
        "PERCENT of Absences Unexcused",
        "PERCENT of Absences due to Suspension",
        "Percent of School Chronically Absent",
        "No Notifications PERCENT",
        "Excessive Absence Letter (only) PERCENT",
        "Notice of Truancy (only) PERCENT",
        "BOTH: Excessive Absence Letter AND Notice of Truancy PERCENT",
        "Pct of Grade",
        "PERCENT Zero NOTs",
        "PERCENT One NOT",
        "PERCENT Two Notices",
        "PERCENT Three or More",
        "Sent Excessive Absence Letter PERCENT",
    ]
    for col in columns_to_convert:
        if col in new_df.columns:
            new_df[col] = new_df[col].mul(100).round(1).astype("str") + "%"
    return render.DataGrid(
        new_df.reset_index(), selection_mode="rows", filters=True, styles=None
    )


def style_table(df, subsets):
    return (
        df.style.set_table_attributes('class="dataframe shiny-table table w-auto"')
        .set_table_styles([dict(selector="th", props=[("text-align", "left")])])
        .format(
            {
                **{
                    col: "{:.1%}"
                    for col in [
                        "PERCENT of Students Receiving Free/Reduced Lunch",
                        "Average Daily Attendance (ADA)",
                        "PERCENT severe chronic absence",
                        "PERCENT moderate chronic absence",
                        "PERCENT ALL chronic absence (severe + moderate)",
                        "PERCENT at-risk attendance",
                        "PERCENT satisfactory attendance",
                        "PERCENT of total students with at least one suspension",
                        "PERCENT of total students with two or more suspension",
                        "PERCENT ALL chronic absense with at least one suspension",
                        "PERCENT ALL chronic absense with two or more suspensions",
                        "PERCENT NOT chronically absent with at least one suspension",
                        "PERCENT NOT chronically absent with two or more suspensions",
                        "PERCENT of Absences Excused",
                        "PERCENT of Absences Unexcused",
                        "PERCENT of Absences due to Suspension",
                        "Percent of School Chronically Absent",
                        "No Notifications PERCENT",
                        "Excessive Absence Letter (only) PERCENT",
                        "Notice of Truancy (only) PERCENT",
                        "BOTH: Excessive Absence Letter AND Notice of Truancy PERCENT",
                        "Pct of Grade",
                        "PERCENT Zero NOTs",
                        "PERCENT One NOT",
                        "PERCENT Two Notices",
                        "PERCENT Three or More",
                        "Sent Excessive Absence Letter PERCENT",
                    ]
                },
            },
            na_rep="0.0%",
        )
        .set_properties(**{"background-color": "#ffc000"}, subset=subsets[0])
        .set_properties(**{"background-color": "#ffcc99"}, subset=subsets[1])
        .set_properties(**{"background-color": "#ff6d6d"}, subset=subsets[2])
        .set_properties(**{"background-color": "#ffff99"}, subset=subsets[3])
        .set_properties(**{"background-color": "#c3d69b"}, subset=subsets[4])
        .set_properties(**{"background-color": "#f2f2f2"}, subset=subsets[5])
        .set_properties(**{"background-color": "#c5d9f1"}, subset=subsets[6])
        .set_properties(**{"background-color": "#8db4e2"}, subset=subsets[7])
        .set_properties(**{"background-color": "#e6b8b7"}, subset=subsets[8])
        .set_properties(**{"background-color": "#b8cce4"}, subset=subsets[9])
        .set_properties(**{"background-color": "#95b3d7"}, subset=subsets[10])
        .set_properties(**{"background-color": "#366092"}, subset=subsets[11])
        .set_properties(**{"background-color": "#d8e4bc"}, subset=subsets[12])
        .set_properties(**{"background-color": "#c4d79b"}, subset=subsets[13])
        .set_properties(**{"background-color": "#9bbb59"}, subset=subsets[14])
        .set_properties(**{"background-color": "#f79443"}, subset=subsets[15])
    )


def get_subsets(all_columns):
    subsets = [
        [
            a
            for a in [
                "PERCENT severe chronic absence",
                "NUMBER severe chronic absence",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "PERCENT moderate chronic absence",
                "NUMBER moderate chronic absence",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "PERCENT ALL chronic absence (severe + moderate)",
                "NUMBER ALL chronic absence (severe + moderate)",
                "NUMBER ALL chronic absence with at least one suspension",
                "PERCENT ALL chronic absense with at least one suspension",
                "NUMBER ALL chronic absense with two or more suspensions",
                "PERCENT ALL chronic absense with two or more suspensions",
                "NUMBER of Days Suspended",
                "PERCENT of Absences due to Suspension",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "PERCENT at-risk attendance",
                "NUMBER at-risk attendance",
                "School Name",
                "Zero NOTs",
                "PERCENT Zero NOTs",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "PERCENT satisfactory attendance",
                "NUMBER satisfactory attendance",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "NUMBER of students with at least one suspension",
                "PERCENT of total students with at least one suspension",
                "NUMBER of students with two or more suspensions",
                "PERCENT of total students with two or more suspension",
                "Total number of incidents of suspension",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "NUMBER NOT CHRONICALLY ABSENT (at-risk + satisfactory)",
                "NUMBER NOT chronically absent with at least one suspension",
                "PERCENT NOT chronically absent with at least one suspension",
                "NUMBER NOT chronically absent with two or more suspensions",
                "PERCENT NOT chronically absent with two or more suspensions",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "NUMBER of Excused Absences",
                "PERCENT of Absences Excused",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "NUMBER of Unexcused Absences",
                "PERCENT of Absences Unexcused",
                "No Notifications",
                "No Notifications PERCENT",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "Excessive Absence Letter (only)",
                "Excessive Absence Letter (only) PERCENT",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "Notice of Truancy (only)",
                "Notice of Truancy (only) PERCENT",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "BOTH: Excessive Absence Letter AND Notice of Truancy",
                "BOTH: Excessive Absence Letter AND Notice of Truancy PERCENT",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "One Notices",
                "PERCENT One NOT",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "Two Notices",
                "PERCENT Two Notices",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "Three or More Notices",
                "PERCENT Three or More",
            ]
            if a in all_columns
        ],
        [
            a
            for a in [
                "Sent Excessive Absence Letter",
                "Sent Excessive Absence Letter PERCENT",
            ]
            if a in all_columns
        ],
    ]
    return subsets
