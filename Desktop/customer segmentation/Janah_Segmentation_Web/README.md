# 📊 Janah Customer Segmentation Web Application

A comprehensive web-based customer segmentation tool for Janah Hardware Store, built with Flask and Streamlit integration. This application analyzes customer purchasing behavior using RFM (Recency, Frequency, Monetary) analysis and K-means clustering to create actionable customer segments.

## 🎯 Project Overview

**Purpose**: Transform raw transactional data into meaningful customer segments for targeted marketing and business decisions.

**Key Features**:
- 📥 **Data Handling**: Default dataset or custom CSV/XLSX upload
- 🧹 **Data Cleaning**: Missing values, duplicates, and outlier removal
- 📊 **RFM Analysis**: Recency, Frequency, Monetary calculations
- 🎯 **K-means Clustering**: Optimal segment determination with elbow method
- 📈 **Visualizations**: Interactive charts and graphs
- 📄 **Report Generation**: Comprehensive analysis reports
- 📧 **Campaign Preview**: Segment-specific email templates
- 📱 **Responsive Design**: Mobile-friendly interface

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Science**: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
- **Segmentation**: Streamlit (embedded component)
- **Deployment**: Render, Heroku, or local hosting

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)
- Modern web browser

## 🚀 Installation & Setup

### Option 1: Quick Start (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Janah_Segmentation_Web
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download dataset**:
   ```bash
   python download_dataset.py
   ```

5. **Run the application**:
   ```bash
   python run.py
   ```

6. **Access the application**:
   Open your browser and go to: `http://localhost:5000`

### Option 2: Automated Setup

Run the dependency checker:
```bash
python check_dependencies.py
```

## 🌐 Deployment Options

### Option 1: Render (Recommended - Free)

1. **Create Render Account**:
   - Go to [render.com](https://render.com)
   - Sign up with GitHub account

2. **Connect Repository**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**:
   ```
   Name: janah-segmentation
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn run:app
   ```

4. **Environment Variables** (if needed):
   ```
   PYTHON_VERSION=3.9.0
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for build to complete
   - Access your live application

### Option 2: Heroku

1. **Install Heroku CLI**:
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**:
   ```bash
   heroku login
   heroku create janah-segmentation-app
   ```

3. **Add Buildpacks**:
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Open Application**:
   ```bash
   heroku open
   ```

### Option 3: Local Network Deployment

1. **Modify run.py**:
   ```python
   app.run(host='0.0.0.0', port=5000, debug=False)
   ```

2. **Run Application**:
   ```bash
   python run.py
   ```

3. **Access from Network**:
   - Find your IP address: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
   - Access from other devices: `http://YOUR_IP:5000`

## 📁 Project Structure

```
Janah_Segmentation_Web/
├── app/                          # Flask application
│   ├── __init__.py              # Flask app factory
│   ├── routes.py                # Route definitions
│   ├── templates/               # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── home.html           # Home page
│   │   ├── segmentation.html   # Analysis page
│   │   └── results.html        # Results page
│   └── static/                 # Static files
│       ├── css/style.css       # Custom styles
│       ├── js/script.js        # JavaScript
│       └── images/             # Images
├── streamlit/                   # Streamlit segmentation
│   ├── segmentation.py         # Core analysis logic
│   └── requirements.txt        # Streamlit dependencies
├── data/                       # Data storage
│   ├── online_retail.csv       # Default dataset
│   ├── processed/              # Analysis outputs
│   └── uploads/                # User uploads
├── tests/                      # Test files
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── download_dataset.py         # Dataset downloader
├── check_dependencies.py       # Dependency checker
├── test_phase5.py             # Phase 5 testing
└── README.md                  # This file
```

## 🎬 Demo Script for Presentation

### **Demo Flow (5-7 minutes)**

#### **1. Introduction (30 seconds)**
- "Welcome to the Janah Customer Segmentation Web Application"
- "This tool helps businesses analyze customer behavior and create targeted marketing segments"
- "Built with Flask backend and Streamlit for data science"

#### **2. Home Page Tour (1 minute)**
- Show the professional landing page
- Highlight the navigation bar (Home, Segmentation, Results)
- Point out the responsive design
- "Notice the modern blue/green theme and professional layout"

#### **3. Data Source Selection (1 minute)**
- Navigate to Segmentation page
- Show the two data source options:
  - **Default Dataset**: Online Retail from UCI repository
  - **Custom Upload**: CSV/XLSX files
- Demonstrate file upload drag & drop functionality
- "Users can either use our pre-loaded dataset or upload their own data"

#### **4. Analysis Configuration (1 minute)**
- Show clustering parameters:
  - Elbow method (automatic optimal clusters)
  - Manual cluster selection (3-6 segments)
- Explain RFM analysis:
  - **Recency**: Days since last purchase
  - **Frequency**: Number of transactions
  - **Monetary**: Total spending amount
- "The system automatically determines the optimal number of customer segments"

#### **5. Run Analysis (1 minute)**
- Click "Run Analysis" button
- Show progress tracking:
  - "Fetching dataset..."
  - "Cleaning data..."
  - "Running segmentation..."
  - "Analysis completed!"
- "Real-time progress updates keep users informed"

#### **6. Results Display (1-2 minutes)**
- Show comprehensive results page:
  - **Summary Statistics**: Total customers, segments, averages
  - **Segment Details**: Customer counts, percentages, characteristics
  - **Visualizations**: Charts and graphs (if available)
  - **RFM Progress**: Analysis completion status
- "The results provide actionable insights for business decisions"

#### **7. Post-Segmentation Actions (1 minute)**
- Demonstrate each action:
  - **📄 Download Report**: Generate comprehensive TXT report
  - **📊 Export Data**: Download CSV with segment data
  - **📧 Campaign Preview**: Show email templates for each segment
  - **🔗 Share Results**: URL sharing functionality
- "These features enable immediate business action"

#### **8. Technical Highlights (30 seconds)**
- Show folder structure
- Highlight key files:
  - `streamlit/segmentation.py` (core analysis)
  - `app/routes.py` (Flask backend)
  - `app/templates/results.html` (dynamic results)
- "Built with modern web technologies and best practices"

### **Demo Tips**
- **Practice the flow** before presentation
- **Have sample data ready** for quick demonstration
- **Prepare answers** for common questions
- **Show both success and error handling**
- **Highlight responsive design** on different screen sizes

## 📊 Dataset Information

### **Default Dataset: Online Retail (UCI)**
- **Source**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail)
- **Size**: ~500,000 transactions
- **Columns**: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
- **Format**: Excel (.xlsx) converted to CSV

