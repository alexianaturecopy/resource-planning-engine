"""
Validation Script for Resource Planning Engine
Tests data loading, optimization, and application readiness

Author: Ye(Alexia) Quan
"""

import sys
import pandas as pd
import numpy as np

def test_data_files():
    """Test that all data files exist and load correctly"""
    print("Test 1: Data Files")
    print("-" * 50)
    
    files_to_check = [
        'data/resource_requests.csv',
        'data/historical_roi.csv',
        'data/service_metrics.csv',
        'data/process_quality.csv',
        'data/constraints.csv'
    ]
    
    all_good = True
    for file in files_to_check:
        try:
            df = pd.read_csv(file)
            print(f"  ✓ {file}: {len(df)} records")
        except Exception as e:
            print(f"  ✗ {file}: ERROR - {e}")
            all_good = False
    
    return all_good

def test_optimization_module():
    """Test that optimization module works"""
    print("\nTest 2: Optimization Module")
    print("-" * 50)
    
    try:
        from src.optimization import optimize_budget_allocation
        
        # Load sample data
        resource_requests = pd.read_csv('data/resource_requests.csv')
        constraints_df = pd.read_csv('data/constraints.csv')
        total_budget = constraints_df[constraints_df['constraint_type'] == 'total_budget']['value'].values[0]
        
        # Run optimization
        result = optimize_budget_allocation(resource_requests, total_budget)
        
        print(f"  ✓ Optimization completed")
        print(f"  ✓ Status: {result['status']}")
        print(f"  ✓ Total allocated: ${result['total_allocated']:,.0f}")
        print(f"  ✓ Projects funded: {len(result['funded_projects'])}")
        print(f"  ✓ Blended ROI: {result['blended_roi']:.2f}x")
        
        if result['status'] != 'Optimal':
            print(f"  ⚠ Warning: Optimization status is {result['status']}")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Optimization module ERROR: {e}")
        return False

def test_dependencies():
    """Test that required packages are installed"""
    print("\nTest 3: Dependencies")
    print("-" * 50)
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'pulp'
    ]
    
    all_good = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package} installed")
        except ImportError:
            print(f"  ✗ {package} NOT installed")
            all_good = False
    
    return all_good

def test_data_quality():
    """Test data quality and consistency"""
    print("\nTest 4: Data Quality")
    print("-" * 50)
    
    try:
        # Load data
        resource_requests = pd.read_csv('data/resource_requests.csv')
        constraints_df = pd.read_csv('data/constraints.csv')
        
        # Check for required columns
        required_cols = ['service_line', 'budget_requested', 'min_viable_budget', 'expected_roi', 'strategic_priority']
        missing_cols = [col for col in required_cols if col not in resource_requests.columns]
        
        if missing_cols:
            print(f"  ✗ Missing columns: {missing_cols}")
            return False
        
        print(f"  ✓ All required columns present")
        
        # Check for data consistency
        total_budget = constraints_df[constraints_df['constraint_type'] == 'total_budget']['value'].values[0]
        total_requested = resource_requests['budget_requested'].sum()
        
        print(f"  ✓ Total budget: ${total_budget:,.0f}")
        print(f"  ✓ Total requested: ${total_requested:,.0f}")
        print(f"  ✓ Gap: ${total_requested - total_budget:,.0f} ({'over' if total_requested > total_budget else 'under'}-requested)")
        
        # Check ROI values are reasonable
        avg_roi = resource_requests['expected_roi'].mean()
        print(f"  ✓ Average expected ROI: {avg_roi:.2f}x")
        
        if avg_roi < 1.0:
            print(f"  ⚠ Warning: Average ROI below 1.0x")
        
        return True
    except Exception as e:
        print(f"  ✗ Data quality check ERROR: {e}")
        return False

def main():
    """Run all validation tests"""
    print("\n" + "=" * 50)
    print("RESOURCE PLANNING ENGINE - VALIDATION")
    print("=" * 50 + "\n")
    
    tests = [
        ("Data Files", test_data_files),
        ("Dependencies", test_dependencies),
        ("Data Quality", test_data_quality),
        ("Optimization Module", test_optimization_module)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    all_passed = all(result for _, result in results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ALL VALIDATION TESTS PASSED!")
        print("=" * 50)
        print("\nDashboard is ready to launch!")
        print("\nTo run the dashboard:")
        print("  streamlit run app.py")
        print("\nThen navigate to: http://localhost:8501")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 50)
        print("\nPlease fix the issues above before launching the dashboard.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
