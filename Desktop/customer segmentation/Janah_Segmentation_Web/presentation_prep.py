#!/usr/bin/env python3
"""
Presentation Preparation Script for Janah Customer Segmentation
Prepares all deliverables and files for the final presentation
"""

import os
import shutil
import json
import pandas as pd
from datetime import datetime

def create_presentation_folder():
    """Create a presentation folder with all deliverables"""
    print("🎯 Creating presentation deliverables...")
    
    # Create presentation folder
    presentation_folder = "Janah_Segmentation_Presentation"
    if os.path.exists(presentation_folder):
        shutil.rmtree(presentation_folder)
    os.makedirs(presentation_folder)
    
    # Create subfolders
    folders = [
        "source_code",
        "documentation", 
        "sample_outputs",
        "screenshots",
        "demo_assets"
    ]
    
    for folder in folders:
        os.makedirs(os.path.join(presentation_folder, folder))
    
    return presentation_folder

def copy_source_code(presentation_folder):
    """Copy essential source code files"""
    print("📁 Copying source code...")
    
    source_files = [
        "app/",
        "streamlit/",
        "run.py",
        "requirements.txt",
        "download_dataset.py",
        "check_dependencies.py"
    ]
    
    for item in source_files:
        if os.path.exists(item):
            dest = os.path.join(presentation_folder, "source_code", item)
            if os.path.isdir(item):
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
            print(f"  ✅ Copied: {item}")

def copy_documentation(presentation_folder):
    """Copy documentation files"""
    print("📚 Copying documentation...")
    
    docs = [
        "README.md",
        ".gitignore"
    ]
    
    for doc in docs:
        if os.path.exists(doc):
            shutil.copy2(doc, os.path.join(presentation_folder, "documentation"))
            print(f"  ✅ Copied: {doc}")

