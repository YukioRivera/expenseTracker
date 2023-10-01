# Expense Tracker

Expense Tracker is a simple and intuitive web application designed to help individuals keep track of their expenses and recurring charges. The application provides a user-friendly interface to add, view, and manage expenses, allowing users to have better control over their financial life.

## Features

- **Add Expense:** Users can easily add individual expense entries specifying the amount and category.
- **Add Recurring Charge:** Users can add recurring charges specifying the amount, category, start date, end date (optional), and day of the month.
- **View Expenses:** A summary of expenses and recurring charges for a selected month and year is displayed in a well-organized table.
- **Expense Insights:** Users can navigate to the Expense Insights section to get a visual breakdown of their expenses.

## Getting Started

### Prerequisites

- Python 3.8 or later
- Flask
- SQLAlchemy

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YukioRivera/expenseTracker.git
   cd expenseTracker

Create a virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt

flask db upgrade

flask run

Open your web browser and navigate to http://127.0.0.1:5000/.

Usage
Adding an Expense:

Navigate to the "Add Expense" section.
Enter the amount and category of the expense.
Click "Add Expense" to save the entry.
Adding a Recurring Charge:

Navigate to the "Add Recurring Charge" section.
Enter the amount, category, start date, end date (optional), and day of the month.
Click "Add Recurring Charge" to save the entry.
Viewing Expenses:

Select the desired month and year from the dropdown menu at the top of the page.
The summary table will update to show the expenses and recurring charges for the selected month and year.
Viewing Expense Insights:

Click the "Expense Insights" button to view a breakdown of expenses by category.
