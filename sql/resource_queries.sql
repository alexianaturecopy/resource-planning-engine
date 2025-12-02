-- Resource Planning SQL Queries
-- Integration with ERP systems (NetSuite, SAP, Workday, etc.)
-- Author: Ye(Alexia) Quan

-- ================================================
-- 1. RESOURCE REQUEST SUMMARY
-- ================================================
-- Pull current budget requests from department heads
-- Maps to: resource_requests.csv

SELECT 
    d.department_name as service_line,
    br.fy2025_budget_request as budget_requested,
    br.minimum_viable_budget as min_viable_budget,
    br.expected_roi,
    br.strategic_priority_score as strategic_priority,
    br.success_probability,
    br.business_rationale as rationale
FROM budget_requests br
JOIN departments d ON br.department_id = d.department_id
WHERE br.fiscal_year = 2025
    AND br.status = 'SUBMITTED'
ORDER BY br.strategic_priority_score DESC, br.expected_roi DESC;

-- ================================================
-- 2. HISTORICAL ROI PERFORMANCE
-- ================================================
-- Calculate actual ROI by service line over past 3 years
-- Maps to: historical_roi.csv

SELECT 
    YEAR(t.transaction_date) as year,
    d.department_name as service_line,
    SUM(t.investment_amount) as investment,
    SUM(t.revenue_generated) as revenue_generated,
    SUM(t.revenue_generated) / NULLIF(SUM(t.investment_amount), 0) as roi,
    COUNT(DISTINCT t.project_id) as projects_delivered,
    AVG(t.revenue_generated) as avg_project_value,
    AVG(cs.satisfaction_score) as client_satisfaction
FROM financial_transactions t
JOIN departments d ON t.department_id = d.department_id
LEFT JOIN client_satisfaction cs ON t.project_id = cs.project_id
WHERE t.transaction_type = 'PROJECT_INVESTMENT'
    AND YEAR(t.transaction_date) BETWEEN YEAR(CURRENT_DATE) - 3 AND YEAR(CURRENT_DATE) - 1
GROUP BY YEAR(t.transaction_date), d.department_name
ORDER BY year DESC, roi DESC;

-- ================================================
-- 3. SERVICE DELIVERY METRICS (Six Sigma)
-- ================================================
-- Daily operational metrics for process improvement
-- Maps to: service_metrics.csv

SELECT 
    DATE(pd.completed_date) as date,
    AVG(DATEDIFF(pd.kickoff_date, c.signed_date)) as onboarding_time_days,
    COUNT(DISTINCT pd.project_id) as projects_completed,
    SUM(CASE WHEN pd.actual_delivery_date <= pd.target_delivery_date THEN 1 ELSE 0 END) as on_time_deliveries,
    SUM(CASE WHEN qc.defect_found = 1 THEN 1 ELSE 0 END) as defects,
    SUM(qc.rework_hours) as rework_hours,
    AVG(cs.satisfaction_score) as client_satisfaction,
    AVG(ru.utilization_pct) as team_utilization_pct,
    AVG(DATEDIFF(pd.kickoff_date, c.signed_date)) as lead_to_kickoff_days,
    AVG(DATEDIFF(pd.actual_delivery_date, pd.kickoff_date)) as kickoff_to_launch_days
FROM project_deliveries pd
JOIN contracts c ON pd.contract_id = c.contract_id
LEFT JOIN quality_control qc ON pd.project_id = qc.project_id
LEFT JOIN client_satisfaction cs ON pd.project_id = cs.project_id
LEFT JOIN resource_utilization ru ON pd.project_id = ru.project_id
WHERE pd.completed_date >= CURRENT_DATE - INTERVAL 90 DAY
GROUP BY DATE(pd.completed_date)
ORDER BY date DESC;

-- ================================================
-- 4. PROCESS QUALITY METRICS (Six Sigma Control Charts)
-- ================================================
-- Daily process quality indicators
-- Maps to: process_quality.csv

SELECT 
    DATE(pq.measurement_date) as date,
    AVG(pq.requirements_clarity_score) as requirements_clarity,
    AVG(pq.resource_availability_score) as resource_availability,
    AVG(pq.communication_effectiveness_score) as communication_score,
    AVG(pq.technical_execution_score) as technical_quality,
    AVG(pq.process_compliance_pct) as process_compliance_pct,
    SUM(CASE WHEN d.defect_category = 'UNCLEAR_REQUIREMENTS' THEN 1 ELSE 0 END) as defect_unclear_requirements,
    SUM(CASE WHEN d.defect_category = 'RESOURCE_UNAVAILABLE' THEN 1 ELSE 0 END) as defect_resource_unavailable,
    SUM(CASE WHEN d.defect_category = 'SCOPE_CREEP' THEN 1 ELSE 0 END) as defect_scope_creep,
    SUM(CASE WHEN d.defect_category = 'TECHNICAL_ISSUE' THEN 1 ELSE 0 END) as defect_technical,
    SUM(CASE WHEN d.defect_category = 'COMMUNICATION_GAP' THEN 1 ELSE 0 END) as defect_communication,
    COUNT(d.defect_id) as total_defects