def create_sample_outputs(presentation_folder):
    """Create sample analysis outputs"""
    print("📊 Creating sample outputs...")
    
    # Create sample RFM data
    sample_data = pd.DataFrame({
        'CustomerID': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        'Recency': [15, 45, 90, 120, 30, 60, 180, 25],
        'Frequency': [8, 5, 2, 1, 6, 3, 1, 7],
        'Monetary': [2500, 1800, 500, 200, 2200, 1200, 300, 2800],
        'Cluster': [0, 0, 2, 2, 0, 1, 2, 0],
        'Segment': ['Loyal Customers', 'Loyal Customers', 'Inactive Customers', 
                   'Inactive Customers', 'Loyal Customers', 'At-Risk Customers', 
                   'Inactive Customers', 'Loyal Customers']
    })
    
    # Save sample data
    output_dir = os.path.join(presentation_folder, "sample_outputs")
    sample_data.to_csv(os.path.join(output_dir, "sample_rfm_data.csv"), index=False)
    
    # Create sample analysis summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "parameters": {
            "data_source": "Sample Dataset",
            "n_clusters": 3,
            "total_customers": 8
        },
        "summary_stats": {
            "total_customers": 8,
            "n_clusters": 3,
            "avg_recency": 58.75,
            "avg_monetary": 1312.5,
            "cluster_sizes": {
                "Loyal Customers": 4,
                "At-Risk Customers": 1,
                "Inactive Customers": 3
            }
        }
    }
    
    with open(os.path.join(output_dir, "sample_analysis_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Create sample report
    report_content = f"""
JANAH HARDWARE STORE - CUSTOMER SEGMENTATION REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ANALYSIS SUMMARY
================
Total Customers Analyzed: 8
Number of Segments: 3
Analysis Parameters: Sample demonstration data

SEGMENT PROFILES
================

LOYAL CUSTOMERS
- Customer Count: 4 (50.0%)
- Average Recency: 28.8 days
- Average Frequency: 6.5 transactions
- Average Monetary: $2,325.0
- Total Revenue: $9,300.0

RECOMMENDATIONS:
- Maintain relationship with exclusive offers
- Consider VIP program
- Request referrals

AT-RISK CUSTOMERS
- Customer Count: 1 (12.5%)
- Average Recency: 60.0 days
- Average Frequency: 3.0 transactions
- Average Monetary: $1,200.0
- Total Revenue: $1,200.0

RECOMMENDATIONS:
- Re-engagement campaigns
- Special discounts
- Customer feedback surveys

INACTIVE CUSTOMERS
- Customer Count: 3 (37.5%)
- Average Recency: 130.0 days
- Average Frequency: 1.3 transactions
- Average Monetary: $333.3
- Total Revenue: $1,000.0

RECOMMENDATIONS:
- Win-back campaigns
- Significant discounts
- Product updates

TECHNICAL DETAILS
=================
- RFM Analysis: Recency, Frequency, Monetary metrics
- Clustering Algorithm: K-means with StandardScaler
- Optimal Clusters: Determined by Elbow Method + Silhouette Score
- Data Quality: Outliers removed using IQR method

BUSINESS INSIGHTS
=================
- Top Revenue Segment: Loyal Customers
- Most Active Segment: Loyal Customers
- Largest Segment: Loyal Customers

NEXT STEPS
==========
1. Implement targeted marketing campaigns
2. Monitor segment performance over time
3. Adjust segmentation parameters as needed
4. Integrate with CRM system for automation

---
Report generated by Janah Customer Segmentation System
For questions, contact: janah@hardwarestore.com
"""
    
    with open(os.path.join(output_dir, "sample_report.txt"), 'w') as f:
        f.write(report_content)
    
    print("  ✅ Created sample RFM data")
    print("  ✅ Created sample analysis summary")
    print("  ✅ Created sample report")

def create_demo_script(presentation_folder):
    """Create demo script for presentation"""
    print("🎬 Creating demo script...")
    
    demo_script = """# Janah Customer Segmentation - Demo Script

## 🎯 Demo Flow (5-7 minutes)

### 1. Introduction (30 seconds)
- "Welcome to the Janah Customer Segmentation Web Application"
- "This tool helps businesses analyze customer behavior and create targeted marketing segments"
- "Built with Flask backend and Streamlit for data science"

### 2. Home Page Tour (1 minute)
- Show the professional landing page
- Highlight the navigation bar (Home, Segmentation, Results)
- Point out the responsive design
- "Notice the modern blue/green theme and professional layout"

### 3. Data Source Selection (1 minute)
- Navigate to Segmentation page
- Show the two data source options:
  - **Default Dataset**: Online Retail from UCI repository
  - **Custom Upload**: CSV/XLSX files
- Demonstrate file upload drag & drop functionality
- "Users can either use our pre-loaded dataset or upload their own data"

### 4. Analysis Configuration (1 minute)
- Show clustering parameters:
  - Elbow method (automatic optimal clusters)
  - Manual cluster selection (3-6 segments)
- Explain RFM analysis:
  - **Recency**: Days since last purchase
  - **Frequency**: Number of transactions
  - **Monetary**: Total spending amount
- "The system automatically determines the optimal number of customer segments"

### 5. Run Analysis (1 minute)
- Click "Run Analysis" button
- Show progress tracking:
  - "Fetching dataset..."
  - "Cleaning data..."
  - "Running segmentation..."
  - "Analysis completed!"
- "Real-time progress updates keep users informed"

### 6. Results Display (1-2 minutes)
- Show comprehensive results page:
  - **Summary Statistics**: Total customers, segments, averages
  - **Segment Details**: Customer counts, percentages, characteristics
  - **Visualizations**: Charts and graphs
  - **RFM Progress**: Analysis completion status
- "The results provide actionable insights for business decisions"

### 7. Post-Segmentation Actions (1 minute)
- Demonstrate each action:
  - **📄 Download Report**: Generate comprehensive TXT report
  - **📊 Export Data**: Download CSV with segment data
  - **📧 Campaign Preview**: Show email templates for each segment
  - **🔗 Share Results**: URL sharing functionality
- "These features enable immediate business action"

### 8. Technical Highlights (30 seconds)
- Show folder structure
- Highlight key files:
  - `streamlit/segmentation.py` (core analysis)
  - `app/routes.py` (Flask backend)
  - `app/templates/results.html` (dynamic results)
- "Built with modern web technologies and best practices"

## 🎬 Demo Tips
- **Practice the flow** before presentation
- **Have sample data ready** for quick demonstration
- **Prepare answers** for common questions
- **Show both success and error handling**
- **Highlight responsive design** on different screen sizes

## ❓ Expected Questions & Answers

**Q: How does the clustering algorithm work?**
A: We use K-means clustering with the elbow method to determine optimal segments. The algorithm groups customers based on RFM metrics.

**Q: Can I use my own data?**
A: Yes! The application accepts CSV and XLSX files with the required columns (CustomerID, InvoiceDate, etc.).

**Q: How accurate are the segments?**
A: The accuracy depends on data quality. We clean the data by removing outliers and missing values for better results.

**Q: Can I export the results?**
A: Absolutely! You can download reports as TXT files and export segment data as CSV for further analysis.

**Q: Is this suitable for production use?**
A: The application is designed for demonstration but can be enhanced for production with additional security and scalability features.
"""
    
    with open(os.path.join(presentation_folder, "demo_script.md"), 'w') as f:
        f.write(demo_script)
    
    print("  ✅ Created demo script")

def create_deployment_guide(presentation_folder):
    """Create deployment guide"""
    print("🚀 Creating deployment guide...")
    
    deployment_guide = """# Deployment Guide

## Quick Deployment Options

### 1. Render (Recommended - Free)
1. Go to render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
5. Deploy!

### 2. Heroku
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Run: `git push heroku main`
4. Run: `heroku open`

### 3. Local Network
1. Modify run.py: `app.run(host='0.0.0.0', port=5000)`
2. Run: `python run.py`
3. Access from network: `http://YOUR_IP:5000`

## Required Files for Deployment
- ✅ requirements.txt
- ✅ Procfile (for Heroku)
- ✅ runtime.txt (Python version)
- ✅ app.json (platform config)
- ✅ All source code files

## Environment Variables
- SECRET_KEY: Flask secret key
- DATABASE_URL: (if using database)
- UPLOAD_FOLDER: data uploads directory
"""
    
    with open(os.path.join(presentation_folder, "deployment_guide.md"), 'w') as f:
        f.write(deployment_guide)
    
    print("  ✅ Created deployment guide")

def create_presentation_checklist(presentation_folder):
    """Create presentation checklist"""
    print("✅ Creating presentation checklist...")
    
    checklist = """# Presentation Checklist

## Before Presentation
- [ ] Test application locally
- [ ] Prepare sample data
- [ ] Practice demo flow
- [ ] Prepare answers for questions
- [ ] Check all files are ready

## During Presentation
- [ ] Start with introduction
- [ ] Show home page features
- [ ] Demonstrate data upload
- [ ] Run analysis with progress
- [ ] Show results and insights
- [ ] Demonstrate post-segmentation actions
- [ ] Highlight technical features
- [ ] Answer questions confidently

## After Presentation
- [ ] Provide access to live demo
- [ ] Share source code repository
- [ ] Offer deployment assistance
- [ ] Collect feedback

## Technical Requirements
- [ ] Python 3.8+ installed
- [ ] All dependencies installed
- [ ] Dataset downloaded
- [ ] Application runs without errors
- [ ] All features working
- [ ] Responsive design tested

## Files to Present
- [ ] Live application demo
- [ ] Source code structure
- [ ] Sample outputs
- [ ] Documentation
- [ ] Deployment instructions
"""
    
    with open(os.path.join(presentation_folder, "presentation_checklist.md"), 'w') as f:
        f.write(checklist)
    
    print("  ✅ Created presentation checklist")

def main():
    """Main function to prepare presentation"""
    print("🎯 Janah Customer Segmentation - Presentation Preparation")
    print("=" * 60)
    
    # Create presentation folder
    presentation_folder = create_presentation_folder()
    
    # Copy files
    copy_source_code(presentation_folder)
    copy_documentation(presentation_folder)
    create_sample_outputs(presentation_folder)
    create_demo_script(presentation_folder)
    create_deployment_guide(presentation_folder)
    create_presentation_checklist(presentation_folder)
    
    print("\n" + "=" * 60)
    print("🎉 Presentation preparation complete!")
    print(f"📁 All files ready in: {presentation_folder}")
    
    print("\n📋 Presentation folder structure:")
    for root, dirs, files in os.walk(presentation_folder):
        level = root.replace(presentation_folder, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}📄 {file}")
    
    print("\n🚀 Next Steps:")
    print("1. Test the application locally")
    print("2. Practice the demo flow")
    print("3. Prepare for questions")
    print("4. Deploy to your preferred platform")
    print("5. Present with confidence!")

if __name__ == "__main__":
    main() 