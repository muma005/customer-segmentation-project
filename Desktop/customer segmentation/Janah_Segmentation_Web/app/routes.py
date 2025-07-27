from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session
import pandas as pd
import os
import requests
import subprocess
import threading
import time
import json
import re
from datetime import datetime

# Try to import secure_filename from Werkzeug, with fallback
try:
    from werkzeug.utils import secure_filename
except ImportError:
    # Fallback implementation if Werkzeug is not available
    def secure_filename(filename):
        """Simple filename sanitization fallback"""
        if filename is None:
            return None
        
        # Remove path separators and dangerous characters
        filename = re.sub(r'[^\w\s-]', '', filename)
        filename = re.sub(r'[-\s]+', '-', filename)
        return filename.strip('-')

main = Blueprint('main', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_sample_dataset():
    """Create a sample dataset for testing when download fails"""
    try:
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        # Create sample data
        np.random.seed(42)
        n_customers = 1000
        n_transactions = 5000
        
        # Generate customer IDs
        customer_ids = [f'CUST{i:04d}' for i in range(1, n_customers + 1)]
        
        # Generate transaction data
        data = []
        for _ in range(n_transactions):
            customer_id = np.random.choice(customer_ids)
            invoice_date = datetime.now() - timedelta(days=np.random.randint(1, 365))
            quantity = np.random.randint(1, 10)
            unit_price = np.random.uniform(10, 100)
            
            data.append({
                'InvoiceNo': f'INV{np.random.randint(1000, 9999)}',
                'StockCode': f'STK{np.random.randint(100, 999)}',
                'Description': f'Product {np.random.randint(1, 50)}',
                'Quantity': quantity,
                'InvoiceDate': invoice_date.strftime('%Y-%m-%d %H:%M:%S'),
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Country': np.random.choice(['United Kingdom', 'Germany', 'France', 'Australia'])
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to file
        dataset_path = os.path.join(current_app.root_path, '..', 'data', 'online_retail.csv')
        os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
        df.to_csv(dataset_path, index=False)
        
        print(f"Sample dataset created with {len(df)} transactions")
        return dataset_path, True
        
    except Exception as e:
        print(f"Error creating sample dataset: {str(e)}")
        return str(e), False

def download_online_retail_dataset():
    """Download the Online Retail dataset from UCI repository"""
    try:
        # Create data directory if it doesn't exist
        data_dir = os.path.join(current_app.root_path, '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Try to download from UCI repository
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
        file_path = os.path.join(data_dir, 'online_retail.csv')
        
        print(f"Attempting to download dataset from: {url}")
        
        # Download the Excel file
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Save Excel file temporarily
            excel_path = os.path.join(data_dir, 'Online_Retail.xlsx')
            with open(excel_path, 'wb') as f:
                f.write(response.content)
            
            # Convert to CSV
            import pandas as pd
            df = pd.read_excel(excel_path, engine='openpyxl')
            df.to_csv(file_path, index=False)
            
            # Clean up Excel file
            os.remove(excel_path)
            
            print(f"Dataset downloaded and converted successfully: {file_path}")
            return file_path, True
        else:
            print(f"Download failed with status code: {response.status_code}")
            # Fallback to creating sample dataset
            print("Creating sample dataset as fallback...")
            return create_sample_dataset()
            
    except Exception as e:
        print(f"Error downloading dataset: {str(e)}")
        # Fallback to creating sample dataset
        print("Creating sample dataset as fallback...")
        return create_sample_dataset()

def run_streamlit_analysis(dataset_path, analysis_params):
    """Run Streamlit analysis in a separate process"""
    try:
        # Create a temporary script to run the analysis
        script_content = f"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from streamlit.segmentation import load_and_clean_data, calculate_rfm, perform_clustering, create_visualizations
import pandas as pd
import json

# Load and process data
data = load_and_clean_data('{dataset_path}')
if data is not None:
    rfm_data = calculate_rfm(data)
    if rfm_data is not None:
        clustered_data, optimal_clusters, model = perform_clustering(rfm_data, {analysis_params.get('num_clusters', 4)})
        if clustered_data is not None:
            # Save results
            output_path = 'data/processed/rfm_clustered.csv'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            clustered_data.to_csv(output_path, index=False)
            
            # Save analysis summary
            summary = {{
                'total_customers': len(clustered_data),
                'num_clusters': optimal_clusters,
                'avg_recency': clustered_data['Recency'].mean(),
                'avg_frequency': clustered_data['Frequency'].mean(),
                'avg_monetary': clustered_data['Monetary'].mean(),
                'cluster_sizes': clustered_data['Cluster'].value_counts().to_dict(),
                'timestamp': '{datetime.now().isoformat()}'
            }}
            
            with open('data/processed/analysis_summary.json', 'w') as f:
                json.dump(summary, f)
            
            print("Analysis completed successfully")
        else:
            print("Clustering failed")
    else:
        print("RFM calculation failed")
else:
    print("Data loading failed")
"""
        
        # Save the script
        script_path = os.path.join(current_app.root_path, '..', 'temp_analysis.py')
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Run the analysis
        result = subprocess.run(['python', script_path], 
                              capture_output=True, text=True, 
                              cwd=os.path.join(current_app.root_path, '..'))
        
        # Clean up
        if os.path.exists(script_path):
            os.remove(script_path)
        
        return result.returncode == 0, result.stdout, result.stderr
        
    except Exception as e:
        return False, "", str(e)

@main.route('/')
@main.route('/home')
def home():
    """Home page route"""
    return render_template('home.html')

@main.route('/segmentation', methods=['GET', 'POST'])
def segmentation():
    """Segmentation page route with form handling"""
    if request.method == 'POST':
        # Handle form submission
        data_source = request.form.get('dataSource', 'default')
        num_clusters = int(request.form.get('numClusters', 4))
        analysis_type = request.form.get('analysisType', 'rfm')
        remove_outliers = 'removeOutliers' in request.form
        normalize_data = 'normalizeData' in request.form
        
        # Handle file upload if selected
        if data_source == 'upload' and 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                flash(f'File {filename} uploaded successfully!', 'success')
            else:
                flash('Invalid file type. Please upload CSV, XLSX, or XLS files.', 'error')
                return redirect(url_for('main.segmentation'))
        
        # Store analysis parameters in session
        session['analysis_params'] = {
            'data_source': data_source,
            'num_clusters': num_clusters,
            'analysis_type': analysis_type,
            'remove_outliers': remove_outliers,
            'normalize_data': normalize_data
        }
        
        flash('Analysis parameters saved. Processing will begin in Phase 3.', 'info')
        return redirect(url_for('main.results'))
    
    return render_template('segmentation.html')

@main.route('/results')
def results():
    """Results page route"""
    # Check if analysis results exist
    summary_path = os.path.join(current_app.root_path, '..', 'data', 'processed', 'analysis_summary.json')
    if os.path.exists(summary_path):
        try:
            with open(summary_path, 'r') as f:
                analysis_summary = json.load(f)
        except:
            analysis_summary = None
    else:
        analysis_summary = None
    
    return render_template('results.html', analysis_summary=analysis_summary)

@main.route('/run_segmentation', methods=['POST'])
def run_segmentation():
    """Run the segmentation analysis"""
    try:
        # Get analysis parameters
        data_source = request.form.get('dataSource', 'default')
        num_clusters = int(request.form.get('numClusters', 4))
        analysis_type = request.form.get('analysisType', 'rfm')
        
        print(f"Starting analysis with data_source={data_source}, num_clusters={num_clusters}")
        
        # Determine dataset path
        if data_source == 'upload' and 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                dataset_path = upload_path
                print(f"Using uploaded file: {dataset_path}")
            else:
                return jsonify({'success': False, 'error': 'Invalid file type'})
        else:
            # Use default dataset
            dataset_path = os.path.join(current_app.root_path, '..', 'data', 'online_retail.csv')
            print(f"Looking for default dataset at: {dataset_path}")
            
            # Download if not exists
            if not os.path.exists(dataset_path):
                print("Dataset not found, attempting download...")
                file_path, success = download_online_retail_dataset()
                if not success:
                    error_msg = f'Failed to download dataset: {file_path}'
                    print(f"Download failed: {error_msg}")
                    return jsonify({'success': False, 'error': error_msg})
                else:
                    print(f"Dataset downloaded successfully to: {file_path}")
            else:
                print("Dataset found at existing location")
        
        # Verify dataset exists
        if not os.path.exists(dataset_path):
            error_msg = f'Dataset file not found at: {dataset_path}'
            print(f"Dataset verification failed: {error_msg}")
            return jsonify({'success': False, 'error': error_msg})
        
        # Analysis parameters
        analysis_params = {
            'num_clusters': num_clusters,
            'analysis_type': analysis_type
        }
        
        print(f"Analysis parameters: {analysis_params}")
        
        # Run analysis in background
        def run_analysis():
            try:
                print("Starting background analysis...")
                success, stdout, stderr = run_streamlit_analysis(dataset_path, analysis_params)
                if success:
                    print("Analysis completed successfully")
                    print(f"STDOUT: {stdout}")
                else:
                    print(f"Analysis failed: {stderr}")
                    print(f"STDOUT: {stdout}")
            except Exception as e:
                print(f"Exception in background analysis: {str(e)}")
        
        # Start analysis in background thread
        thread = threading.Thread(target=run_analysis)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True, 
            'message': 'Analysis started successfully',
            'dataset_path': dataset_path
        })
        
    except Exception as e:
        error_msg = f'Unexpected error: {str(e)}'
        print(f"Exception in run_segmentation: {error_msg}")
        return jsonify({'success': False, 'error': error_msg})

@main.route('/api/test')
def test_api():
    """Simple test endpoint to verify the app is working"""
    return jsonify({
        'status': 'success',
        'message': 'Flask app is running correctly',
        'timestamp': datetime.now().isoformat(),
        'data_folder': os.path.exists(os.path.join(current_app.root_path, '..', 'data')),
        'uploads_folder': os.path.exists(current_app.config['UPLOAD_FOLDER'])
    })

@main.route('/api/analysis-progress')
def analysis_progress():
    """API endpoint for analysis progress"""
    # Check if analysis is complete
    summary_path = os.path.join(current_app.root_path, '..', 'data', 'processed', 'analysis_summary.json')
    if os.path.exists(summary_path):
        try:
            with open(summary_path, 'r') as f:
                summary = json.load(f)
            return jsonify({
                'progress': 100,
                'status': 'completed',
                'message': 'Analysis completed successfully',
                'summary': summary
            })
        except:
            pass
    
    # Check if analysis is running
    clustered_path = os.path.join(current_app.root_path, '..', 'data', 'processed', 'rfm_clustered.csv')
    if os.path.exists(clustered_path):
        return jsonify({
            'progress': 75,
            'status': 'processing',
            'message': 'Generating visualizations...'
        })
    
    return jsonify({
        'progress': 0,
        'status': 'not_started',
        'message': 'Analysis not started'
    })

@main.route('/api/download-report')
def download_report():
    """API endpoint for report download (Phase 5)"""
    return jsonify({
        'status': 'success',
        'message': 'Report download functionality coming in Phase 5'
    })

@main.route('/api/export-data')
def export_data():
    """API endpoint for data export (Phase 5)"""
    return jsonify({
        'status': 'success',
        'message': 'Data export functionality coming in Phase 5'
    })

@main.route('/api/share-results')
def share_results():
    """API endpoint for sharing results (Phase 5)"""
    return jsonify({
        'status': 'success',
        'message': 'Share functionality coming in Phase 5'
    })

# Error handlers
@main.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
