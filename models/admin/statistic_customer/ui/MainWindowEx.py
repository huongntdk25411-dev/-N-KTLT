import json
import pandas as pd
import seaborn as sns

from PyQt6.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from models.admin.statistic_customer.ui.MainWindow import Ui_MainWindow


class MainWindowEx(Ui_MainWindow):

    def __init__(self):
        self.df = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.MainWindow = MainWindow

        self.loadData()
        self.showKPIs()
        self.showCharts()

    def show(self):
        self.MainWindow.show()

# ===============================
# LOAD DATA
# ===============================

    def loadData(self):

        with open('../data/bookings.json', "r", encoding="utf-8") as f:
            data = json.load(f)

        self.df = pd.DataFrame(data)

        # convert date
        self.df["date"] = pd.to_datetime(
            self.df["date"], format="%d/%m/%Y"
        )

        # convert hour
        self.df["hour"] = pd.to_datetime(
            self.df["time"], format="%H:%M"
        ).dt.hour


# ===============================
# KPI DASHBOARD
# ===============================

    def showKPIs(self):

        today = pd.Timestamp.today().normalize()

        total_booking = len(self.df)

        today_booking = len(
            self.df[self.df["date"] == today]
        )

        current_week = today.isocalendar().week

        week_booking = len(
            self.df[self.df["date"].dt.isocalendar().week == current_week]
        )

        popular_location = self.df["place"].value_counts().idxmax()

        popular_concept = self.df["concept"].value_counts().idxmax()

        popular_hour = self.df["hour"].mode()[0]

        self.labelTotalBookingDesc.setText(str(total_booking))
        self.labelTodayBookingDesc.setText(str(today_booking))
        self.labelWeekBookingDesc.setText(str(week_booking))

        self.labelPopularLocationValue.setText(popular_location)
        self.labelPopularConceptDesc.setText(popular_concept)
        self.labelPopularTimeDesc.setText(f"{popular_hour}:00")


# ===============================
# CHART CONTROLLER
# ===============================

    def showCharts(self):

        self.showWeeklyChart()
        self.showConceptChart()
# ===============================
# BAR CHART BOOKING PER WEEK
# ===============================

    def showWeeklyChart(self):

        today = pd.Timestamp.today()
        current_week = today.isocalendar().week

        last_week_df = self.df[
            self.df["date"].dt.isocalendar().week == current_week - 1
            ]

        # lấy thứ trong tuần
        daily = last_week_df.groupby(
            last_week_df["date"].dt.day_name()
        ).size()

        order = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]

        daily = daily.reindex(order, fill_value=0)

        # label hiển thị ngắn
        labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)

        ax = figure.add_subplot(111)

        colors = [
            "#4DB6E2", "#64B5F6", "#81C784",
            "#FFD54F", "#FFB74D", "#E57373", "#BA68C8"
        ]

        bars = ax.bar(
            labels,
            daily.values,
            color=colors,
            width=0.6
        )

        # hiển thị số trên cột
        for bar in bars:
            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.1,
                int(height),
                ha='center',
                fontsize=10,
                fontweight="bold"
            )

        ax.set_title(
            "Số lượng người đặt lịch chụp ảnh trong tuần qua",
            fontsize=14,
            fontweight="bold",
            pad=15
        )

        ax.set_xlabel("Ngày trong tuần", fontsize=11)
        ax.set_ylabel("Số lượng người đặt lịch", fontsize=11)

        ax.grid(axis="y", linestyle="--", alpha=0.5)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        figure.patch.set_facecolor("white")
        ax.set_facecolor("white")

        figure.tight_layout()

        layout = self.groupBoxWeeklyBooking.layout()

        if layout is None:
            layout = QVBoxLayout()
            self.groupBoxWeeklyBooking.setLayout(layout)

        layout.addWidget(canvas)
# ===============================
# PIE CHART CONCEPT
# ===============================

    def showConceptChart(self):

        concept = self.df["concept"].value_counts()
        labels = [
            "Ảnh nhóm",
            "HSSV\n(Kỷ yếu)",
            "Sự kiện",
            "Gia đình",
            "Ảnh thẻ",
            "Cặp đôi",
            "Cá nhân"
        ]

        figure = Figure(figsize=(5, 4))
        canvas = FigureCanvas(figure)

        ax = figure.add_subplot(111)

        colors = [
            "#4DB6E2",
            "#81C784",
            "#FFD54F",
            "#FF8A65",
            "#BA68C8",
            "#90A4AE",
            "#F06292"
        ]

        wedges, texts, autotexts = ax.pie(
            concept.values,
            labels=labels[:len(concept)],
            autopct="%1.1f%%",
            startangle=90,
            colors=colors[:len(concept)],
            pctdistance=0.75,
            wedgeprops={
                "edgecolor": "white",
                "linewidth": 2
            }
        )

        # chỉnh font %
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight("bold")

        ax.set_title(
            "Tỷ lệ concept được đặt",
            fontsize=14,
            fontweight="bold",
            pad=15
        )

        ax.axis("equal")

        figure.patch.set_facecolor("white")

        figure.tight_layout()

        layout = self.groupBox_4.layout()

        if layout is None:
            layout = QVBoxLayout()
            self.groupBox_4.setLayout(layout)

        layout.addWidget(canvas)

