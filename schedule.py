import pandas as pd
import scraper

#existing_file = 'schedule.xlsx'
#check_schedule = pd.read_excel(existing_file)

# Ensure both lists are of the same length
min_length = min(len(scraper.schedule), len(scraper.ids))
schedule = scraper.schedule[:min_length]
ids = scraper.ids[:min_length]
person_id = scraper.person_id[0]
person = scraper.person[0]
print(person_id)
print(person)

# Lists
hours = [
    ['X', 0, 0],
    ['EX1', 1, 5.25],
    ['EX2', 0, 5.25],
    ['EX3', 0, 5.25],
    ['EX4', 1, 5.25],
    ['Gr1', 6, 2],
    ['Gr2', 5, 2],
    ['Li1', 5, 3.25]
]
paytable = [
    ['Kr/Hour', 157.16],
    ['OB1', 16.11],
    ['OB2', 39.92]
]

# Create a DataFrame from the scraped data
df = pd.DataFrame({'Schedule': schedule, 'IDs': ids})
df2 = pd.DataFrame(paytable, columns=['Paytable', 'Amount'])
df3 = pd.DataFrame(hours, columns=['Place', 'OB1', 'OB2'])
df_person_id = pd.DataFrame({'Employment number': [person_id]})

with pd.ExcelWriter('Schedule.xlsx') as writer:
    df_person_id.to_excel(writer, startcol=0, startrow=0, sheet_name=person, index=False)
    df.to_excel(writer, startcol=1, startrow=0, sheet_name=person, index=False)
    df2.to_excel(writer, startcol=3, startrow=0, sheet_name=person, index=False)
    df3.to_excel(writer, startcol=5, startrow=0, sheet_name=person, index=False)

