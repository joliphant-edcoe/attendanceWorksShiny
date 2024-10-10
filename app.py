from shiny import App, ui, reactive, render
import pickle
from chart_plotting import (
    grade_race_gender_charts,
    sp_eng_fre_charts,
    race_grade_charts,
    absence_gender_charts,
    absence_grade_charts,
    heatmap_plot,
    notification_plot,
    notification_plot2,
    notification_plot3,
    notif_grade_plot,
    notif_grade_plot2,
    notif_grade_plot3,
    grade_3yr_charts,
)
from utils import (
    reports,
    question_titles,
    districts,
    get_subsets,
    style_table,
    style_dataframe,
)
from dotenv import load_dotenv
import os
import bcrypt
from github import Github
import pandas as pd
import urllib.request

##### to deploy on shinyapps.io ###### (anaconda prompt worked)
# rsconnect deploy shiny "C:\Users\joliphant\OneDrive - El Dorado County Office of Education\Documents\shinyPractice\01-basic-app"
# --name edcoe-fiscal-data --title attendanceworks2425


# all_data.pickle should contain a multilevel dict
# with the top level keys being the names of districts ('black_oak_mine_unified', etc),
# and the assiociated values being a dictionary with keys
# for each report type ('bygrade', etc)
# the values of this dictionary will be pandas dataframes.

path_to_file = os.path.dirname(__file__)
load_dotenv(os.path.join(path_to_file, ".env"))

ghub = Github(os.getenv('github_token'))
repo = ghub.get_repo('joliphant-edcoe/attendanceWorksDatastore')
contents = repo.get_contents('data')
private_urls = [c.download_url for c in contents]
# print(private_urls)

with urllib.request.urlopen(private_urls[0]) as f:
    oct = pickle.load(f)

with urllib.request.urlopen(private_urls[1]) as f:
    sep = pickle.load(f)

all_data = {"October": oct, "September": sep}

# UI
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.output_image("icon_img", height="60px"),
            ui.input_select(
                "username",
                "Choose your user",
                choices=[
                    "COUNTY",
                    "BOM",
                    "CAMINO",
                    "EDHS",
                    "GOAK",
                    "GTRAIL",
                    "LAKETAHOE",
                    "LATROBE",
                    "MOTHER",
                    "PIONEER",
                    "PLACERV",
                    "POLLOCK",
                    "RESCUE",
                    "SPED",
                    "CHARTER",
                ],
                multiple=False,
            ),
            ui.input_password(
                "secret_key",
                "Enter your District's secret key to access:",
            ),
            ui.input_select(
                "districts",
                "Select District to Display",
                choices=[],
                # choices=list(districts.keys()),
                multiple=False,
            ),
            ui.input_select(
                "reports",
                "Select Report Type",
                choices=list(reports.keys()),
                multiple=False,
            ),
            ui.card(
                ui.input_radio_buttons(
                    "rb",
                    "Choose one:",
                    {
                        "table": "Table (static table with color coding)",
                        "dataframe": "Dataframe (enables sorting and scrolling)",
                    },
                ),
            ),
            ui.input_select(
                "date_range",
                "Select Date",
                choices=list(all_data.keys()),
                multiple=False,
            ),
            ui.output_text("date_note"),
            ui.input_dark_mode(id="mode"),
        ),
        # ui.output_text("report_title"),
        ui.output_text("report_questions"),
        ui.hr(),
        ui.navset_tab(
            ui.nav_panel(
                "Data Table",
                ui.output_table("table2"),
                ui.output_data_frame("dataframe2"),
            ),
            ui.nav_panel("Graphs", ui.output_plot("all_charts", height="650px")),
        ),
    ),
    title="EDCOE Attendance Works",
    id="page",
)


