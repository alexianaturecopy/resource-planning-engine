"""
Budget Optimization Module using Linear Programming
Constraint-based resource allocation optimizer

Uses PuLP library for linear programming optimization.
Maximizes expected ROI subject to budget, headcount, and strategic constraints.

Author: Ye(Alexia) Quan
"""

from pulp import *
import pandas as pd
import numpy as np

def optimize_budget_allocation(
    resource_requests,
    total_budget,
    constraints=None
):
    """
    Optimize budget allocation across service lines using linear programming.
    
    Objective: Maximize total expected ROI
    
    Constraints:
    - Total allocated budget ≤ available budget
    - Each allocation ≥ minimum viable budget
    - Each allocation ≤ requested budget
    - Optional: max allocation per service line
    - Optional: min number of funded projects
    - Optional: strategic priority weighting
    
    Args:
        resource_requests (DataFrame): Contains service_line, budget_requested, 
                                       min_viable_budget, expected_roi, strategic_priority
        total_budget (float): Total available budget
        constraints (dict): Additional constraints
    
    Returns:
        dict: Optimization results including allocations and metrics
    """
    
    # Initialize the optimization problem
    prob = LpProblem("Budget_Allocation_Optimization", LpMaximize)
    
    # Decision variables: allocation amount for each service line
    service_lines = resource_requests['service_line'].tolist()
    
    # Create decision variables (how much to allocate to each service line)
    allocations = LpVariable.dicts(
        "allocation",
        service_lines,
        lowBound=0,
        cat='Continuous'
    )
    
    # Binary variables: whether to fund each service line (0 or 1)
    funded = LpVariable.dicts(
        "funded",
        service_lines,
        cat='Binary'
    )
    
    # Objective function: Maximize weighted ROI
    # ROI = (allocation * expected_roi * strategic_priority)
    objective = lpSum([
        allocations[sl] * 
        float(resource_requests[resource_requests['service_line'] == sl]['expected_roi'].values[0]) *
        float(resource_requests[resource_requests['service_line'] == sl]['strategic_priority'].values[0])
        for sl in service_lines
    ])
    
    prob += objective, "Total_Weighted_ROI"
    
    # Constraint 1: Total allocation cannot exceed available budget
    prob += lpSum([allocations[sl] for sl in service_lines]) <= total_budget, "Total_Budget_Constraint"
    
    # Constraint 2: If funded, allocation must be at least minimum viable budget
    for sl in service_lines:
        min_budget = float(resource_requests[resource_requests['service_line'] == sl]['min_viable_budget'].values[0])
        max_budget = float(resource_requests[resource_requests['service_line'] == sl]['budget_requested'].values[0])
        
        # If funded, allocation >= min_viable_budget
        prob += allocations[sl] >= min_budget * funded[sl], f"Min_Budget_{sl}"
        
        # Allocation cannot exceed requested amount
        prob += allocations[sl] <= max_budget * funded[sl], f"Max_Budget_{sl}"
    
    # Optional Constraint 3: Minimum number of funded projects
    if constraints and 'min_funded_projects' in constraints:
        min_projects = constraints['min_funded_projects']
        prob += lpSum([funded[sl] for sl in service_lines]) >= min_projects, "Min_Funded_Projects"
    
    # Optional Constraint 4: Maximum allocation per service line
    if constraints and 'max_per_service' in constraints:
        max_per_service = constraints['max_per_service']
        for sl in service_lines:
            prob += allocations[sl] <= max_per_service, f"Max_Per_Service_{sl}"
    
    # Optional Constraint 5: Strategic priority threshold
    # High priority projects (priority >= 4) should be funded if possible
    if constraints and 'prioritize_high_priority' in constraints:
        if constraints['prioritize_high_priority']:
            high_priority = resource_requests[resource_requests['strategic_priority'] >= 4]['service_line'].tolist()
            for sl in high_priority:
                # Encourage funding of high priority projects by setting minimum allocation
                prob += allocations[sl] >= 0, f"High_Priority_{sl}"
    
    # Solve the optimization problem
    prob.solve(PULP_CBC_CMD(msg=0))
    
    # Extract results
    results = {
        'status': LpStatus[prob.status],
        'total_allocated': sum([allocations[sl].varValue for sl in service_lines if allocations[sl].varValue]),
        'allocations': {},
        'funded_projects': [],
        'unfunded_projects': [],
        'objective_value': value(prob.objective),
        'budget_utilization': 0
    }
    
    for sl in service_lines:
        allocation = allocations[sl].varValue if allocations[sl].varValue else 0
        is_funded = funded[sl].varValue == 1 if funded[sl].varValue else False
        
        results['allocations'][sl] = {
            'allocated': allocation,
            'funded': is_funded,
            'requested': float(resource_requests[resource_requests['service_line'] == sl]['budget_requested'].values[0]),
            'expected_roi': float(resource_requests[resource_requests['service_line'] == sl]['expected_roi'].values[0]),
            'strategic_priority': float(resource_requests[resource_requests['service_line'] == sl]['strategic_priority'].values[0])
        }
        
        if is_funded:
            results['funded_projects'].append(sl)
        else:
            results['unfunded_projects'].append(sl)
    
    results['budget_utilization'] = (results['total_allocated'] / total_budget) * 100
    
    # Calculate expected returns
    total_expected_return = sum([
        results['allocations'][sl]['allocated'] * results['allocations'][sl]['expected_roi']
        for sl in service_lines
    ])
    
    results['total_expected_return'] = total_expected_return
    results['blended_roi'] = total_expected_return / results['total_allocated'] if results['total_allocated'] > 0 else 0
    
    return results