FROM process_quality_metrics pq
LEFT JOIN defects d ON DATE(pq.measurement_date) = DATE(d.identified_date)
WHERE pq.measurement_date >= CURRENT_DATE - INTERVAL 90 DAY
GROUP BY DATE(pq.measurement_date)
ORDER BY date DESC;

-- ================================================
-- 5. BUDGET CONSTRAINTS
-- ================================================
-- Current fiscal constraints and policies
-- Maps to: constraints.csv

SELECT 
    'total_budget' as constraint_type,
    total_approved_budget as value,
    'USD' as unit,
    'Total available budget for all service lines' as description
FROM fiscal_year_budgets
WHERE fiscal_year = 2025

UNION ALL

SELECT 
    'max_headcount_growth' as constraint_type,
    max_yoy_headcount_growth_pct as value,
    'Percentage' as unit,
    'Maximum year-over-year headcount growth' as description
FROM hr_policies
WHERE policy_active = 1

UNION ALL

SELECT 
    'min_cash_runway_months' as constraint_type,
    min_required_cash_months as value,
    'Months' as unit,
    'Minimum cash runway to maintain' as description
FROM treasury_policies
WHERE policy_active = 1

UNION ALL

SELECT 
    'max_single_service_allocation' as constraint_type,
    max_department_budget as value,
    'USD' as unit,
    'Maximum budget for any single service line' as description
FROM budget_allocation_policies
WHERE fiscal_year = 2025 AND policy_active = 1

UNION ALL

SELECT 
    'min_roi_threshold' as constraint_type,
    min_acceptable_roi as value,
    'Ratio' as unit,
    'Minimum acceptable ROI for funded projects' as description
FROM investment_policies
WHERE policy_active = 1;

-- ================================================
-- 6. RESOURCE UTILIZATION ANALYSIS
-- ================================================
-- Current team capacity and utilization

SELECT 
    d.department_name as service_line,
    COUNT(DISTINCT e.employee_id) as current_headcount,
    SUM(CASE WHEN e.employment_type = 'CONTRACTOR' THEN 1 ELSE 0 END) as contractor_count,
    AVG(ru.billable_hours / ru.total_hours * 100) as avg_utilization_pct,
    SUM(ru.billable_hours) as total_billable_hours,
    SUM(p.project_revenue) / COUNT(DISTINCT e.employee_id) as revenue_per_employee,
    COUNT(DISTINCT p.project_id) as projects_active,
    COUNT(hr.job_requisition_id) as open_positions
FROM departments d
JOIN employees e ON d.department_id = e.department_id
LEFT JOIN resource_utilization ru ON e.employee_id = ru.employee_id
LEFT JOIN project_assignments pa ON e.employee_id = pa.employee_id
LEFT JOIN projects p ON pa.project_id = p.project_id
LEFT JOIN hr_requisitions hr ON d.department_id = hr.department_id AND hr.status = 'OPEN'
WHERE e.employment_status = 'ACTIVE'
    AND ru.period_month = DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
GROUP BY d.department_name
ORDER BY revenue_per_employee DESC;

-- ================================================
-- 7. PROJECT PIPELINE ANALYSIS
-- ================================================
-- Current sales pipeline for capacity planning

SELECT 
    d.department_name as service_line,
    COUNT(DISTINCT o.opportunity_id) as pipeline_opportunities,
    SUM(o.estimated_value) as pipeline_value,
    AVG(o.win_probability) as avg_win_probability,
    SUM(o.estimated_value * o.win_probability) as weighted_pipeline,
    AVG(DATEDIFF(o.expected_close_date, o.created_date)) as avg_sales_cycle_days,
    COUNT(DISTINCT CASE WHEN o.stage = 'NEGOTIATION' THEN o.opportunity_id END) as late_stage_opps
FROM opportunities o
JOIN departments d ON o.service_department_id = d.department_id
WHERE o.status = 'OPEN'
    AND o.expected_close_date >= CURRENT_DATE
    AND o.expected_close_date <= CURRENT_DATE + INTERVAL 6 MONTH
GROUP BY d.department_name
ORDER BY weighted_pipeline DESC;

-- ================================================
-- 8. COST STRUCTURE ANALYSIS
-- ================================================
-- Breakdown of operating expenses by category

SELECT 
    d.department_name as service_line,
    DATE_FORMAT(gl.transaction_date, '%Y-%m') as month,
    SUM(CASE WHEN gl.account_category = 'PERSONNEL' THEN gl.amount ELSE 0 END) as personnel_cost,
    SUM(CASE WHEN gl.account_category = 'CONTRACTOR' THEN gl.amount ELSE 0 END) as contractor_cost,
    SUM(CASE WHEN gl.account_category = 'MARKETING' THEN gl.amount ELSE 0 END) as marketing_cost,
    SUM(CASE WHEN gl.account_category IN ('SOFTWARE', 'TOOLS', 'INFRASTRUCTURE') THEN gl.amount ELSE 0 END) as technology_cost,
    SUM(CASE WHEN gl.account_category NOT IN ('PERSONNEL', 'CONTRACTOR', 'MARKETING', 'SOFTWARE', 'TOOLS', 'INFRASTRUCTURE') THEN gl.amount ELSE 0 END) as other_opex,
    SUM(gl.amount) as total_opex
