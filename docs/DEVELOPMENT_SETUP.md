# EDGE_ENGINE Development Setup

Version: 1.1

Status: Active

---

# Purpose

This document is a practical guide for setting up EDGE_ENGINE on a new Windows PC.

It is written so that a contributor can prepare the environment without needing external help.

---

# Prerequisites

Install the following tools first:

* Git
* Python
* Visual Studio Code

---

# 1. Install Git

Download and install Git from the official website.

After installation, verify that Git is available:

```powershell
git --version
```

If Git is not recognized, restart the terminal or reopen Visual Studio Code.

---

# 2. Install Python

Install Python and make sure the Python executable is available in the PATH.

Verify the installation:

```powershell
python --version
```

---

# 3. Install Visual Studio Code

Install Visual Studio Code and open the repository folder from there.

It is recommended to use the integrated terminal for the following steps.

---

# 4. Clone the Repository

Open PowerShell and run:

```powershell
git clone <repository-url>
cd edge-platform
```

Replace `<repository-url>` with the correct repository address.

---

# 5. Create the Virtual Environment

From the repository root, run:

```powershell
python -m venv .venv
```

---

# 6. Activate the Virtual Environment

In PowerShell, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the script because of the Execution Policy, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then run the activation command again.

---

# 7. Install the Project

Install the project in editable mode:

```powershell
pip install -e .
```

---

# 8. Install Development Dependencies

Install the required development packages:

```powershell
pip install pytest PyYAML
```

---

# 9. Final Verification

Run the test suite:

```powershell
pytest
```

Expected result:

* 46 tests passed

---

# Troubleshooting

## Git is not recognized

If the terminal reports that `git` is not recognized:

* close and reopen the terminal;
* verify that Git was installed successfully;
* check that the Git installation path is available in the system PATH.

## Execution Policy error

If PowerShell returns an execution policy error:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

This applies only to the current terminal session.

## pytest is not installed

If `pytest` is missing, install it manually:

```powershell
pip install pytest
```

## Missing yaml module

If Python reports that `yaml` is missing, install it manually:

```powershell
pip install PyYAML
```

---

# Recommended Reading Order

After setup, review the documentation in this order:

1. README.md
2. PROJECT_STATUS.md
3. FOUNDATION_BLUEPRINT.md
4. PROJECT_BOOTSTRAP.md
5. docs/DEVELOPMENT_WORKFLOW.md
6. docs/WF-001_DEVELOPMENT_WORKFLOW.md
