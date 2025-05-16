import random
import csv
import datetime
import uuid

# Predefined lists for categorical columns
states = ["New", "Assess", "Authorize", "Scheduled", "Implement", "Review", "Closed"]
priorities = ["High", "Moderate", "Low"]
risks = ["High", "Moderate", "Low"]
impacts = ["High", "Moderate", "Low"]
categories = ["Hardware", "Software", "Network", "Database", "Security"]
subcategories = ["Replacement", "Upgrade", "Maintenance", "Configuration", "Access", "Performance"]
teams = ["Network Team", "DBA Team", "App Support", "Security Team"]

# Helper functions
def random_name():
    first_names = ["John", "Jane", "Alex", "Emily", "Chris"]
    last_names = ["Smith", "Doe", "Brown", "Lee", "Wilson"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_datetime(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + datetime.timedelta(seconds=random_seconds)

def generate_short_description():
    actions = ["Upgrade", "Replace", "Configure", "Patch", "Test"]
    items = ["server", "database", "network switch", "application", "firewall"]
    return f"{random.choice(actions)} {random.choice(items)}"

def generate_description():
    return f"{generate_short_description()} to improve performance and reliability."

def generate_reason():
    reasons = [
        "Routine maintenance scheduled.",
        "Critical issue reported by user.",
        "Security vulnerability detected."
    ]
    return random.choice(reasons)

def generate_approval_history(approval, created_on):
    if approval == "Approved":
        approver = random_name()
        approval_date = random_datetime(created_on, datetime.datetime.now())
        return f"Approved by {approver} on {approval_date.strftime('%Y-%m-%d %H:%M:%S')}"
    return ""

# Function to generate a single row with optional specific values
def generate_row(counter, specific_values={}):
    i = counter[0]
    change_number = "CHG" + str(i).zfill(4)
    short_description = generate_short_description()
    description = generate_description()
    
    # Apply specific values or use random choice
    state = specific_values.get('State', random.choice(states))
    priority = specific_values.get('Priority', random.choice(priorities))
    risk = specific_values.get('Risk', random.choice(risks))
    impact = specific_values.get('Impact', random.choice(impacts))
    category = specific_values.get('Category', random.choice(categories))
    subcategory = specific_values.get('Subcategory', random.choice(subcategories))
    
    assigned_to = random_name()
    assignment_group = random.choice(teams)
    created_by = random_name()
    created_on = random_datetime(datetime.datetime(2022, 1, 1), datetime.datetime(2023, 1, 1))
    
    # Logic for dependent fields
    if state in ["New", "Assess"]:
        approval = "Pending"
        approval_history = ""
    else:
        approval = "Approved"
        approval_history = generate_approval_history(approval, created_on)
    
    if state in ["Scheduled", "Implement", "Review", "Closed"]:
        planned_start = random_datetime(created_on, created_on + datetime.timedelta(days=30))
        planned_end = random_datetime(planned_start, planned_start + datetime.timedelta(days=2))
    else:
        planned_start = ""
        planned_end = ""
    
    if state in ["Implement", "Review", "Closed"]:
        actual_start = random_datetime(planned_start, planned_start + datetime.timedelta(hours=1))
        if state in ["Review", "Closed"] or (state == "Implement" and random.random() < 0.5):
            actual_end = random_datetime(actual_start, actual_start + datetime.timedelta(hours=2))
        else:
            actual_end = ""
    else:
        actual_start = ""
        actual_end = ""
    
    sys_id = uuid.uuid4().hex
    sys_updated_on = random_datetime(created_on, datetime.datetime.now())
    sys_updated_by = random_name()
    
    # Format dates as strings
    row = [
        change_number, short_description, description, state, priority,
        assigned_to, assignment_group, created_by,
        created_on.strftime("%Y-%m-%d %H:%M:%S") if created_on else "",
        planned_start.strftime("%Y-%m-%d %H:%M:%S") if planned_start else "",
        planned_end.strftime("%Y-%m-%d %H:%M:%S") if planned_end else "",
        actual_start.strftime("%Y-%m-%d %H:%M:%S") if actual_start else "",
        actual_end.strftime("%Y-%m-%d %H:%M:%S") if actual_end else "",
        category, subcategory, risk, impact, generate_reason(), approval,
        approval_history, sys_id,
        sys_updated_on.strftime("%Y-%m-%d %H:%M:%S"), sys_updated_by
    ]
    counter[0] += 1
    return row

# Main script
num_rows = 100
rows = []
counter = [1]

# Generate initial rows
for _ in range(num_rows):
    row = generate_row(counter)
    rows.append(row)

# Collect used values
used_states = set(row[3] for row in rows)
used_priorities = set(row[4] for row in rows)
used_risks = set(row[15] for row in rows)
used_impacts = set(row[16] for row in rows)
used_categories = set(row[13] for row in rows)
used_subcategories = set(row[14] for row in rows)

# Generate additional rows for missing values
for state in states:
    if state not in used_states:
        row = generate_row(counter, {'State': state})
        rows.append(row)

for priority in priorities:
    if priority not in used_priorities:
        row = generate_row(counter, {'Priority': priority})
        rows.append(row)

for risk in risks:
    if risk not in used_risks:
        row = generate_row(counter, {'Risk': risk})
        rows.append(row)

for impact in impacts:
    if impact not in used_impacts:
        row = generate_row(counter, {'Impact': impact})
        rows.append(row)

for category in categories:
    if category not in used_categories:
        row = generate_row(counter, {'Category': category})
        rows.append(row)

for subcategory in subcategories:
    if subcategory not in used_subcategories:
        row = generate_row(counter, {'Subcategory': subcategory})
        rows.append(row)

# Write to CSV
header = [
    "Change Request Number", "Short Description", "Description", "State", "Priority",
    "Assigned To", "Assignment Group", "Created By", "Created On",
    "Planned Start Date", "Planned End Date", "Actual Start Date", "Actual End Date",
    "Category", "Subcategory", "Risk", "Impact", "Reason", "Approval",
    "Approval History", "sys_id", "sys_updated_on", "sys_updated_by"
]

with open('change_requests.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)