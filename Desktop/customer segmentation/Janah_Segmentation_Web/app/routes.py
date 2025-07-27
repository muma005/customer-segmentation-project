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

def download_online_retail_dataset():
    """Download the Online Retail dataset from UCI repository"""
    try:
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
        data_dir = os.path.join(current_app.root_path, '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        file_path = os.path.join(data_dir, 'online_retail.csv')
        
        # Download the Excel file
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Save as Excel first
        excel_path = os.path.join(data_dir, 'online_retail.xlsx')
        with open(excel_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Convert to CSV
        df = pd.read_excel(excel_path)
        df.to_csv(file_path, index=False)
        
        # Remove Excel file
        os.remove(excel_path)
        
        return file_path, True
        
    except Exception as e:
        return str(e), False

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
        
        # Determine dataset path
        if data_source == 'upload' and 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                dataset_path = upload_path
            else:
                return jsonify({'success': False, 'error': 'Invalid file type'})
        else:
            # Use default dataset
            dataset_path = os.path.join(current_app.root_path, '..', 'data', 'online_retail.csv')
            
            # Download if not exists
            if not os.path.exists(dataset_path):
                file_path, success = download_online_retail_dataset()
                if not success:
                    return jsonify({'success': False, 'error': f'Failed to download dataset: {file_path}'})
        
        # Analysis parameters
        analysis_params = {
            'num_clusters': num_clusters,
            'analysis_type': analysis_type
        }
        
        # Run analysis in background
        def run_analysis():
            success, stdout, stderr = run_streamlit_analysis(dataset_path, analysis_params)
            if success:
                print("Analysis completed successfully")
            else:
                print(f"Analysis failed: {stderr}")
        
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
        return jsonify({'success': False, 'error': str(e)})

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