# Server
def server(input, output, session):

    @render.image
    def icon_img():
        return {"src": "icon.png", "height": "60px"}

    @reactive.effect
    @reactive.event(input.make_light)
    def _():
        ui.update_dark_mode("light")

    @reactive.effect
    @reactive.event(input.make_dark)
    def _():
        ui.update_dark_mode("dark")

    @render.text
    def date_note():
        notes = {
            "September": "Data is for time period Aug 2024 - Sep 6, 2024",
            "October": "Data is for time period Aug 2024 - Oct 4, 2024",
        }
        return notes.get(input.date_range())

    @reactive.effect
    # @render.text
    def update_select():
        input_key = input.secret_key().encode("utf-8")
        username = input.username()
        if username == "COUNTY":
            if bcrypt.checkpw(input_key, os.getenv("SECRET_KEY_EDCOE").encode("utf-8")):
                ui.update_select("districts", choices=list(districts.keys()))
                ui.update_select("username", choices=['COUNTY'])
        elif username == "BOM":
            if bcrypt.checkpw(input_key, os.getenv("SECRET_KEY_BOM").encode("utf-8")):
                ui.update_select("districts", choices=["Black Oak Mine Unified"])
                ui.update_select("username", choices=['BOM'])
        elif username == "CAMINO":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_CAMINO").encode("utf-8")
            ):
                ui.update_select("districts", choices=["Camino Unified"])
                ui.update_select("username", choices=['CAMINO'])
        elif username == "EDHS":
            if bcrypt.checkpw(input_key, os.getenv("SECRET_KEY_EDHS").encode("utf-8")):
                ui.update_select("districts", choices=["El Dorado Union High"])
                ui.update_select("username", choices=['EDHS'])
        elif username == "GOAK":
            if bcrypt.checkpw(input_key, os.getenv("SECRET_KEY_GOAK").encode("utf-8")):
                ui.update_select("districts", choices=["Gold Oak Union Elementary"])
                ui.update_select("username", choices=['GOAK'])
        elif username == "GTRAIL":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_GTRAIL").encode("utf-8")
            ):
                ui.update_select("districts", choices=["Gold Trail Union Elementary"])
                ui.update_select("username", choices=['GTRAIL'])
        elif username == "LAKETAHOE":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_LAKETAHOE").encode("utf-8")
            ):
                ui.update_select("districts", choices=["Lake Tahoe Unified"])
                ui.update_select("username", choices=['LAKETAHOE'])
        elif username == "LATROBE":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_LATROBE").encode("utf-8")
            ):
                ui.update_select("districts", choices=["Latrobe"])
                ui.update_select("username", choices=['LATROBE'])
        elif username == "MOTHER":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_MOTHER").encode("utf-8")
            ):
                ui.update_select("districts", choices=["Mother Lode Union Elementary"])
                ui.update_select("username", choices=['MOTHER'])
        elif username == "PIONEER":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_PIONEER").encode("utf-8")
            ):
                ui.update_select("districts", choices=["Pioneer Union Elementary"])
                ui.update_select("username", choices=['PIONEER'])
        elif username == "PLACERV":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_PLACERV").encode("utf-8")
            ):
                ui.update_select("districts", choices=["Placerville Union Elementary"])
                ui.update_select("username", choices=['PLACERV'])
        elif username == "POLLOCK":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_POLLOCK").encode("utf-8")
            ):
                ui.update_select(
                    "districts",
                    choices=["Pollock Pines Elementary", "Silver Fork Elementary"],
                )
                ui.update_select("username", choices=['POLLOCK'])
        elif username == "RESCUE":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_RESCUE").encode("utf-8")
            ):
                ui.update_select("districts", choices=["Rescue Union Elementary"])
                ui.update_select("username", choices=['RESCUE'])
        elif username == "SPED":
            if bcrypt.checkpw(input_key, os.getenv("SECRET_KEY_SPED").encode("utf-8")):
                ui.update_select("districts", choices=["Edcoe Sped"])
                ui.update_select("username", choices=['SPED'])
        elif username == "CHARTER":
            if bcrypt.checkpw(
                input_key, os.getenv("SECRET_KEY_CHARTER").encode("utf-8")
            ):
                ui.update_select("districts", choices=["Edcoe Charter"])
                ui.update_select("username", choices=['CHARTER'])
        else:
            ui.update_select("districts", choices=[])

    @output
    @render.text
    def report_questions():
        return question_titles[input.reports()]

    @output
    @render.table
    def table2():
        if input.rb() == "dataframe":
            return
        if not input.districts():
            return
        selected_month = input.date_range()
        selected_district = districts[input.districts()]
        selected_reports = reports[input.reports()]
        if all_data[selected_month][selected_district][selected_reports] is not None:
            all_columns = list(
                all_data[selected_month][selected_district][selected_reports].columns
            )
            subsets = get_subsets(all_columns)

            if selected_reports != "bygrade3yrs":
                return style_table(
                    all_data[selected_month][selected_district][selected_reports],
                    subsets,
                )

            return all_data[selected_month][selected_district][selected_reports]

    @render.data_frame
    def dataframe2():
        if input.rb() == "table":
            return
        if not input.districts():
            return
        selected_month = input.date_range()
        selected_district = districts[input.districts()]
        selected_reports = reports[input.reports()]
        if all_data[selected_month][selected_district][selected_reports] is not None:
            all_columns = list(
                all_data[selected_month][selected_district][selected_reports].columns
            )
            subsets = get_subsets(all_columns)

            return style_dataframe(
                all_data[selected_month][selected_district][selected_reports]
            )

    @output
    @render.plot
    def all_charts():
        if not input.districts():
            return
        selected_month = input.date_range()
        selected_district = districts[input.districts()]
        selected_reports = reports[input.reports()]
        plotdata = all_data[selected_month][selected_district][selected_reports]
        if selected_reports in ["bygrade", "bygrade_prior", "bygrade_two_yr_prior"]:
            grade_race_gender_charts(
                plotdata,
                [
                    "What percentage of students in each grade level\nhave moderate or severe chronic absence?",
                    "What percentage of students in each grade level\nhave satisfactory attendance?",
                ],
            )
        elif selected_reports == "bygrade3yrs":
            grade_3yr_charts(plotdata)
        elif selected_reports == "byrace":
            grade_race_gender_charts(
                plotdata,
                [
                    "What percentage of students in each race/ethnicity have\nmoderate or severe chronic absence?",
                    "What percentage of students in each race/ethnicity have\nsatisfactory attendance?",
                ],
                label_rot=90,
            )
        elif selected_reports == "bygender":
            plotdata = plotdata.rename(index={"M": "Male", "F": "Female"})
            grade_race_gender_charts(
                plotdata,
                [
                    "What percentage of boys and girls have moderate or severe\nchronic absence?",
                    "What percentage of boys and girls have\nsatisfactory attendance?",
                ],
            )
        elif selected_reports == "byracegender":
            plotdata = plotdata.iloc[:-1, :]
            grade_race_gender_charts(
                plotdata,
                [
                    "What percentage of students have moderate or\nsevere chronic absence by race/ethnicity and gender?",
                    "What percentage of students have satisfactory\nattendance by race/ethnicity and gender?",
                ],
                label_rot=90,
            )

        elif selected_reports in ["byIEP", "byEngLearner", "byFreeReduced"]:
            titles = {
                "byIEP": [
                    "Do students with special needs have higher rates of\nmoderate or severe chronic absence?",
                    "What are the attendance patterns of students with\nspecial needs?",
                ],
                "byEngLearner": [
                    "Do English Learners have different rates of moderate or severe\nchronic absence than students not learning English?",
                    "What are the attendance patterns of English Learners?",
                ],
                "byFreeReduced": [
                    "Do students with free/reduced lunch status have higher\nrates of chronic or severe chronic absence?",
                    "What are the attendance patterns of students with\nFree/Reduced Lunch status?",
                ],
            }
            sp_eng_fre_charts(
                plotdata,
                titles[selected_reports],
            )

        elif selected_reports == "byracegrade":
            race_grade_charts(plotdata)

        elif selected_reports == "absence_types":
            absence_gender_charts(plotdata)
        elif selected_reports == "absence_by_gender":
            absence_gender_charts(plotdata, label_rot=90)

        elif selected_reports == "absence_by_grade":
            absence_grade_charts(
                plotdata,
                "What is the percentage of each absence type, by grade, for chronically absent, non-chronically absent and all students?",
                label_rot=90,
                ha="center",
                label_bars=False,
            )
        elif selected_reports == "absence_by_race":
            absence_grade_charts(
                plotdata,
                "What is the percentage of each absence type, by ethnicity for chronically absent, non-chronically absent and students overall?",
                label_rot=60,
                ha="right",
            )
        elif selected_reports == "absence_by_racegender":
            absence_grade_charts(
                plotdata,
                "Among chronically absent students, what is the percentage of each absence type, by race/ethnicity and gender?",
                label_rot=60,
                ha="right",
            )
        elif selected_reports == "absence_by_racegender_not":
            absence_grade_charts(
                plotdata,
                "Among non-chronically absent students, what is the percentage of each absence type, by race/ethnicity and gender?",
                label_rot=60,
                ha="right",
            )
        elif selected_reports == "part1_notifications":
            notification_plot(plotdata)
        elif selected_reports == "part2_notifications":
            notification_plot2(plotdata)
        elif selected_reports == "part3_notifications":
            notification_plot3(plotdata)
        elif selected_reports == "part1_grade_notifications":
            notif_grade_plot(plotdata)
        elif selected_reports == "part2_grade_notifications":
            notif_grade_plot2(plotdata)
        elif selected_reports == "part3_grade_notifications":
            notif_grade_plot3(plotdata)

        elif selected_reports == "heatmap":
            heatmap_plot(plotdata)


app = App(app_ui, server)
