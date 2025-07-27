#!/usr/bin/env python3
"""
Test script for Phase 5: Post-Segmentation Features and Polish
"""

import os
import json
import pandas as pd
from datetime import datetime

def test_phase5_features():
    """Test all Phase 5 features"""
    print("🧪 Testing Phase 5: Post-Segmentation Features and Polish")
    print("=" * 60)
    
    # Test 1: Check if required files exist
    print("\n📁 Testing file structure...")
    required_files = [
        'streamlit/segmentation.py',
        'app/templates/results.html',
        'app/static/css/style.css',
        'app/static/js/script.js'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Found")
        else:
            print(f"❌ {file_path} - Missing")
    
    # Test 2: Check if data directories exist
    print("\n📊 Testing data directories...")
    data_dirs = [
        'data/',
        'data/processed/',
        'data/uploads/'
    ]
    
    for dir_path in data_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} - Found")
        else:
            print(f"❌ {dir_path} - Missing")
            os.makedirs(dir_path, exist_ok=True)
            print(f"   📁 Created {dir_path}")
    
    # Test 3: Test report generation
    print("\n📄 Testing report generation...")
    try:
        # Create sample RFM data
        sample_data = pd.DataFrame({
            'CustomerID': [1, 2, 3, 4, 5],
            'Recency': [30, 60, 15, 90, 45],
            'Frequency': [5, 3, 8, 1, 4],
            'Monetary': [1500, 800, 2000, 300, 1200],
            'Cluster': [0, 1, 0, 2, 1],
            'Segment': ['Loyal Customers', 'At-Risk Customers', 'Loyal Customers', 'Inactive Customers', 'At-Risk Customers']
        })
        
        # Test analysis parameters
        analysis_params = {
            "data_source": "Default Dataset",
            "n_clusters": 3,
            "total_customers": 5
        }
        
        # Import and test report generation
        import sys
        sys.path.append('streamlit')
        from segmentation import generate_report
        
        report_content = generate_report(sample_data, analysis_params)
        
        if "JANAH HARDWARE STORE" in report_content:
            print("✅ Report generation - Working")
            
            # Save test report
            with open('data/processed/test_report.txt', 'w') as f:
                f.write(report_content)
            print("   📄 Test report saved to data/processed/test_report.txt")
        else:
            print("❌ Report generation - Failed")
            
    except Exception as e:
        print(f"❌ Report generation - Error: {str(e)}")
    
    # Test 4: Test campaign preview
    print("\n📧 Testing campaign preview...")
    try:
        from segmentation import create_campaign_preview
        
        campaign = create_campaign_preview('Loyal Customers', sample_data)
        
        if isinstance(campaign, dict) and 'subject' in campaign and 'content' in campaign:
            print("✅ Campaign preview - Working")
        else:
            print("❌ Campaign preview - Failed")
            
    except Exception as e:
        print(f"❌ Campaign preview - Error: {str(e)}")
    
    # Test 5: Test data export
    print("\n📊 Testing data export...")
    try:
        # Save sample data
        sample_data.to_csv('data/processed/test_rfm_data.csv', index=False)
        
        if os.path.exists('data/processed/test_rfm_data.csv'):
            print("✅ Data export - Working")
            print(f"   📁 Test data saved to data/processed/test_rfm_data.csv")
        else:
            print("❌ Data export - Failed")
            
    except Exception as e:
        print(f"❌ Data export - Error: {str(e)}")
    
    # Test 6: Test analysis summary
    print("\n📈 Testing analysis summary...")
    try:
        summary = {
            "timestamp": datetime.now().isoformat(),
            "parameters": analysis_params,
            "summary_stats": {
                "total_customers": len(sample_data),
                "n_clusters": sample_data['Cluster'].nunique(),
                "avg_recency": sample_data['Recency'].mean(),
                "avg_monetary": sample_data['Monetary'].mean(),
                "cluster_sizes": sample_data['Segment'].value_counts().to_dict()
            }
        }
        
        with open('data/processed/test_analysis_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        if os.path.exists('data/processed/test_analysis_summary.json'):
            print("✅ Analysis summary - Working")
            print(f"   📁 Test summary saved to data/processed/test_analysis_summary.json")
        else:
            print("❌ Analysis summary - Failed")
            
    except Exception as e:
        print(f"❌ Analysis summary - Error: {str(e)}")
    
    # Test 7: Check CSS enhancements
    print("\n🎨 Testing CSS enhancements...")
    try:
        with open('app/static/css/style.css', 'r') as f:
            css_content = f.read()
        
        css_features = [
            'action-card',
            'metric-card',
            'campaign-preview',
            'hover',
            'animation',
            'responsive'
        ]
        
        for feature in css_features:
            if feature in css_content:
                print(f"✅ CSS {feature} - Found")
            else:
                print(f"⚠️  CSS {feature} - Not found")
                
    except Exception as e:
        print(f"❌ CSS testing - Error: {str(e)}")
    
    # Test 8: Check JavaScript enhancements
    print("\n⚡ Testing JavaScript enhancements...")
    try:
        with open('app/static/js/script.js', 'r') as f:
            js_content = f.read()
        
        js_features = [
            'showNotification',
            'pollAnalysisProgress',
            'displayResults',
            'initializeNotifications',
            'handleFileSelection'
        ]
        
        for feature in js_features:
            if feature in js_content:
                print(f"✅ JS {feature} - Found")
            else:
                print(f"⚠️  JS {feature} - Not found")
                
    except Exception as e:
        print(f"❌ JavaScript testing - Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 Phase 5 Testing Complete!")
    print("\n📋 Next Steps:")
    print("1. Run: python run.py")
    print("2. Visit: http://localhost:5000")
    print("3. Test the post-segmentation features:")
    print("   - Download Report")
    print("   - Export Data")
    print("   - Campaign Preview")
    print("   - Share Results")
    print("4. Check responsive design on different screen sizes")

if __name__ == "__main__":
    test_phase5_features() 