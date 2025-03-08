# Suicide Rate Analysis Dashboard

## Project Overview

This project is a web-based dashboard for analyzing global suicide rates using interactive visualizations. The application is built with Flask and uses Plotly for data visualization. The goal of this dashboard is to provide insights into suicide trends over time, across different age groups, regions, and economic factors to support mental health awareness and intervention strategies.

## Features

- Interactive bar, line, and pie charts for data visualization
- Filtering options to analyze trends by age group, economic factors, and region
- A responsive and user-friendly interface for ease of exploration

## Requirements

To set up and run the project, ensure that you have the following installed:

- Python 3.8+
- pip (Python package manager)
- A stable internet connection for downloading dependencies

## Installation and Setup

1. **Clone the Repository:**

   git clone <repository_url>
   cd <repository_folder>

   ```

   ```

2. **Create a Virtual Environment (Optional but Recommended):**

   python -m venv venv
   source venv/bin/activate # On macOS/Linux
   venv\Scripts\activate # On Windows

   ```

   ```

3. **Install Dependencies:**

   pip install -r requirements.txt

4. **Ensure the Required Data Files Are Present:**
   Place the datasets (`suicide_rates.csv` and `age_std_suicide_rates.csv`) inside the `data` directory.

5. **Run the Application:**


   python app.py


6. **Access the Dashboard:**
   Open your browser and go to `http://127.0.0.1:5000/`

## Deployment

To deploy this project on a production server:

- Use a WSGI server like Gunicorn for Flask applications.
- Deploy using cloud platforms such as AWS, DigitalOcean, or Heroku.
- Set up an Nginx reverse proxy for better performance.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Acknowledgments

The data used in this project is sourced from reputable public datasets on global suicide rates. The analysis aims to provide insights while promoting mental health awareness.
