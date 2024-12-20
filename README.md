# Expense Tracker Project - README

This README provides comprehensive instructions on how to set up and use the Expense Tracker project. The project is designed to help you track your expenses by processing bank statement CSV files, importing the data into a SQLite database for efficient querying and analysis, and performing data visualization and machine learning to understand your spending habits. The original CSV files are kept as backups and for data verification.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Navigate to the Project Directory](#2-navigate-to-the-project-directory)
  - [3. Review Project Files](#3-review-project-files)
  - [4. Build the Docker Image](#4-build-the-docker-image)
  - [5. Run the Docker Container](#5-run-the-docker-container)
  - [6. Persisting Data with Volumes](#6-persisting-data-with-volumes)
- [Using the Application](#using-the-application)
  - [1. Importing CSV Files into SQLite](#1-importing-csv-files-into-sqlite)
  - [2. Data Analysis and Visualization](#2-data-analysis-and-visualization)
  - [3. Applying Machine Learning](#3-applying-machine-learning)
- [Additional Commands](#additional-commands)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Final Notes](#final-notes)

---

## Introduction

The Expense Tracker project is a tool designed to help you monitor and analyze your personal finances. By processing bank statement CSV files, it imports your transaction data into a SQLite database, allowing for efficient querying and data analysis. The application provides capabilities for data visualization and applies machine learning techniques to help you understand and improve your spending habits. Original CSV files are preserved as backups for data verification and security.

---

## Features

- **CSV File Processing**: Reads bank statements in CSV format.
- **SQLite Database Storage**: Imports transaction data into a SQLite database for efficient querying.
- **Data Backup**: Keeps original CSV files as backups for verification.
- **Data Analysis**: Analyzes spending patterns using data analysis tools.
- **Data Visualization**: Visualizes spending habits with charts and graphs.
- **Machine Learning**: Applies machine learning algorithms to identify spending trends.
- **Dockerized Environment**: Ensures a consistent development and execution environment using Docker.

---

## Prerequisites

- **Docker**: Ensure that Docker is installed on your system. Download it from the [official Docker website](https://www.docker.com/get-started).

- **Bank Statement CSV Files**: Obtain your bank statements in CSV format and place them in the `data/` directory.

---

## Project Structure

Your project directory should have the following structure:

```
expense-tracker/
├── Dockerfile
├── requirements.txt
├── main.py
├── data/
│   └── (Your CSV files)
├── backups/
│   └── (Backup CSV files will be stored here)
├── scripts/
│   ├── import_data.py
│   ├── analyze_data.py
│   └── ml_model.py
└── README.md
```

- **Dockerfile**: Contains instructions to build the Docker image.
- **requirements.txt**: Lists all Python dependencies.
- **main.py**: The main script that orchestrates the application workflow.
- **data/**: Directory containing your bank statement CSV files.
- **backups/**: Directory where backup copies of CSV files are stored.
- **scripts/**: Contains separate scripts for data import, analysis, and machine learning.
- **README.md**: This README file.

---

## Environment Setup

Follow these steps to set up and run your environment.

### 1. Clone the Repository

If you have a Git repository for your project, clone it using:

```bash
git clone https://github.com/your-username/expense-tracker.git
```

Alternatively, create a new directory for your project:

```bash
mkdir expense-tracker
cd expense-tracker
```

### 2. Navigate to the Project Directory

Ensure you are in the project's root directory:

```bash
cd expense-tracker
```

### 3. Review Project Files

- **Dockerfile**: Contains instructions for building the Docker image.
- **requirements.txt**: Lists all the Python packages required for the project.
- **main.py**: The main script to run the application.
- **scripts/**: Contains scripts for data import (`import_data.py`), analysis (`analyze_data.py`), and machine learning (`ml_model.py`).
- **data/**: Place your bank statement CSV files here.
- **backups/**: Backup copies of your CSV files will be stored here.

### 4. Build the Docker Image

Run the following command to build the Docker image:

```bash
docker build -t expense-tracker .
```

- `-t expense-tracker-env`: Tags the image with the name `expense-tracker-env`.
- `.`: Specifies the current directory as the build context.

### 5. Run the Docker Container

To run the container interactively:

```bash
docker run -it --rm expense-tracker
```

- `-it`: Runs the container in interactive mode with a pseudo-TTY.
- `--rm`: Automatically removes the container when it exits.

### 6. Persisting Data with Volumes (Better alt)

To ensure data (like your SQLite database and CSV backups) persists between runs, use Docker volumes:

```bash
docker run -it -v /home/dev/expenseTracker:/workspace --name expense-tracker expense-tracker bash
```

---

## Using the Application

### 1. Importing CSV Files into SQLite

The `import_data.py` script reads your bank statement CSV files, preprocesses the data, imports it into a SQLite database, and creates backups of the original CSV files.

#### Steps:

1. **Place Your CSV Files**: Copy your bank statement CSV files into the `data/` directory.

2. **Run the Import Script**:

   Inside the Docker container, run:

   ```bash
   python scripts/import_data.py
   ```

#### Notes:

- Adjust the column names in the script to match those in your CSV files.
- Ensure that the `data/` and `backups/` directories exist and are correctly mounted in the Docker container.

### 2. Data Analysis and Visualization

The `analyze_data.py` script reads data from the SQLite database and performs data analysis and visualization.

#### Steps:

1. **Run the Analysis Script**:

   Inside the Docker container, run:

   ```bash
   python scripts/analyze_data.py
   ```

#### Notes:

- The script saves plots of your spending patterns to the `data/` directory.
- Customize the analysis to suit your needs, such as categorizing expenses or identifying trends.

### 3. Applying Machine Learning

The `ml_model.py` script applies machine learning algorithms to your transaction data to identify spending patterns.

#### Steps:

1. **Run the Machine Learning Script**:

   Inside the Docker container, run:

   ```bash
   python scripts/ml_model.py
   ```

#### Notes:

- The script generates plots and saves the results to the `data/` directory.
- You can modify the features used for clustering and the machine learning algorithms applied.

---

## Additional Commands

- **Accessing a Shell in the Container**:

  To start a bash session inside the container for debugging:

  ```bash
  docker run -it --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/backups:/app/backups" expense-tracker-env bash
  ```

- **Rebuilding the Image After Changes**:

  If you make changes to the Dockerfile or `requirements.txt`, rebuild the image:

  ```bash
  docker build -t expense-tracker-env .
  ```

---

## Troubleshooting

- **Permission Issues**:

  If you encounter permission issues with mounted volumes, ensure you have the necessary permissions on the host system.

- **Docker Daemon Not Running**:

  If Docker commands fail, make sure the Docker daemon is running.

- **Dependency Errors**:

  If a Python package fails to install, check the package name and version in `requirements.txt`.

- **Data Import Errors**:

  If the CSV files have unexpected formats or missing columns, adjust the preprocessing steps in the `import_data.py` script accordingly.

- **Visualization Issues**:

  If plots are not displaying within the Docker container, ensure that you have appropriate display settings or save plots to files as shown in the scripts.

---

## Contributing

Contributions are welcome! If you'd like to improve this project:

1. **Fork the Repository**: Click the "Fork" button at the top of the repository page.

2. **Create a New Branch**: For your feature or bugfix.

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes**: With clear and descriptive messages.

   ```bash
   git commit -am 'Add new feature: your feature description'
   ```

4. **Push to the Branch**:

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a Pull Request**: Describe your changes and submit the PR for review.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Final Notes

- **Data Privacy**: Be cautious with your financial data. Ensure that your backups and databases are stored securely.

- **Customization**: Feel free to customize the scripts to better suit your data and analysis needs.

- **Learning and Improvement**: Use this project as an opportunity to improve your programming, data analysis, and machine learning skills.

---

**Thank you for using the Expense Tracker project! If you have any questions or need assistance, please feel free to reach out. Happy tracking!**

---