### **Data Requirements**
Your CSV should contain these columns:
- `CustomerID`: Unique customer identifier
- `InvoiceDate`: Date of transaction
- `InvoiceNo`: Invoice number
- `Quantity`: Quantity purchased
- `UnitPrice`: Price per unit

## ⚙️ Configuration

### **Environment Variables**
```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=data/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# Optional: Database Configuration
DATABASE_URL=your-database-url
```

### **Customization**
- **Theme Colors**: Modify CSS variables in `app/static/css/style.css`
- **Analysis Parameters**: Adjust clustering settings in `streamlit/segmentation.py`
- **Report Templates**: Customize report format in `generate_report()` function

## 🧪 Testing

### **Run Test Suite**
```bash
python test_phase5.py
```

### **Manual Testing Checklist**
- [ ] Application starts without errors
- [ ] Navigation works on all pages
- [ ] File upload accepts CSV/XLSX files
- [ ] Analysis runs successfully
- [ ] Results display correctly
- [ ] Download functions work
- [ ] Responsive design on mobile
- [ ] Error handling works

## 🐛 Troubleshooting

### **Common Issues**

**1. Import Errors**
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
python check_dependencies.py
```

**2. Dataset Not Found**
```bash
# Solution: Download dataset
python download_dataset.py
```

**3. Port Already in Use**
```bash
# Solution: Change port in run.py
app.run(port=5001)  # or any available port
```

**4. Memory Issues**
```bash
# Solution: Reduce dataset size or increase system memory
# Modify data loading in streamlit/segmentation.py
```

**5. Deployment Issues**
- Check build logs on deployment platform
- Verify all dependencies are in `requirements.txt`
- Ensure `run.py` is properly configured

### **Debug Mode**
```bash
# Enable debug mode for development
export FLASK_ENV=development
python run.py
```

## 📈 Performance Optimization

### **For Large Datasets**
- Implement data sampling for initial analysis
- Add pagination for results display
- Use background processing for long-running analyses
- Implement caching for repeated calculations

### **For Production**
- Use production WSGI server (Gunicorn)
- Implement proper error logging
- Add monitoring and analytics
- Set up automated backups

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Developer Information

**Project**: Janah Customer Segmentation Web Application  
**Developer**: [Your Name]  
**Date**: July 27, 2025  
**Course**: Data Science & Web Development  
**Institution**: [Your Institution]  

## 📞 Support

For questions or support:
- **Email**: janah@hardwarestore.com
- **Documentation**: This README file
- **Issues**: Create an issue in the repository

---

**Built with ❤️ for Janah Hardware Store**  
*Transforming data into actionable business insights*