FROM general_ledger gl
JOIN departments d ON gl.department_id = d.department_id
WHERE gl.transaction_date >= CURRENT_DATE - INTERVAL 12 MONTH
    AND gl.account_type = 'EXPENSE'
GROUP BY d.department_name, DATE_FORMAT(gl.transaction_date, '%Y-%m')
ORDER BY month DESC, service_line;

-- ================================================
-- 9. CLIENT ACQUISITION ECONOMICS
-- ================================================
-- CAC, LTV, and payback metrics by service line

SELECT 
    d.department_name as service_line,
    COUNT(DISTINCT c.client_id) as new_clients_acquired,
    SUM(me.marketing_spend) / COUNT(DISTINCT c.client_id) as cac,
    AVG(clv.lifetime_value) as avg_ltv,
    AVG(clv.lifetime_value) / (SUM(me.marketing_spend) / COUNT(DISTINCT c.client_id)) as ltv_cac_ratio,
    AVG(cr.annual_contract_value) / (SUM(me.marketing_spend) / COUNT(DISTINCT c.client_id)) * 12 as payback_months,
    AVG(cr.retention_months) as avg_retention_months,
    SUM(cr.total_revenue) as total_revenue_generated
FROM clients c
JOIN departments d ON c.acquisition_department_id = d.department_id
JOIN client_lifetime_value clv ON c.client_id = clv.client_id
JOIN client_revenue cr ON c.client_id = cr.client_id
JOIN marketing_expenses me ON d.department_id = me.department_id 
    AND YEAR(c.acquisition_date) = me.fiscal_year
WHERE c.acquisition_date >= CURRENT_DATE - INTERVAL 12 MONTH
GROUP BY d.department_name
ORDER BY ltv_cac_ratio DESC;

-- ================================================
-- 10. OPTIMIZATION INPUT SUMMARY
-- ================================================
-- Consolidated view for optimization algorithm

SELECT 
    d.department_name as service_line,
    br.fy2025_budget_request as budget_requested,
    br.minimum_viable_budget as min_viable_budget,
    COALESCE(hr.avg_roi_3yr, 2.0) as expected_roi,
    br.strategic_priority_score as strategic_priority,
    br.success_probability,
    hc.current_headcount,
    hc.current_utilization_pct,
    pp.weighted_pipeline_value,
    ca.ltv_cac_ratio,
    sm.avg_client_satisfaction,
    sm.avg_defect_rate
FROM budget_requests br
JOIN departments d ON br.department_id = d.department_id
LEFT JOIN (
    SELECT department_id, AVG(roi) as avg_roi_3yr
    FROM financial_transactions
    WHERE transaction_date >= CURRENT_DATE - INTERVAL 3 YEAR
    GROUP BY department_id
) hr ON d.department_id = hr.department_id
LEFT JOIN (
    SELECT department_id, 
           COUNT(DISTINCT employee_id) as current_headcount,
           AVG(utilization_pct) as current_utilization_pct
    FROM employees e
    JOIN resource_utilization ru ON e.employee_id = ru.employee_id
    WHERE e.employment_status = 'ACTIVE'
    GROUP BY department_id
) hc ON d.department_id = hc.department_id
LEFT JOIN (
    SELECT service_department_id,
           SUM(estimated_value * win_probability) as weighted_pipeline_value
    FROM opportunities
    WHERE status = 'OPEN'
    GROUP BY service_department_id
) pp ON d.department_id = pp.service_department_id
LEFT JOIN (
    SELECT acquisition_department_id,
           AVG(lifetime_value) / NULLIF(AVG(cac), 0) as ltv_cac_ratio
    FROM clients c
    JOIN client_lifetime_value clv ON c.client_id = clv.client_id
    JOIN (
        SELECT department_id, SUM(marketing_spend) / COUNT(DISTINCT client_id) as cac
        FROM marketing_expenses me
        JOIN clients c ON me.department_id = c.acquisition_department_id
        GROUP BY department_id
    ) cac_calc ON c.acquisition_department_id = cac_calc.department_id
    GROUP BY acquisition_department_id
) ca ON d.department_id = ca.acquisition_department_id
LEFT JOIN (
    SELECT department_id,
           AVG(satisfaction_score) as avg_client_satisfaction,
           AVG(defect_rate) as avg_defect_rate
    FROM project_deliveries pd
    JOIN client_satisfaction cs ON pd.project_id = cs.project_id
    JOIN quality_control qc ON pd.project_id = qc.project_id
    GROUP BY department_id
) sm ON d.department_id = sm.department_id
WHERE br.fiscal_year = 2025
    AND br.status = 'SUBMITTED'
ORDER BY br.strategic_priority_score DESC, hr.avg_roi_3yr DESC;
