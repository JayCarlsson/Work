import xlsxwriter
import datetime

workbook = xlsxwriter.Workbook('Payroll.xlsx')
worksheet = workbook.add_worksheet('Payroll')
worksheet_schedule = workbook.add_worksheet('Schedule')

# Set the default column width
worksheet.set_column('A:AAA', 20)
worksheet_schedule.set_column('A:AAA', 20)
# Set the default row height
worksheet.set_default_row(25)
worksheet_schedule.set_default_row(25)
# Set the alignment for the entire worksheet
worksheet.autofit(max_width=20)
worksheet_schedule.autofit(max_width=20)

payroll = [
    ['Kr/Hour', 157.16],
    ['OB1', 16.11],
    ['OB2', 39.92]
]

paytable_we = [
    ['X', 0, 0],
    ['EX1', 1, 5.25],
    ['EX2', 0, 5.25],
    ['EX3', 0, 5.25],
    ['EX4', 1, 5.25],
    ['Gr1', 6, 2],
    ['Gr2', 5, 2],
    ['Li1', 5, 3.25]
]

schedule = [
    ['EX2', str(datetime.date(2025, 5, 2))],
    ['Gr1', str(datetime.date(2025, 5, 3))],
    ['X', str(datetime.date(2025, 5, 9))],
    ['X', str(datetime.date(2025, 5, 13))],
    ['Gr1', str(datetime.date(2025, 5, 16))],
    ['Gr2', str(datetime.date(2025, 5, 17))],
    ['Gr2', str(datetime.date(2025, 5, 23))],
    ['Li1', str(datetime.date(2025, 5, 24))],
    ['Li1', str(datetime.date(2025, 5, 28))],
    ['Gr1', str(datetime.date(2025, 5, 30))],
    ['Gr1', str(datetime.date(2025, 5, 31))]
]

row = 0
col = 0
i = 0

worksheet.write(row, col, 'Place')
worksheet.write(row, col + 1, 'Hours')
worksheet.write(row, col + 2, 'Date')
worksheet.write(row, col + 3, 'Kr/Hour')
worksheet.write(row, col + 4, 'OB1')
worksheet.write(row, col + 5, 'OB2')
worksheet.write(row, col + 6, 'Total')
row += 1


for item in schedule:
    while i <= len(paytable_we)-1:
        if item[0] in paytable_we[i]:
            worksheet.write(row, col, item[0])
            worksheet.write(row, col + 1, paytable_we[i][1]+paytable_we[i][2])
            worksheet.write(row, col + 2, item[1])
            row += 1
            i = len(paytable_we)
        i += 1
    i = 0

worksheet.write(row + 1, col, 'Hours')
worksheet.write(row + 1, col + 1, '=SUM(B2:B12)')
worksheet.write(row + 2, col, 'Total Payroll')
worksheet.write(row + 2, col + 1, '=SUM(G2:G12)')
worksheet.write(row + 3, col, 'Pay after taxes')
worksheet.write(row + 3, col + 1, '=B15*0.66')

row = 1
ph = 0
ob1 = 0
ob2 = 0

for item in schedule:
    while i <= len(paytable_we)-1:
        if item[0] in paytable_we[i]:
            ph = (paytable_we[i][1]+paytable_we[i][2])*payroll[0][1]
            ob1 = paytable_we[i][1]*payroll[1][1]
            ob2 = paytable_we[i][2]*payroll[2][1]
            worksheet.write(row, col + 3, ph)
            worksheet.write(row, col + 4, ob1)
            worksheet.write(row, col + 5, ob2)
            worksheet.write(row, col + 6, sum([ph, ob1, ob2]))
            row += 1
            i = len(paytable_we)
        i += 1
    i = 0
row = 0

worksheet.write(row + 18, col, 'test')

workbook.close()



# Set a format for the excelfile
workbook = xlsxwriter.Workbook('Schedule.xlsx')
worksheet = workbook.add_worksheet()

# Set the column width
worksheet.set_column('A:AAA', 25)
# Set the row height
worksheet.set_row(0, 20)
# Set the header format
header_format = workbook.add_format({
    'bold': True,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFA07A'
})
# Set the cell format
cell_format = workbook.add_format({
    'border': 1,
    'align': 'center',
    'valign': 'vcenter'
})
