import os
import subprocess
import sys
from pathlib import Path


def run_test_file(test_file, test_dir, report_path):
    test_path = os.path.join(test_dir, test_file)

    pytest_command = f'pytest {test_path} --html={report_path} --self-contained-html --reruns 1 --tb=short --disable-warnings'

    print(f"[INFO] Running: {pytest_command}")
    process = subprocess.run(pytest_command, shell=True, text=True, encoding="utf-8")

    if process.returncode != 0:
        print(f"[ERROR] Test Failed: {test_file}")
        sys.exit(process.returncode)


def run_test_suite():

    project_root = Path(__file__).resolve().parent.parent
    test_dir = project_root / "Test_runner_folder" / "API_Modules"
    report_dir = project_root / "Test_runner_folder" / "Reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "test_report.html"
    test_files = [
        "test_email_templates.py",
        "test_recipients.py",
        "test_campaigns.py"
    ]

    for test_file in test_files:
        run_test_file(test_file, test_dir, report_path)

    print(f"\n All tests completed. Report generated at: {report_path}")


if __name__ == "__main__":
    print("[INFO] Auto-detecting test paths...")
    run_test_suite()
