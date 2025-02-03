# End-to-End Test Automation Framework with Python & Pytest

## Overview
This test automation framework is designed for **end-to-end (E2E) API testing** using **Python and Pytest**. It dynamically retrieves email templates and recipient data, creates campaigns, validates responses, and ensures smooth execution through a scheduled suite runner.

---

## Framework Components

### 1️⃣ **Test Plan & API Coverage**
The framework automates the following API workflows:
- **`test_get_email_templates`**: Fetches email templates dynamically.
- **`test_get_recipients_list`**: Retrieves recipient email lists.
- **`test_get_campaigns`**: Validates campaign retrieval.
- **`test_create_campaigns`**: Dynamically creates email campaigns.
- **`test_update_campaign_name`**: Updates campaign details and verifies response.
- **`test_get_campaign_and_validate_update`**: Fetches and validates campaign updates.

Each test case:
✅ **Retrieves required data dynamically**
✅ **Validates API response codes & messages**
✅ **Stores extracted data for reuse**
✅ **Ensures correctness through assertions**

---

### 2️⃣ **Dynamic Data Handling (CSV Storage)**
The framework dynamically **extracts and stores** required data in CSV files:
- **Template Data (`template_ids.csv`)**: Stores email template IDs.
- **Recipient Data (`recipient_list_ids.csv`)**: Stores recipient email list IDs.
- **Campaign Data (`campaigns.csv`)**: Stores created campaign IDs & names.

This allows:
✔ **Reusability across multiple test cases**
✔ **Parameterization without hardcoding values**
✔ **Data-driven campaign creation**

---

### 3️⃣ **Test Execution (Suite Runner & Scheduler Integration)**
A **central suite file** (`api_suite.py`) is responsible for executing all test scripts in the correct order.

- **Runs all tests dynamically** based on CSV input.
- **Generates test execution reports** in HTML format.
- **Configured via Windows Task Scheduler** to execute on a Virtual Machine (VM) at required intervals.
- **Triggers `run_api_suite.bat`** to launch the tests automatically at a scheduled time.

#### **Scheduler Integration (Task Scheduler in VM)**
1. **Create a Windows Task** (`taskschd.msc`).
2. Set the action to execute `run_api_suite.bat`.
3. Configure the trigger for desired execution time.
4. Ensure VM remains active at runtime.
 
---

### 4️⃣ **Framework Folder Structure**
```
E2E_Framework/
│── Test_runner_folder/
│   ├── API_Modules/               # Contains API test scripts
│   ├── Reports/                   # Stores test reports
│   ├── Test_Data/                  
│   │   ├── Template_ID/            # Stores template data
│   │   ├── Recipients_ID/          # Stores recipient data
│   │   ├── Campaigns_ID/           # Stores campaign data
│── Tsuites/
│   ├── api_suite.py               # Main suite runner
│── run_api_suite.bat              # Batch script for scheduling
│── requirements.txt                # Dependencies file
```

---

## Setup Instructions

### **1️⃣ Install Dependencies**
Run the following command to install required packages:
```sh
pip install -r requirements.txt
```

### **2️⃣ Update Local Paths**
Modify the **report path** in `api_suite.py` and `test_campaigns.py` to ensure correct report storage.

```python
report_dir = Path(__file__).resolve().parent / "Test_runner_folder" / "Reports"
```
Ensure the **Reports/** folder exists before execution.

---

## Execution Guide

### **1️⃣ Run the Suite Manually**
To execute all tests, run:
```sh
python api_suite.py
```

### **2️⃣ Run via Scheduler (Automated Execution)**
- Use the **Task Scheduler** to execute `run_api_suite.bat`.
- The script will automatically trigger `api_suite.py` and store reports in the `Reports/` folder.

---

## Reporting & Debugging

### **Generated Reports**
- The framework **generates HTML reports** after each execution.
- Reports are stored in `E2E_Framework/Test_runner_folder/Reports/`.
- Open `test_report.html` in a browser to view results.

### **Debugging Issues**
If test execution fails:
1. **Check `test_report.html` for failure logs.**
2. **Manually run individual tests** to identify issues:
   ```sh
   pytest path/to/test_file.py --tb=short
   ```
3. **Ensure data CSV files are updated correctly.**
4. **Verify API responses and expected assertions.**

---

## Conclusion
This **E2E API testing framework** automates the entire workflow of fetching email templates, retrieving recipients, creating campaigns, and validating API responses. With **dynamic data handling, scheduled execution, and automated reporting**, it ensures a **fully functional and scalable API testing process.**

For support, contact the QA Automation Team.


---
Naveen Chandrasekaran
SDET -Interview
