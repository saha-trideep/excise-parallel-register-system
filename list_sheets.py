import pandas as pd

xls = pd.ExcelFile('Register Format.xlsx')
print('All sheets in the Excel file:')
for i, sheet in enumerate(xls.sheet_names, 1):
    print(f'{i}. {sheet}')
