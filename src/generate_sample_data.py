"""
Generate Realistic Sample Data for Resource Planning Engine
Context: B2B E-Commerce Agency providing Marketing, Branding, Automation Solutions

Generates:
- Resource requests by service line
- Historical ROI data
- Service delivery metrics
- Process quality data (Six Sigma)
- Budget constraints

Author: Ye(Alexia) Quan
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def generate_resource_requests():
    """
    Generate resource allocation requests from different service lines
    
    Service lines for B2B e-commerce agency:
    - Digital Marketing Campaigns
    - Brand Strategy & Development
    - Marketing Automation Implementation
    - E-Commerce Platform Optimization
    - Content Marketing
    - Social Media Management
    - Email Marketing Automation
    - SEO/SEM Services
    - Analytics & Reporting
    - Client Success & Support
    """
    
    service_lines = [
        {
            'service_line': 'Digital Marketing Campaigns',
            'budget_requested': 3_500_000,
            'min_viable_budget': 2_000_000,
            'expected_roi': 2.8,
            'strategic_priority': 5,
            'success_probability': 0.85,
            'rationale': 'Core revenue driver, proven ROI, high client demand'
        },
        {
            'service_line': 'Marketing Automation',
            'budget_requested': 2_800_000,
            'min_viable_budget': 1_500_000,
            'expected_roi': 3.2,
            'strategic_priority': 5,
            'success_probability': 0.90,
            'rationale': 'High-margin service, recurring revenue potential, strategic differentiator'
        },
        {
            'service_line': 'Brand Strategy',
            'budget_requested': 2_200_000,
            'min_viable_budget': 1_200_000,
            'expected_roi': 2.4,
            'strategic_priority': 4,
            'success_probability': 0.80,
            'rationale': 'Premium positioning, attracts enterprise clients'
        },
        {
            'service_line': 'E-Commerce Optimization',
            'budget_requested': 3_000_000,
            'min_viable_budget': 1_800_000,
            'expected_roi': 2.9,
            'strategic_priority': 5,
            'success_probability': 0.88,
            'rationale': 'Growing market, high conversion rates, technical expertise'
        },
        {
            'service_line': 'Content Marketing',
            'budget_requested': 1_800_000,
            'min_viable_budget': 1_000_000,
            'expected_roi': 2.2,
            'strategic_priority': 3,
            'success_probability': 0.75,
            'rationale': 'Supports other services, builds brand authority'
        },
        {
            'service_line': 'Social Media Management',
            'budget_requested': 1_500_000,
            'min_viable_budget': 800_000,
            'expected_roi': 1.9,
            'strategic_priority': 3,
            'success_probability': 0.70,
            'rationale': 'Lower margins, competitive market, client acquisition tool'
        },
        {
            'service_line': 'Email Marketing',
            'budget_requested': 1_200_000,
            'min_viable_budget': 600_000,
            'expected_roi': 3.5,
            'strategic_priority': 4,
            'success_probability': 0.92,
            'rationale': 'Highest ROI, automated delivery, scalable'
        },
        {
            'service_line': 'SEO/SEM Services',
            'budget_requested': 2_500_000,
            'min_viable_budget': 1_500_000,
            'expected_roi': 2.6,
            'strategic_priority': 4,
            'success_probability': 0.82,
            'rationale': 'Long-term value, recurring revenue, competitive advantage'
        },
        {
            'service_line': 'Analytics & Reporting',
            'budget_requested': 1_500_000,
            'min_viable_budget': 900_000,
            'expected_roi': 2.0,
            'strategic_priority': 3,
            'success_probability': 0.85,
            'rationale': 'Client retention tool, upsell opportunity'
        },
        {
            'service_line': 'Client Success',
            'budget_requested': 1_800_000,
            'min_viable_budget': 1_200_000,
            'expected_roi': 1.8,
            'strategic_priority': 4,
            'success_probability': 0.90,
            'rationale': 'Critical for retention, reduces churn, enables expansion'
        }
    ]
    
    df = pd.DataFrame(service_lines)
    df['expected_return'] = df['budget_requested'] * df['expected_roi']
    df['roi_score'] = df['expected_roi'] * df['strategic_priority'] * df['success_probability']
    
    return df

def generate_historical_roi():
    """Generate historical ROI data for service lines over past 3 years"""
    
    service_lines = [
        'Digital Marketing Campaigns',
        'Marketing Automation',
        'Brand Strategy',
        'E-Commerce Optimization',
        'Content Marketing',
        'Social Media Management',
        'Email Marketing',
        'SEO/SEM Services',
        'Analytics & Reporting',
        'Client Success'
    ]
    
    years = [2022, 2023, 2024]
    
    data = []
    for year in years:
        for service in service_lines:
            # Base ROI with variation by service and year
            if service == 'Email Marketing':
                base_roi = 3.5
            elif service == 'Marketing Automation':
                base_roi = 3.2
            elif service == 'E-Commerce Optimization':
                base_roi = 2.9
            elif service == 'Digital Marketing Campaigns':
                base_roi = 2.8
            elif service == 'SEO/SEM Services':
                base_roi = 2.6
            elif service == 'Brand Strategy':
                base_roi = 2.4
            elif service == 'Content Marketing':
                base_roi = 2.2
            elif service == 'Analytics & Reporting':
                base_roi = 2.0
            elif service == 'Social Media Management':
                base_roi = 1.9
            else:
                base_roi = 1.8
            
            # ROI improves over years (learning curve)
            year_factor = 1 + (year - 2022) * 0.05
            roi = base_roi * year_factor * np.random.uniform(0.95, 1.05)
            
            investment = np.random.uniform(800_000, 3_000_000)
            revenue_generated = investment * roi
            
            # Project metrics
            projects_delivered = int(np.random.uniform(15, 60))
            avg_project_value = revenue_generated / projects_delivered
            
            data.append({
                'year': year,
                'service_line': service,
                'investment': investment,
                'revenue_generated': revenue_generated,
                'roi': roi,
                'projects_delivered': projects_delivered,
                'avg_project_value': avg_project_value,
                'client_satisfaction': np.random.uniform(4.0, 4.8)
            })
    
    return pd.DataFrame(data)

def generate_service_metrics():
    """Generate service delivery metrics for Six Sigma analysis"""
    
    # Generate 90 days of data
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    
    data = []
    for date in dates:
        # Onboarding metrics
        onboarding_time = np.random.normal(21, 3)  # Mean 21 days, currently above 14-day target
        onboarding_time = np.clip(onboarding_time, 12, 35)
        
        # Project delivery metrics
        projects_completed = np.random.poisson(3)  # Average 3 projects per day
        on_time_delivery = np.random.binomial(projects_completed, 0.88)  # 88% on-time rate
        
        # Quality metrics
        defects = np.random.binomial(projects_completed, 0.08)  # 8% defect rate (target: 3%)
        rework_hours = defects * np.random.uniform(8, 24)
        
        # Client satisfaction (daily average)
        satisfaction_score = np.random.normal(4.2, 0.3)  # Mean 4.2, target 4.5
        satisfaction_score = np.clip(satisfaction_score, 3.0, 5.0)
        
        # Resource utilization
        team_utilization = np.random.normal(65, 8)  # 65% utilization (room for improvement)
        team_utilization = np.clip(team_utilization, 45, 85)
        
        # Cycle time metrics
        lead_to_kickoff_days = np.random.normal(14, 4)  # Time from lead to project start
        kickoff_to_launch_days = np.random.normal(30, 7)  # Project duration
        
        data.append({
            'date': date,
            'onboarding_time_days': onboarding_time,
            'projects_completed': projects_completed,
            'on_time_deliveries': on_time_delivery,
            'on_time_rate': on_time_delivery / projects_completed if projects_completed > 0 else 0,
            'defects': defects,
            'defect_rate': defects / projects_completed if projects_completed > 0 else 0,
            'rework_hours': rework_hours,
            'client_satisfaction': satisfaction_score,
            'team_utilization_pct': team_utilization,
            'lead_to_kickoff_days': lead_to_kickoff_days,
            'kickoff_to_launch_days': kickoff_to_launch_days,
            'total_cycle_time': lead_to_kickoff_days + kickoff_to_launch_days
        })
    
    return pd.DataFrame(data)

def generate_process_quality():
    """Generate process quality data for Six Sigma control charts"""
    
    # Generate 90 days of process metrics
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    
    data = []
    for date in dates:
        # Process metrics with variation
        
        # Requirements clarity score (1-10)
        requirements_clarity = np.random.normal(6.5, 1.5)
        requirements_clarity = np.clip(requirements_clarity, 1, 10)
        
        # Resource availability score (1-10)
        resource_availability = np.random.normal(7.0, 1.2)
        resource_availability = np.clip(resource_availability, 1, 10)
        
        # Communication effectiveness (1-10)
        communication_score = np.random.normal(7.5, 1.0)
        communication_score = np.clip(communication_score, 1, 10)
        
        # Technical execution quality (1-10)
        technical_quality = np.random.normal(8.0, 1.0)
        technical_quality = np.clip(technical_quality, 1, 10)
        
        # Process compliance (% adherence to standards)
        process_compliance = np.random.normal(75, 10)
        process_compliance = np.clip(process_compliance, 50, 100)
        
        # Defect categories
        unclear_requirements = np.random.poisson(0.35)
        resource_unavailable = np.random.poisson(0.28)
        scope_creep = np.random.poisson(0.18)
        technical_issues = np.random.poisson(0.12)
        communication_gaps = np.random.poisson(0.08)
        
        data.append({
            'date': date,
            'requirements_clarity': requirements_clarity,
            'resource_availability': resource_availability,
            'communication_score': communication_score,
            'technical_quality': technical_quality,
            'process_compliance_pct': process_compliance,
            'defect_unclear_requirements': unclear_requirements,
            'defect_resource_unavailable': resource_unavailable,
            'defect_scope_creep': scope_creep,
            'defect_technical': technical_issues,
            'defect_communication': communication_gaps,
            'total_defects': unclear_requirements + resource_unavailable + scope_creep + technical_issues + communication_gaps
        })
    
    return pd.DataFrame(data)

def generate_constraints():
    """Generate budget and operational constraints"""
    
    constraints = [
        {
            'constraint_type': 'total_budget',
            'value': 18_000_000,
            'unit': 'USD',
            'description': 'Total available budget for all service lines'
        },
        {
            'constraint_type': 'max_headcount_growth',
            'value': 25,
            'unit': 'Percentage',
            'description': 'Maximum year-over-year headcount growth'
        },
        {
            'constraint_type': 'min_cash_runway_months',
            'value': 18,
            'unit': 'Months',
            'description': 'Minimum cash runway to maintain'
        },
        {
            'constraint_type': 'max_single_service_allocation',
            'value': 4_000_000,
            'unit': 'USD',
            'description': 'Maximum budget for any single service line'
        },
        {
            'constraint_type': 'min_roi_threshold',
            'value': 1.5,
            'unit': 'Ratio',
            'description': 'Minimum acceptable ROI for funded projects'
        },
        {
            'constraint_type': 'min_funded_projects',
            'value': 6,
            'unit': 'Count',
            'description': 'Minimum number of service lines to fund'
        },
        {
            'constraint_type': 'target_utilization',
            'value': 75,
            'unit': 'Percentage',
            'description': 'Target team utilization rate'
        },
        {
            'constraint_type': 'max_contractor_pct',
            'value': 20,
            'unit': 'Percentage',
            'description': 'Maximum percentage of workforce as contractors'
        }
    ]
    
    return pd.DataFrame(constraints)

def main():
    """Generate all sample data files"""
    
    import os
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    print("Generating Resource Planning Engine sample data...")
    
    # Generate datasets
    print("  1/5 Generating resource requests...")
    resource_requests = generate_resource_requests()
    resource_requests.to_csv('data/resource_requests.csv', index=False)
    print(f"      Created: data/resource_requests.csv ({len(resource_requests)} records)")
    
    print("  2/5 Generating historical ROI data...")
    historical_roi = generate_historical_roi()
    historical_roi.to_csv('data/historical_roi.csv', index=False)
    print(f"      Created: data/historical_roi.csv ({len(historical_roi)} records)")
    
    print("  3/5 Generating service metrics...")
    service_metrics = generate_service_metrics()
    service_metrics.to_csv('data/service_metrics.csv', index=False)
    print(f"      Created: data/service_metrics.csv ({len(service_metrics)} records)")
    
    print("  4/5 Generating process quality data...")
    process_quality = generate_process_quality()
    process_quality.to_csv('data/process_quality.csv', index=False)
    print(f"      Created: data/process_quality.csv ({len(process_quality)} records)")
    
    print("  5/5 Generating constraints...")
    constraints = generate_constraints()
    constraints.to_csv('data/constraints.csv', index=False)
    print(f"      Created: data/constraints.csv ({len(constraints)} records)")
    
    print("\n✅ All sample data generated successfully!")
    print("\nData Summary:")
    print(f"  - Total budget available: ${constraints[constraints['constraint_type']=='total_budget']['value'].values[0]:,.0f}")
    print(f"  - Total budget requested: ${resource_requests['budget_requested'].sum():,.0f}")
    print(f"  - Gap (over-requested): ${resource_requests['budget_requested'].sum() - constraints[constraints['constraint_type']=='total_budget']['value'].values[0]:,.0f}")
    print(f"  - Service lines: {len(resource_requests)}")
    print(f"  - Optimization required: YES (requests exceed budget)")
    
    print("\nHistorical Performance:")
    print(f"  - Avg ROI 2022: {historical_roi[historical_roi['year']==2022]['roi'].mean():.2f}x")
    print(f"  - Avg ROI 2023: {historical_roi[historical_roi['year']==2023]['roi'].mean():.2f}x")
    print(f"  - Avg ROI 2024: {historical_roi[historical_roi['year']==2024]['roi'].mean():.2f}x")
    
    print("\nProcess Quality (Current State):")
    print(f"  - Avg onboarding time: {service_metrics['onboarding_time_days'].mean():.1f} days (target: 14 days)")
    print(f"  - Avg defect rate: {service_metrics['defect_rate'].mean()*100:.1f}% (target: 3%)")
    print(f"  - Avg satisfaction: {service_metrics['client_satisfaction'].mean():.2f}/5.0 (target: 4.5)")
    print(f"  - Avg utilization: {service_metrics['team_utilization_pct'].mean():.1f}% (target: 75%)")

if __name__ == "__main__":
    main()
