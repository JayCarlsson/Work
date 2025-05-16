import requests
from bs4 import BeautifulSoup

# Global lists to store data
person_ids = []
person_names = []
person_schedules = []
dates = []

def scrape_schedule(url, identifier, days_in_month):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    # Extract numbers from the identifier and use it as the key in the data dictionary
    current_person_id = "".join(filter(str.isdigit, identifier))

    # Create new lists for the new person
    person_name = "".join(filter(lambda x: not x.isdigit() and x != " ", identifier))
    person_schedule = []
    person_ids_local = []

    sched = soup.find(string={identifier})
    sched = sched.parent.parent.parent
    next_sched = sched

    first_entry = True  # Track the first entry for the second website
    # Check the previous sibling at the beginning of the scrape
    prev_sched = sched.previous_sibling
    if prev_sched:
        child_sched = prev_sched.find("b")
        if child_sched:
            group = child_sched.text.strip()
            if (len(group) == 1 or len(group) == 2 or len(group) == 3 or len(group) == 4) and group.isalpha():
                person_schedule.append(group)
            elif group[-1].isdigit() and group[:-1].isalpha():
                person_schedule.append(group)
            else:
                person_schedule.append(" ")
        s_id = str(prev_sched)
        start_id = s_id.find('id="') + 4
        end_id = s_id.find('">')
        if start_id != -1 and end_id != -1:
            extracted_id = s_id[start_id:end_id]
            if '-' in extracted_id and len(extracted_id.split('-')) == 3:
                person_ids_local.append(extracted_id[5:].replace("_", "", 1))

    for _ in range(days_in_month):  # Adjust the range to match the days in the month
        if next_sched is None:  # Break if there are no more siblings
            break
        next_sched = next_sched.next_sibling
        if next_sched is None:  # Check again to avoid errors
            break
        child_sched = next_sched.find("b")
        if child_sched:
            group = child_sched.text.strip()
            if (len(group) == 1 or len(group) == 2 or len(group) == 3 or len(group) == 4) and group.isalpha():
                person_schedule.append(group)
            elif group[-1].isdigit() and group[:-1].isalpha():
                person_schedule.append(group)
            elif not (first_entry and url.endswith("FD60DBDC-DAC2-44BE-8138-74B530A7726D")):
                person_schedule.append(" ")
        else:
            person_schedule.append(" ")
        s_id = str(next_sched)
        start_id = s_id.find('id="') + 4
        end_id = s_id.find('">')
        if start_id != -1 and end_id != -1:
            extracted_id = s_id[start_id:end_id]
            if '-' in extracted_id and len(extracted_id.split('-')) == 3:
                person_ids_local.append(extracted_id[5:].replace("_", "", 1))

    # Append data to global lists
    person_ids.append(current_person_id)
    person_names.append(person_name)
    person_schedules.append(person_schedule)
    dates.append(person_ids_local)

# Scrape only one website
scrape_schedule("schedule", "id, name", 31)  # May 2025 has 31 days

print("Done scraping")
