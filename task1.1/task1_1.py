
# debug whole code one by one ~getting wrong result like all fails.

''' 

import pandas as pd
import re

# 🔹 File Paths
marks_file = "/Users/foyezahammed/Desktop/A Algorithm/task1.1/task1_1_marks.csv"
modules_file = "/Users/foyezahammed/Desktop/A Algorithm/task1.1/cs modules.csv"
output_file = "/Users/foyezahammed/Desktop/A Algorithm/task1.1/degree_results.csv"

# ✅ Load Data Safely
try:
    # First, check if the first row contains proper headers
    temp_df = pd.read_csv(marks_file, nrows=5, header=None)
    
    # If first row contains module names (they match expected module format), use it as headers
    first_row_as_headers = temp_df.iloc[0].astype(str).str.contains("UFC").any()

    if first_row_as_headers:
        marks_df = pd.read_csv(marks_file, header=0)  # First row is the header
    else:
        marks_df = pd.read_csv(marks_file, header=None)
    
    modules_df = pd.read_csv(modules_file, header=None, names=["Module Code", "Module Name"])
    
    print("✅ Files loaded successfully!")

except FileNotFoundError:
    print("❌ Error: One or both CSV files not found. Check the file paths.")
    exit()
except pd.errors.EmptyDataError:
    print("❌ Error: One or both CSV files are empty.")
    exit()

# ✅ Rename first column to "Student ID"
marks_df.rename(columns={marks_df.columns[0]: "Student ID"}, inplace=True)

# ✅ If the CSV did not have headers, manually assign correct headers from `cs modules.csv`
if not first_row_as_headers:
    expected_module_count = len(modules_df)
    actual_column_count = marks_df.shape[1] - 1  # Excluding "Student ID"

    if expected_module_count == actual_column_count:
        module_names = modules_df["Module Code"].tolist()
        marks_df.columns = ["Student ID"] + module_names
        print("✅ Module names assigned from `cs modules.csv`.")
    else:
        print("❌ Mismatch: `task1_1_marks.csv` does not match expected column count.")
        print("🔹 Expected Modules:", modules_df["Module Code"].tolist())
        print("🔹 Found in CSV:", marks_df.columns.tolist())
        exit()

# ✅ Convert marks to numeric
marks_df.iloc[:, 1:] = marks_df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# ✅ Extract module credits using regex
def extract_credit_value(module_code):
    match = re.search(r"-(\d+)-", module_code)
    return int(match.group(1)) if match else 0

module_credits = {row["Module Code"]: extract_credit_value(row["Module Code"]) for _, row in modules_df.iterrows()}

# ✅ Identify Level 5 and Level 6 modules
level_5_modules = {code: credits for code, credits in module_credits.items() if '-2' in code}
level_6_modules = {code: credits for code, credits in module_credits.items() if '-3' in code}

# ✅ Check which modules exist in marks_df
valid_level_5_modules = {code: level_5_modules[code] for code in level_5_modules if code in marks_df.columns}
valid_level_6_modules = {code: level_6_modules[code] for code in level_6_modules if code in marks_df.columns}

print("✅ Valid Level 5 Modules:", valid_level_5_modules)
print("✅ Valid Level 6 Modules:", valid_level_6_modules)

# ✅ Calculate Degree Classification for Each Student
students_data = []

for _, row in marks_df.iterrows():
    student_id = row["Student ID"]

    # ✅ Calculate Level 5 Average (Best 100 credits)
    level_5_scores = [(row[module], valid_level_5_modules[module]) for module in valid_level_5_modules if not pd.isna(row[module])]
    level_5_scores.sort(key=lambda x: x[0], reverse=True)  # Sort by highest marks

    best_100_credits = []
    credit_sum = 0
    for mark, credit in level_5_scores:
        if credit_sum + credit <= 100:
            best_100_credits.append((mark, credit))
            credit_sum += credit
        else:
            break

    level_5_average = sum(m * c for m, c in best_100_credits) / sum(c for _, c in best_100_credits) if best_100_credits else 0

    # ✅ Calculate Level 6 Average (All Level 6 Modules)
    level_6_scores = [(row[module], valid_level_6_modules[module]) for module in valid_level_6_modules if not pd.isna(row[module])]
    level_6_average = sum(m * c for m, c in level_6_scores) / sum(c for _, c in level_6_scores) if level_6_scores else 0

    # ✅ Compute Final Aggregate Mark
    final_mark = (3 * level_6_average + level_5_average) / 4

    # ✅ Assign Degree Classification
    if final_mark >= 70:
        classification = "First Class"
    elif final_mark >= 60:
        classification = "Upper Second (2:1)"
    elif final_mark >= 50:
        classification = "Lower Second (2:2)"
    elif final_mark >= 40:
        classification = "Third Class"
    else:
        classification = "Fail"

    students_data.append([student_id, level_5_average, level_6_average, final_mark, classification])

    # ✅ Print results for debugging
    print(f"🔹 Student ID: {student_id}")
    print(f"   Level 5 Average: {level_5_average:.2f}")
    print(f"   Level 6 Average: {level_6_average:.2f}")
    print(f"   Final Mark: {final_mark:.2f}")
    print(f"   Classification: {classification}\n")

# ✅ Convert results to DataFrame and Save
degree_results_df = pd.DataFrame(students_data, columns=["Student ID", "Level 5 Avg", "Level 6 Avg", "Final Mark", "Classification"])
degree_results_df.to_csv(output_file, index=False)

print("✅ Degree calculation complete. Results saved in:", output_file)'


'''