import pandas as pd
import os

from scraper import person_ids, person_names, person_schedules, dates

data = {
    "Employment ID": person_ids,
    "Name": person_names,
    "Place": person_schedules,
    "Date": dates
}

sdf = pd.DataFrame(data)
sdf["Place"] = sdf["Place"].astype(str)
sdf["Date"] = sdf["Date"].astype(str)

file_path = 'schedule_test.xlsx'

# Check if file exists and has sheets
if os.path.exists(file_path):
    with pd.ExcelFile(file_path, engine='openpyxl') as reader:
        if not reader.sheet_names:
            # File exists but is empty, just write the new data
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                sdf.to_excel(writer, sheet_name='Sheet1', index=False)
            print(sdf)
            exit()
        else:
            existing_sheets = {sheet: reader.parse(sheet) for sheet in reader.sheet_names}
else:
    existing_sheets = {}

# Update or create sheets based on Employment ID
for emp_id in sdf["Employment ID"].unique():
    sheet_name = f"ID_{emp_id}"
    emp_data = sdf[sdf["Employment ID"] == emp_id]
    if sheet_name in existing_sheets:
        if "Employment ID" in existing_sheets[sheet_name].columns:
            sheet_emp_ids = existing_sheets[sheet_name]["Employment ID"].astype(str).unique()
            if str(emp_id) in sheet_emp_ids:
                combined = pd.concat([existing_sheets[sheet_name], emp_data], ignore_index=True)
                combined = combined.drop_duplicates()
                existing_sheets[sheet_name] = combined
            else:
                new_sheet_name = f"ID_{emp_id}_new"
                existing_sheets[new_sheet_name] = emp_data
        else:
            existing_sheets[sheet_name] = emp_data
    else:
        existing_sheets[sheet_name] = emp_data

with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
    for sheet_name, df in existing_sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(sdf)
