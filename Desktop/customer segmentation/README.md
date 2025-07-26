# Janah Customer Segmentation Web Application

A comprehensive web application for customer segmentation analysis using Flask and Streamlit.

## Features

- Web-based customer segmentation analysis
- Interactive Streamlit dashboard
- Data upload and processing capabilities
- Multiple segmentation algorithms
- Visualization and reporting

## Installation

### Using pip

```bash
pip install -e .
```

### For development

```bash
pip install -e ".[dev]"
```

### For analysis features

```bash
pip install -e ".[analysis]"
```

## Usage

### Flask Web Application

```bash
python run.py
```

### Streamlit Dashboard

```bash
streamlit run streamlit/segmentation.py
```

## Project Structure

```
Janah_Segmentation_Web/
├── app/                    # Flask application
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, images
├── streamlit/              # Streamlit components
│   ├── segmentation.py
│   └── requirements.txt
├── data/                   # Data files
│   ├── online_retail.csv
│   └── uploads/
├── setup.py               # Package configuration
├── README.md
└── run.py                 # Application entry point
```

## Requirements

- Python 3.8+
- Flask 2.3+
- Streamlit 1.28+
- pandas, numpy, scikit-learn
- matplotlib, seaborn, plotly

## License

MIT License
