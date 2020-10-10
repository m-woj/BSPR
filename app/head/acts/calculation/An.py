from typing import Tuple
import math
import tkinter as tk
from ..templates import CalculationActTemplate
from ....core import An, AnOutplut
from ....gui.frames import ResultsFrame


class AnAct(CalculationActTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fuel_name = args[1]
        data = args[2]
        config = args[3]
        output = An(data, config).get_results()
        self.generate_report(self.frame, output)

    def generate_report(self, 
        frame: ResultsFrame, output: AnOutplut):
        title = frame.create_title(frame.interior, 
            f"WYNIKI OBLICZEŃ DLA PALIWA {self.fuel_name}")

        plotfig = self.draw_approx_plot(frame, output)

        final_output = tk.Label(frame.interior, text=f"A = {output.A:.3e} m/(s⋅Pa^n)\
            n = {output.n:.3g}", font=("bold", 20))

        data = self.get_table_data(output)
        table = frame.create_table(frame.interior, data)

        title.pack(fill="both")
        plotfig.pack(expand=1, fill="both")
        final_output.pack(pady=10)
        table.pack()

    @staticmethod
    def get_table_data(output: AnOutplut) -> Tuple[tuple, ...]:
        headings = ("Nr.\npomiaru", "p\n[MPa]", "u\n[mm/s]","t0\n[ms]", "tk\n[ms]", 
            "tc\n[ms]", "Ipk\n[MPa⋅s]", "Śr. kryt.\ndyszy [mm]", "t chwil.\n[ms]")
        data = [(i, round(item.p/1000, 3), round(item.u*1000, 2), *item.times,
            round(item.Ipk/1000_000, 3), item.jet_d, item.point_time)
                for i, item in enumerate(output.surveys_details, start=1)]
        return tuple((headings, *data))

    @staticmethod
    def get_plot_cords(output: AnOutplut) -> Tuple[tuple, tuple]:
        xs = tuple(math.log(survey.p) for survey in output.surveys_details)
        ys = tuple(math.log(survey.u) for survey in output.surveys_details)
        return xs, ys

    def draw_approx_plot(self, frame, output):
        plotfig = frame.create_plot(frame.interior)
        plotfig.figure.subplots_adjust(left=0.095, top=0.93)
        plot = plotfig.add_subplot(111)
        plot.set_title("Wykres zależności szybkości spalania "
            "SPR od ciśnienia w komorze spalania")
        plot.set_xlabel("ln(p)")
        plot.set_ylabel("ln(u)")
        plot.grid()

        cords = self.get_plot_cords(output)
        points = plot.scatter(*cords, color="red")
        for i in range(len(cords[0])):
            plot.annotate(i+1, (cords[0][i], cords[1][i]))

        A_log = math.log(output.A)
        n = output.n
        f = lambda x: A_log + n*x
        xs = cords[0][0], cords[0][-1]
        ys = f(xs[0]), f(xs[1])
        line = plot.axline((xs[0], ys[0]), (xs[1], ys[1]), ls="--")
        plot.legend((points, line), ("Pomiar", "Aproksymacja"))
        return plotfig