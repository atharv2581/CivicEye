# CivicEye

CivicEye is an AI-assisted civic issue reporting and tracking application built with Python, Streamlit, MySQL, and Ollama.

## Features

- Submit civic complaints with descriptions and locations.
- Analyze complaints using a locally running AI model.
- Categorize issues and assign severity, priority, and departments.
- Track complaints using a reference ID.
- Manage complaint status and administrator notes.
- View dashboard metrics, charts, and department workload.
- Maintain a history of complaint status changes.

## Technology Stack

- Python
- Streamlit
- MySQL
- Ollama
- Gemma 3 4B

## Prerequisites

- Python installed
- MySQL Server installed
- Ollama installed with the `gemma3:4b` model available

## Setup

1. Clone or download this repository.
2. Create and activate a Python virtual environment.
3. Install the required Python packages.
4. Configure database and administrator credentials in `.streamlit/secrets.toml`.
5. Create the required MySQL database and tables.
6. Start Ollama and ensure the `gemma3:4b` model is available.
7. Run the application:

   `python -m streamlit run app.py`

## Configuration

Keep credentials in `.streamlit/secrets.toml`. Never commit secrets, database passwords, or private database exports.

## Project Status

This is a personal portfolio project under development.
