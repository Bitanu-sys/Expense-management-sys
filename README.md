# Expense Management System

A Python-based command-line application for managing personal expenses, processing external datasets, and importing/exporting financial records.

## Features

- Add, view, search and delete expenses.
- Calculate total and category-wise spending.
- Persistent JSON-based data storage.
- Import expense records from CSV and JSON.
- Validate and clean imported records.
- Detect duplicate records.
- Preview rejected records before importing.
- Export expenses into CSV and JSON formats.
- Automated tests using pytest.

## Technology Stack

- Python
- JSON
- CSV
- pathlib
- pytest

## Project Structure

```text
Expense-Management-System/
├── main.py
├── expense_manager.py
├── storage.py
├── data_processor.py
├── import_export.py
├── sample_data/
├── tests/
├── exports/
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd Expense-Management-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python main.py
```

## Run Tests

```bash
python -m pytest -v
```

## Import and Export

The application supports CSV and JSON imports and exports.

Sample datasets are available inside `sample_data/`.

Exported files are generated inside the `exports/` directory.

## Architecture

The project follows a modular structure separating application orchestration, business logic, data processing, file handling, and persistent storage.

## Future Improvements

- REST API integration using FastAPI.
- Database integration.
- Web-based dashboard.
- Expense analytics and visualisation.