def optimize_with_scenarios(resource_requests, scenarios):
    """
    Run optimization across multiple budget scenarios
    
    Args:
        resource_requests (DataFrame): Resource request data
        scenarios (dict): Dict of scenario_name: budget_amount
    
    Returns:
        dict: Results for each scenario
    """
    results = {}
    
    for scenario_name, budget in scenarios.items():
        results[scenario_name] = optimize_budget_allocation(
            resource_requests,
            budget
        )
    
    return results

def sensitivity_analysis(resource_requests, base_budget, sensitivity_range=0.2, steps=10):
    """
    Perform sensitivity analysis on budget allocation
    
    Args:
        resource_requests (DataFrame): Resource request data
        base_budget (float): Base budget amount
        sensitivity_range (float): +/- range to test (default 20%)
        steps (int): Number of steps to test
    
    Returns:
        DataFrame: Sensitivity analysis results
    """
    
    budgets = np.linspace(
        base_budget * (1 - sensitivity_range),
        base_budget * (1 + sensitivity_range),
        steps
    )
    
    results = []
    
    for budget in budgets:
        opt_result = optimize_budget_allocation(resource_requests, budget)
        
        results.append({
            'budget': budget,
            'budget_pct_change': ((budget - base_budget) / base_budget) * 100,
            'total_allocated': opt_result['total_allocated'],
            'projects_funded': len(opt_result['funded_projects']),
            'expected_return': opt_result['total_expected_return'],
            'blended_roi': opt_result['blended_roi']
        })
    
    return pd.DataFrame(results)

def compare_allocation_strategies(resource_requests, total_budget):
    """
    Compare different allocation strategies
    
    Strategies:
    1. Optimize for ROI (base optimization)
    2. Equal distribution
    3. Priority-based (allocate to highest priority first)
    4. Proportional to request
    
    Args:
        resource_requests (DataFrame): Resource request data
        total_budget (float): Total available budget
    
    Returns:
        dict: Comparison of strategies
    """
    
    strategies = {}
    
    # Strategy 1: Optimized (ROI-weighted)
    strategies['Optimized'] = optimize_budget_allocation(resource_requests, total_budget)
    
    # Strategy 2: Equal distribution
    equal_amount = total_budget / len(resource_requests)
    strategies['Equal'] = {
        'allocations': {},
        'total_allocated': total_budget,
        'blended_roi': 0
    }
    
    for _, row in resource_requests.iterrows():
        sl = row['service_line']
        allocation = min(equal_amount, row['budget_requested'])
        strategies['Equal']['allocations'][sl] = {
            'allocated': allocation,
            'expected_roi': row['expected_roi']
        }
    
    equal_return = sum([v['allocated'] * v['expected_roi'] for v in strategies['Equal']['allocations'].values()])
    strategies['Equal']['total_expected_return'] = equal_return
    strategies['Equal']['blended_roi'] = equal_return / total_budget
    
    # Strategy 3: Priority-based
    priority_sorted = resource_requests.sort_values('strategic_priority', ascending=False).copy()
    strategies['Priority'] = {
        'allocations': {},
        'total_allocated': 0,
        'blended_roi': 0
    }
    
    remaining = total_budget
    for _, row in priority_sorted.iterrows():
        sl = row['service_line']
        if remaining >= row['min_viable_budget']:
            allocation = min(row['budget_requested'], remaining)
            strategies['Priority']['allocations'][sl] = {
                'allocated': allocation,
                'expected_roi': row['expected_roi']
            }
            strategies['Priority']['total_allocated'] += allocation
            remaining -= allocation
        else:
            strategies['Priority']['allocations'][sl] = {
                'allocated': 0,
                'expected_roi': row['expected_roi']
            }
    
    priority_return = sum([v['allocated'] * v['expected_roi'] for v in strategies['Priority']['allocations'].values()])
    strategies['Priority']['total_expected_return'] = priority_return
    strategies['Priority']['blended_roi'] = priority_return / strategies['Priority']['total_allocated'] if strategies['Priority']['total_allocated'] > 0 else 0
    
    # Strategy 4: Proportional to request
    total_requested = resource_requests['budget_requested'].sum()
    strategies['Proportional'] = {
        'allocations': {},
        'total_allocated': total_budget,
        'blended_roi': 0
    }
    
    for _, row in resource_requests.iterrows():
        sl = row['service_line']
        proportion = row['budget_requested'] / total_requested
        allocation = total_budget * proportion
        allocation = min(allocation, row['budget_requested'])
        
        strategies['Proportional']['allocations'][sl] = {
            'allocated': allocation,
            'expected_roi': row['expected_roi']
        }
    
    prop_return = sum([v['allocated'] * v['expected_roi'] for v in strategies['Proportional']['allocations'].values()])
    strategies['Proportional']['total_expected_return'] = prop_return
    strategies['Proportional']['blended_roi'] = prop_return / total_budget
    
    return strategies
