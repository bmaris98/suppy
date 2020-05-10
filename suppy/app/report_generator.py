import pandas as pd
from pathlib import Path
import matplotlib
import webbrowser
import matplotlib.pyplot as plt
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from suppy.utils.stats_constants import BUFFER, CONVERGENCE, CUSTOM, DIVERGENCE, END, RANDOM_ERROR, REPAIR, START, TEST, TRANSPORT
from fpdf import FPDF

class ReportGenerator:

    def __init__(self, project_name, stats):
        self._data_path = Path(__file__).parent / '../data'
        self._project_name = project_name
        self._stats = stats
        self._transform_df = pd.DataFrame()
        self._verification_df = pd.DataFrame()
        self._repair_df = pd.DataFrame()
        self._transport_df = pd.DataFrame()
        self._cost_df = pd.DataFrame()
        self._pie_areas = ['Transport', 'Transform', 'Repair', 'Testing']
        self._costs = self._load_cost_df()
        explode = (0, 0, 0, 0)

        fig1, ax1 = plt.subplots()
        ax1.pie(self._costs, explode=explode, labels=self._pie_areas, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        self._image_path = (self._data_path / ('tmp/export/' + project_name + '.png')).resolve()
        self._pdf_path = (self._data_path / ('tmp/export/' + project_name + '.pdf')).resolve()
        plt.savefig(self._image_path)
        self._create_pdf(project_name)
        
        webbrowser.open_new(str(self._pdf_path))

    def _create_pdf(self, project_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_xy(0, 0)
        pdf.set_font('arial', 'B', 12)
        pdf.cell(60)
        pdf.cell(75, 40, "Cost Distribution", 0, 2, 'C')
        pdf.cell(-30)
        pdf.image(str(self._image_path), x = 0, y = 45, w = 0, h = 0, type = '', link = '')
        pdf.output(str(self._pdf_path), 'F')

    def _load_cost_df(self):
        transport_cost = 0
        custom_cost = 0
        repair_cost = 0
        verification_cost = 0
        for data in self._stats['stats']:
            if data['type'] == TRANSPORT:
                transport_cost += data['total_cost']
            if data['type'] == CUSTOM:
                custom_cost += data['total_calibration_cost']
                custom_cost += data['total_cost']
            if data['type'] == REPAIR:
                repair_cost += data['total_calibration_cost']
                repair_cost += data['total_cost']
            if data['type'] == TEST:
                verification_cost += data['total_calibration_cost']
                verification_cost += data['total_cost']
        return [transport_cost, custom_cost, repair_cost, verification_cost]

# df = pd.DataFrame()
# df['Question'] = ["Q1", "Q2", "Q3", "Q4"]
# df['Charles'] = [3, 4, 5, 3]
# df['Mike'] = [3, 3, 4, 4]

# title("Professor Criss's Ratings by Users")
# xlabel('Question Number')
# ylabel('Score')

# c = [2.0, 4.0, 6.0, 8.0]
# m = [x - 0.5 for x in c]

# xticks(c, df['Question'])

# bar(m, df['Mike'], width=0.5, color="#91eb87", label="Mike")
# bar(c, df['Charles'], width=0.5, color="#eb879c", label="Charles")

# legend()
# axis([0, 10, 0, 8])
# savefig('barchart.png')

# pdf = FPDF()
# pdf.add_page()
# pdf.set_xy(0, 0)
# pdf.set_font('arial', 'B', 12)
# pdf.cell(60)
# pdf.cell(75, 10, "A Tabular and Graphical Report of Professor Criss's Ratings by Users Charles and Mike", 0, 2, 'C')
# pdf.cell(90, 10, " ", 0, 2, 'C')
# pdf.cell(-40)
# pdf.cell(50, 10, 'Question', 1, 0, 'C')
# pdf.cell(40, 10, 'Charles', 1, 0, 'C')
# pdf.cell(40, 10, 'Mike', 1, 2, 'C')
# pdf.cell(-90)
# pdf.set_font('arial', '', 12)
# for i in range(0, len(df)):
#     pdf.cell(50, 10, '%s' % (df['Question'].iloc[i]), 1, 0, 'C')
#     pdf.cell(40, 10, '%s' % (str(df.Mike.iloc[i])), 1, 0, 'C')
#     pdf.cell(40, 10, '%s' % (str(df.Charles.iloc[i])), 1, 2, 'C')
#     pdf.cell(-90)
# pdf.cell(90, 10, " ", 0, 2, 'C')
# pdf.cell(-30)
# pdf.image('barchart.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
# pdf.output('test.pdf', 'F')