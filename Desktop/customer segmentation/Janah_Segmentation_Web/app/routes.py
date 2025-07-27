from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
import pandas as pd
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        
        # Store analysis parameters in session (for Phase 3)
        # session['analysis_params'] = {
        #     'data_source': data_source,
        #     'num_clusters': num_clusters,
        #     'analysis_type': analysis_type,
        #     'remove_outliers': remove_outliers,
        #     'normalize_data': normalize_data
        # }
        
        flash('Analysis parameters saved. Processing will begin in Phase 3.', 'info')
        return redirect(url_for('main.results'))
    
    return render_template('segmentation.html')

@main.route('/results')
def results():
    """Results page route"""
    # Placeholder data for Phase 2
    # In Phase 3, this will display actual analysis results
    return render_template('results.html')

@main.route('/api/analysis-progress')
def analysis_progress():
    """API endpoint for analysis progress (Phase 3)"""
    # Placeholder for progress tracking
    return jsonify({
        'progress': 0,
        'status': 'Not started',
        'message': 'Analysis functionality coming in Phase 3'
    })

@main.route('/api/download-report')
def download_report():
    """API endpoint for report download (Phase 5)"""
    # Placeholder for report generation
    return jsonify({
        'status': 'success',
        'message': 'Report download functionality coming in Phase 5'
    })

@main.route('/api/export-data')
def export_data():
    """API endpoint for data export (Phase 5)"""
    # Placeholder for data export
    return jsonify({
        'status': 'success',
        'message': 'Data export functionality coming in Phase 5'
    })

@main.route('/api/share-results')
def share_results():
    """API endpoint for sharing results (Phase 5)"""
    # Placeholder for sharing functionality
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
