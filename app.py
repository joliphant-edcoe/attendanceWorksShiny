from shiny import App, ui, reactive, render
import pickle
from chart_plotting import (
    grade_race_gender_charts,
    sp_eng_fre_charts,
    race_grade_charts,
    absence_gender_charts,
    absence_grade_charts,
    heatmap_plot,
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


with open("all_data.pickle", "rb") as f:
    all_data = pickle.load(f)

# UI
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.output_image("icon_img", height="60px"),
            ui.input_select(
                "districts",
                "Select District to Display",
                choices=list(districts.keys()),
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
            ui.card_footer("Data is for time period Aug 2024 - Sep 6, 2024"),
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

    # @output
    # @render.text
    # def report_title():
    #     return input.reports()

    @output
    @render.text
    def report_questions():
        return question_titles[input.reports()]

    @output
    @render.table
    def table2():
        if input.rb() == "dataframe":
            return
        selected_district = districts[input.districts()]
        selected_reports = reports[input.reports()]
        if all_data[selected_district][selected_reports] is not None:
            all_columns = list(all_data[selected_district][selected_reports].columns)
            subsets = get_subsets(all_columns)

            return style_table(all_data[selected_district][selected_reports], subsets)

    @render.data_frame
    def dataframe2():
        if input.rb() == "table":
            return
        selected_district = districts[input.districts()]
        selected_reports = reports[input.reports()]
        if all_data[selected_district][selected_reports] is not None:
            all_columns = list(all_data[selected_district][selected_reports].columns)
            subsets = get_subsets(all_columns)

            return style_dataframe(all_data[selected_district][selected_reports])

    @output
    @render.plot
    def all_charts():
        selected_district = districts[input.districts()]
        selected_reports = reports[input.reports()]
        plotdata = all_data[selected_district][selected_reports]
        if selected_reports in ["bygrade", "bygrade_prior", "bygrade_two_yr_prior"]:
            grade_race_gender_charts(
                plotdata,
                [
                    "What percentage of students in each grade level\nhave moderate or severe chronic absence?",
                    "What percentage of students in each grade level\nhave satisfactory attendance?",
                ],
            )
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
        elif selected_reports == "heatmap":
            heatmap_plot(plotdata)


app = App(app_ui, server)
