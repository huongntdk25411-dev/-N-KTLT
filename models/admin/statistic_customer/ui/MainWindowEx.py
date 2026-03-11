import json
import pandas as pd
import seaborn as sns

from PyQt6.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from models.admin.statistic_customer.MainWindow import Ui_MainWindow


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

# ==============================
# LOAD DATA
# ==============================

    def loadData(self):

        with open("../data/bookings.json", "r", encoding="utf-8") as f:
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


# ==============================
# KPI DASHBOARD
# ==============================

    def showKPIs(self):

        today = pd.Timestamp.today().normalize()

        # tổng booking
        total_booking = len(self.df)

        # booking hôm nay
        today_booking = len(self.df[self.df["date"] == today])

        # booking tuần
        current_week = today.isocalendar().week
        week_booking = len(
            self.df[self.df["date"].dt.isocalendar().week == current_week]
        )

        # địa điểm phổ biến
        popular_location = self.df["place"].value_counts().idxmax()

        # concept phổ biến
        popular_concept = self.df["concept"].value_counts().idxmax()

        # giờ phổ biến
        popular_hour = self.df["hour"].mode()[0]

        # hiển thị lên UI

        self.labelTotalBookingDesc.setText(str(total_booking))
        self.labelTodayBookingDesc.setText(str(today_booking))
        self.labelWeekBookingDesc.setText(str(week_booking))

        self.labelPopularLocationValue.setText(popular_location)
        self.labelPopularConceptDesc.setText(popular_concept)
        self.labelPopularTimeDesc.setText(f"{popular_hour}:00")


# ==============================
# CHARTS
# ==============================

    def showCharts(self):

        self.showWeeklyChart()
        self.showConceptChart()


# ==============================
# WEEKLY BOOKING CHART
# ==============================

    def showWeeklyChart(self):

        self.df["week"] = self.df["date"].dt.isocalendar().week

        weekly = self.df.groupby("week").size()

        figure = Figure()
        canvas = FigureCanvas(figure)

        ax = figure.add_subplot(111)

        sns.lineplot(
            x=weekly.index,
            y=weekly.values,
            marker="o",
            ax=ax
        )

        ax.set_title("Số lượng booking theo tuần")
        ax.set_xlabel("Tuần")
        ax.set_ylabel("Số booking")

        layout = self.groupBoxWeeklyBooking.layout()

        if layout is None:
            layout = QVBoxLayout()
            self.groupBoxWeeklyBooking.setLayout(layout)

        layout.addWidget(canvas)


# ==============================
# CONCEPT PIE CHART
# ==============================

    def showConceptChart(self):

        concept = self.df["concept"].value_counts()

        figure = Figure()
        canvas = FigureCanvas(figure)

        ax = figure.add_subplot(111)

        ax.pie(
            concept.values,
            labels=concept.index,
            autopct="%1.1f%%"
        )

        ax.set_title("Tỉ lệ concept được đặt")

        layout = self.groupBox_4.layout()

        if layout is None:
            layout = QVBoxLayout()
            self.groupBox_4.setLayout(layout)

        layout.addWidget(canvas)