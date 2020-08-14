from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
from gui.frames.base import BaseFrame


class AddSurveyValuesBaseFrame(BaseFrame):
    def __init__(self, top):
        super().__init__(top)
        self.raw_values = None
        self.survey_plots = []
        self.create_head_section()
        self.create_body_section()
        self.adjust_plot()

    def create_head_section(self):
        self.title = self.create_title('')
        self.title.pack(side="top", fill="x")

    def create_body_section(self):
        scrolled_container, interior = self.create_scrolled_container(self)
        btns_container, self.down_nav_widgets = self.create_down_nav_container()
        self.create_plot_section(interior)

        scrolled_container.pack(side="top", fill="both", expand=1)
        btns_container.pack(side="bottom", fill="x")
        self.top.update_idletasks()

    def create_plot_section(self, top):
        plot_container, survey_plot = self.create_plot(top)
        self.survey_plots.append(survey_plot)
        plot_container.pack()

    @staticmethod
    def create_plot(top, size=(10, 4)):
        plot_container = tk.Frame(top)
        fig = Figure(figsize=size, dpi=100)

        canvas = FigureCanvasTkAgg(fig, master=plot_container)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1, padx=10)

        toolbar = NavigationToolbar2Tk(canvas, plot_container)
        toolbar.update()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1, padx=10)

        survey_plot = fig.add_subplot(111)
        fig.subplots_adjust(left=0.08,
                            bottom=0.12,
                            right=0.99,
                            top=0.99)
        return plot_container, survey_plot

    def set_raw_values(self, values):
        self.raw_values = values

    def adjust_plot(self):
        for plot in self.survey_plots:
            plot.set_xlabel("Czas [ms]")


class AddSurveyPressureValuesFrame(AddSurveyValuesBaseFrame):
    def __init__(self, top):
        super().__init__(top)
        self.title.set_text("IMPORTOWANIE WARTOŚCI UZYSKANYCH Z POMIARU CiśNIENIA")

    def adjust_plot(self):
        super().adjust_plot()
        self.survey_plots[0].set_ylabel("Ciśnienie [MPa]")


class AddSurveyThrustValuesFrame(AddSurveyValuesBaseFrame):
    def __init__(self, top):
        super().__init__(top)
        self.title.set_text("IMPORTOWANIE WARTOŚCI UZYSKANYCH Z POMIARU CIĄGU")

    def adjust_plot(self):
        super().adjust_plot()
        self.survey_plots[0].set_ylabel("Siła ciągu [kN]")


class AddSurveyDoubleValuesFrame(AddSurveyValuesBaseFrame):
    def __init__(self, top):
        self.survey_plots = []
        super().__init__(top)
        self.title.set_text("IMPORTOWANIE WARTOŚCI UZYSKANYCH Z POMIARU CiśNIENIA I CIĄGU")

    def create_plot_section(self, top):
        plot_container1, survey_plot1 = self.create_plot(top)
        plot_container2, survey_plot2 = self.create_plot(top)

        self.survey_plots.append(survey_plot1)
        self.survey_plots.append(survey_plot2)

        plot_container1.pack(side="top", anchor="n")
        plot_container2.pack(side="top", anchor="n")

    def adjust_plot(self):
        super().adjust_plot()
        self.survey_plots[0].set_ylabel("Ciśnienie [MPa]")
        self.survey_plots[1].set_ylabel("Siła ciągu [kN]")
