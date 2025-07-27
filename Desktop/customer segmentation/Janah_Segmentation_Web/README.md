# Janah Customer Segmentation Web App

A web-based customer segmentation tool for Janah Hardware Store using RFM (Recency, Frequency, Monetary) analysis and K-means clustering.

## 🎯 Project Overview

This application helps analyze customer purchasing behavior using the Online Retail dataset from UCI Machine Learning Repository. It segments customers into actionable groups (e.g., loyal buyers, inactive customers) to enable targeted marketing and inventory decisions.

## 🚀 Features

- **Data Processing**: Automated data cleaning and RFM metric calculation
- **Segmentation**: K-means clustering with elbow method optimization
- **Visualizations**: Interactive charts and graphs for insights
- **Multi-page UI**: Clean navigation with Home, Segmentation, and Results pages
- **File Upload**: Support for custom CSV/XLSX datasets
- **Export Options**: Download reports and segment data
- **Campaign Preview**: Generate targeted marketing suggestions

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Data Analysis**: Pandas, Scikit-learn, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Segmentation**: Streamlit (embedded component)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## ⚙️ Installation & Setup

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd Janah_Segmentation_Web

# Or download and extract the project folder
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python run.py
```

### 5. Access the Application
Open your web browser and navigate to: **http://localhost:5000**

## 📁 Project Structure

```
Janah_Segmentation_Web/
├── app/                    # Flask application
│   ├── __init__.py        # App factory
│   ├── routes.py          # Route definitions
│   ├── templates/         # HTML templates
│   └── static/           # CSS, JS, images
├── streamlit/             # Streamlit segmentation module
│   ├── segmentation.py   # Main segmentation logic
│   └── requirements.txt  # Streamlit dependencies
├── data/                  # Data storage
│   ├── online_retail.csv # Default dataset
│   └── uploads/          # User uploaded files
├── venv/                 # Virtual environment
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── run.py              # Application entry point
```

## 🎮 Usage

1. **Home Page**: Overview and navigation to different sections
2. **Segmentation Page**: Upload data and configure segmentation parameters
3. **Results Page**: View segmentation results, visualizations, and export options

## 📊 Dataset

The application uses the Online Retail dataset from UCI Machine Learning Repository:
- **Source**: https://archive.ics.uci.edu/dataset/352/online+retail
- **Format**: CSV file with customer transaction data
- **Features**: CustomerID, InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, Country

## 🔧 Configuration

- **Port**: Default 5000 (configurable in run.py)
- **Upload Limit**: 16MB maximum file size
- **Clusters**: 3-5 segments (configurable)

## 🐛 Troubleshooting

### Common Issues:

1. **Port already in use**: Change port in run.py or kill existing process
2. **Module not found**: Ensure virtual environment is activated
3. **Upload fails**: Check file size and format (CSV/XLSX only)

### Debug Mode:
The application runs in debug mode by default. For production, set `debug=False` in run.py.

## 📝 License

This project is created for educational purposes as part of a data science course assignment.

## 👨‍💻 Developer

Created for Janah Hardware Store customer segmentation analysis.

---

**Last Updated**: July 27, 2025
**Version**: 1.0.0
