from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Define the simulation state with 21 variables (all default to 50)
simulation_state = {
    "morale": 50,
    "productivity": 50,
    "communication": 50,
    "trust": 50,
    "engagement": 50,
    "collaboration": 50,
    "innovation": 50,
    "leadership_effectiveness": 50,
    "employee_satisfaction": 50,
    "conflict_resolution": 50,
    "work_life_balance": 50,
    "resilience": 50,
    "organizational_learning": 50,
    "adaptability": 50,
    "diversity_inclusion": 50,
    "change_readiness": 50,
    "resource_allocation": 50,
    "employee_turnover": 50,
    "absenteeism": 50,
    "stress_levels": 50,
    "customer_satisfaction": 50
}

def update_simulation():
    # 1. Trust: influenced by Communication (60%) and Leadership Effectiveness (40%)
    simulation_state["trust"] = min(simulation_state["communication"] * 0.6 +
                                      simulation_state["leadership_effectiveness"] * 0.4, 100)
    
    # 2. Conflict Resolution: influenced equally by Leadership Effectiveness and Trust.
    simulation_state["conflict_resolution"] = min(
        simulation_state["leadership_effectiveness"] * 0.5 + simulation_state["trust"] * 0.5, 100)
    
    # 3. Stress Levels: lower when Work–Life Balance and Conflict Resolution are high.
    stress = 100 - (simulation_state["work_life_balance"] * 0.5 + simulation_state["conflict_resolution"] * 0.5)
    simulation_state["stress_levels"] = max(0, stress)
    
    # 4. Employee Satisfaction: boosted by Leadership, Work–Life Balance, and low Stress Levels.
    simulation_state["employee_satisfaction"] = min(
        simulation_state["leadership_effectiveness"] * 0.3 +
        simulation_state["work_life_balance"] * 0.4 +
        (100 - simulation_state["stress_levels"]) * 0.3, 100)
    
    # 5. Morale: influenced by Trust, Employee Satisfaction, plus smaller contributions from Conflict Resolution and Work–Life Balance.
    simulation_state["morale"] = min(
        simulation_state["trust"] * 0.3 +
        simulation_state["employee_satisfaction"] * 0.4 +
        simulation_state["conflict_resolution"] * 0.1 +
        simulation_state["work_life_balance"] * 0.2, 100)
    
    # 6. Engagement: influenced equally by Employee Satisfaction and Leadership Effectiveness.
    simulation_state["engagement"] = min(
        simulation_state["employee_satisfaction"] * 0.5 +
        simulation_state["leadership_effectiveness"] * 0.5, 100)
    
    # 7. Collaboration: influenced by Communication, Trust, and Diversity & Inclusion.
    simulation_state["collaboration"] = min(
        simulation_state["communication"] * 0.4 +
        simulation_state["trust"] * 0.4 +
        simulation_state["diversity_inclusion"] * 0.2, 100)
    
    # 8. Innovation: driven equally by Organizational Learning and Adaptability.
    simulation_state["innovation"] = min(
        simulation_state["organizational_learning"] * 0.5 +
        simulation_state["adaptability"] * 0.5, 100)
    
    # 9. Resilience: built from Organizational Learning and Employee Satisfaction.
    simulation_state["resilience"] = min(
        simulation_state["organizational_learning"] * 0.5 +
        simulation_state["employee_satisfaction"] * 0.5, 100)
    
    # 10. Adaptability: influenced by Change Readiness (60%) and Resilience (40%).
    simulation_state["adaptability"] = min(
        simulation_state["change_readiness"] * 0.6 +
        simulation_state["resilience"] * 0.4, 100)
    
    # 11. Organizational Learning: driven by Innovation (40%) and Adaptability (60%).
    simulation_state["organizational_learning"] = min(
        simulation_state["innovation"] * 0.4 +
        simulation_state["adaptability"] * 0.6, 100)
    
    # 12. Employee Turnover: inversely related to Employee Satisfaction.
    simulation_state["employee_turnover"] = max(0, 100 - simulation_state["employee_satisfaction"])
    
    # 13. Absenteeism: inversely related to Engagement.
    simulation_state["absenteeism"] = max(0, 100 - simulation_state["engagement"])
    
    # 14. Customer Satisfaction: based on Productivity, Employee Satisfaction, and Innovation.
    simulation_state["customer_satisfaction"] = min(
        simulation_state["productivity"] * 0.4 +
        simulation_state["employee_satisfaction"] * 0.3 +
        simulation_state["innovation"] * 0.3, 100)
    
    # 15. Productivity: built from Morale, Engagement, Collaboration, and Resource Allocation,
    #      but reduced by Employee Turnover and Absenteeism.
    simulation_state["productivity"] = min(
        simulation_state["morale"] * 0.3 +
        simulation_state["engagement"] * 0.2 +
        simulation_state["collaboration"] * 0.2 +
        simulation_state["resource_allocation"] * 0.2 -
        (simulation_state["employee_turnover"] * 0.05) -
        (simulation_state["absenteeism"] * 0.05), 100)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/state')
def state():
    update_simulation()
    return jsonify(simulation_state)

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    variable = data.get("variable")
    value = data.get("value")
    # Define base variables that can be directly updated by the user.
    base_vars = [
        "leadership_effectiveness",
        "communication",
        "work_life_balance",
        "resource_allocation",
        "change_readiness",
        "diversity_inclusion"
    ]
    if variable == "reset":
        # Reset all variables to 50.
        for key in simulation_state.keys():
            simulation_state[key] = 50
    elif variable in base_vars:
        simulation_state[variable] = value
    # Derived variables remain computed.
    update_simulation()
    return jsonify(simulation_state)

if __name__ == '__main__':
    app.run(debug=True)
