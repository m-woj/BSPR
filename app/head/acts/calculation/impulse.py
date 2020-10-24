from typing import Tuple
from statistics import mean
from ..templates import CalculationActTemplate
from ....core import Impulse, ImpulseOutput
from ....gui.frames import ResultsFrame


class ImpulseAct(CalculationActTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fuel_name = args[1]
        data = args[2]
        config = args[3]
        output = Impulse(data, config).get_results()
        self.generate_report(self.frame, output)

    def generate_report(self, 
        frame: ResultsFrame, output: ImpulseOutput):
        title = frame.create_title(frame.interior, 
            f"WYNIKI OBLICZEŃ IMPULSU JEDNOSTKOWEGO DLA PALIWA {self.fuel_name}")
        data = self.get_table_data(output)
        table = frame.create_table(frame.interior, data)

        title.pack(fill="both")
        table.pack(pady=20)

    @staticmethod
    def get_table_data(output: ImpulseOutput) -> Tuple[tuple, ...]:
        headings = ("Nr.\npomiaru", "Impuls jednostkowy\n[MN*s/kg]",
            "Impuls całkowity\n[N*s]", "Śr. kryt.\ndyszy [mm]",
            "Dł. komory\nspalania [mm]", "Śr. komory\nspalania [mm]")
        data = [(i, round(item.unit_impulse / 1000_000, 4),
            round(item.total_impulse / 1000_000, 4),
            item.jet_d, item.chamber_length,
            item.chamber_d)
            for i, item in enumerate(output, start=1)]
        return tuple((headings, *data))
