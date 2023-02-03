
from pandas import ExcelWriter
import os, csv, json
import pandas as pd
from openpyxl import Workbook as WB
from openpyxl.chart import BarChart, Series, Reference

class Workbook:
    def __init__(self, name):
        self.sheets ={}
        self.workbook_name=f'{name}'
        self.writer = pd.ExcelWriter(name, engine='xlsxwriter')
    def write_csv(self,fn, rows):
        with open(fn, 'w', newline='') as f:
            _writer = csv.writer(f)
            for row in rows:
                _writer.writerow(row)
    def write_workbook(self):

        # writer = ExcelWriter(self.workbook_name)
        # print(os.getcwd())
        # for k,v in self.sheets.items():
        #     if type(v) == str:
        #         print(v)
        #
        #     else:
        #         v.to_excel(writer, k)

        self.writer.save()
        print('\n'.join([x for x in self.writer.sheets.keys()]))
    def build_csv_sheet(self, sheetname,data):
        print(f"{sheetname}.csv")
        self.write_csv(f"{sheetname}.csv", data)
        df_csv = pd.read_csv(f"{sheetname}.csv")
        df_csv.to_excel(self.writer, f"{sheetname}", index=False)

        os.remove(f"{sheetname}.csv")

    def build_bar_chart(self, report_data,indexes,sheet_name="sheet", title="Chart", y_axis_title="y-axis", x_axis_title="x_axis"):
        # Some sample data to plot.
        # farm_1 = {'Apples': 10, 'Berries': 32, 'Squash': 21, 'Melons': 13, 'Corn': 18}
        # farm_2 = {'Apples': 15, 'Berries': 43, 'Squash': 17, 'Melons': 10, 'Corn': 22}
        # farm_3 = {'Apples': 6, 'Berries': 24, 'Squash': 22, 'Melons': 16, 'Corn': 30}
        # farm_4 = {'Apples': 12, 'Berries': 30, 'Squash': 15, 'Melons': 9, 'Corn': 15}

        # data = [farm_1, farm_2, farm_3, farm_4]
        # index = ['Farm 1', 'Farm 2', 'Farm 3', 'Farm 4']

        # Create a Pandas dataframe from the data.
        # _writer = pd.ExcelWriter("tmp.xlsx", engine='xlsxwriter')
        df = pd.DataFrame(report_data, index=indexes)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        # sheet_name = 'Sheet1'
        df.to_excel(self.writer, sheet_name=sheet_name)

        # Access the XlsxWriter workbook and worksheet objects from the dataframe.
        # workbook = self.writer.book
        worksheet = self.writer.sheets[sheet_name]

        # Create a chart object.
        chart = self.writer.book.add_chart({'type': 'column'})
        chart.title_name=title
        # Some alternative colors for the chart.
        colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00']

        # Configure the series of the chart from the dataframe data.
        for col_num in range(1, len(report_data[0].keys()) + 1):
            chart.add_series({
                'name': [sheet_name, 0, col_num],
                'categories': [sheet_name, 1, 0, len(indexes), 0],
                'values': [sheet_name, 1, col_num, len(indexes), col_num],
                'fill': {'color': colors[col_num - 1]},
                'overlap': -10,
            })

        # Configure the chart axes.
        chart.set_x_axis({'name': x_axis_title})
        chart.set_y_axis({'name': y_axis_title, 'major_gridlines': {'visible': False}})


        index = len(report_data[0].keys())
        if index> 74: #the logic wont accept more than 74 columns, can be fixed by reworking the starting point calculation because excel is weird
            raise Exception("Cannot exceed 74 columns")
        # index = 74
        starting_point = ['']
        alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
        alpha_index = 0
        for i in range(0, index + 3):
            if alpha_index == len(alpha) -\
                    1:
                starting_point[-1] = alpha[0]
                starting_point.append(alpha[0])
                alpha_index = 0
                continue
            else:
                starting_point[-1] = alpha[alpha_index]

            alpha_index += 1
        # print(starting_point)
            # Insert the chart into the worksheet.
        worksheet.insert_chart(''.join(starting_point)+'1', chart)
        self.writer.sheets[sheet_name]=worksheet
        # self.sheets[sheet_name]=df
        # ws.add_chart(chart1, ''.join(starting_point)+'1')
        # Close the Pandas Excel writer and output the Excel file.
        # writer.save()
        # plotdata = pd.DataFrame(
        #     report_data,
        #     index=indexes)
        # # Plot a bar chart
        # plotdata.plot(kind="bar")
        # # self.sheets['fuckery']=plotdata
        # writer = ExcelWriter(self.workbook_name)
        # plotdata.to_excel(writer,sheet_name="fick")
        # workbook = writer.book
        # worksheet = writer.sheets['fick']
        #
        # chart = workbook.add_chart({'type': 'column'})
        #
        # writer.save()
        # wb = WB(write_only=True)
        # ws = wb.create_sheet()
        # for row in report_data:
        #     ws.append(row)
        # chart1 = BarChart()
        # chart1.type = "col"
        # chart1.style = 10
        # chart1.title = title
        # chart1.y_axis.title = y_axis_title
        # chart1.x_axis.title = x_axis_title
        #
        # data = Reference(ws, min_col=2, min_row=1, max_row=len(report_data), max_col=len(report_data[0]))
        # cats = Reference(ws, min_col=1, min_row=2, max_row=len(report_data))
        # chart1.add_data(data, titles_from_data=True)
        # chart1.set_categories(cats)
        # chart1.shape = 4
        #
        # index = len(report_data[0])
        # if index> 74: #the logic wont accept more than 74 columns, can be fixed by reworking the starting point calculation because excel is weird
        #     raise Exception("Cannot exceed 74 columns")
        # # index = 74
        # starting_point = ['']
        # alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        #          'U', 'V', 'W', 'X', 'Y', 'Z']
        # alpha_index = 0
        # for i in range(0, index + 3):
        #     if alpha_index == len(alpha) -\
        #             1:
        #         starting_point[-1] = alpha[0]
        #         starting_point.append(alpha[0])
        #         alpha_index = 0
        #         continue
        #     else:
        #         starting_point[-1] = alpha[alpha_index]
        #
        #     alpha_index += 1
        # # print(starting_point)
        #
        # ws.add_chart(chart1, ''.join(starting_point)+'1')
        # wb.save("bar.xlsx")