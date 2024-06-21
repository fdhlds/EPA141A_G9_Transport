# Dike Heightening for IJssel River Flood Risk Management
## Model-Based Decision Making

Prepared for EPA141A by Group 9 [**Transport Company**].

| Team Member            | Student Number |
| ---------------------- | -------------- |
| Aryasatya Adyatama     | 5844924        |
| Fadhila Dewi Susetya   | 5992125        |
| Hidayahtullah Abdi Robhani | 6075894      |
| Prima Sandy Yonanda    | 5916976        |

## Table of Contents
- [Dike Heightening for IJssel River Flood Risk Management](#dike-heightening-for-ijssel-river-flood-risk-management)
  - [Model-Based Decision Making](#model-based-decision-making)
  - [Table of Contents](#table-of-contents)
  - [File Structure](#file-structure)
    - [Directories](#directories)
    - [Model Files](#model-files)
    - [Experimentation & Analysis Files (& Usage)](#experimentation--analysis-files--usage)
    - [Other Files](#other-files)
  - [Modeling Approach](#modeling-approach)
    - [Step 1: Run Initial Experiments with the "Base Case" Policy](#step-1-run-initial-experiments-with-the-base-case-policy)
    - [Step 2: Open Exploration: Uncertainty Analysis](#step-2-open-exploration-uncertainty-analysis)
    - [Step 3: Open Exploration: Scenario Discovery & Selection](#step-3-open-exploration-scenario-discovery--selection)
        - [Step 3a: Scenario Discovery](#step-3a-scenario-discovery)
        - [Step 3b: Scenario Selection](#step-3b-scenario-selection)
    - [Step 4: Multi-Scenario, Multi-Objective Robust Policy Search](#step-4-multi-scenario-multi-objective-robust-policy-search)
        - [Step 4a: Generative Algorithm Policy Search](#step-4a-generative-algorithm-policy-search)
        - [Step 4b: Convergence Testing & Initial Policy Filtering](#step-4b-convergence-testing--initial-policy-filtering)
        - [Step 4c: Robustness Testing](#step-4c-robustness-testing)
        - [Step 4d: Vulnerability Testing](#step-4d-vulnerability-testing)

## File Structure

### Directories
* `archives/` - Contains historical run data from the optimization process for reference and validation of convergence.
* `data/` - Unmodified folder containing data used by the base model.
* `output/` - Includes all output files from our analysis, such as CSVs or compressed files of results.
* `img/` - Contains plots and diagrams generated during analysis.
* `report/` - Contains the technical report in PDF format.

### Report Files
* [Technical Report](./report/Group9_Transport_Company_Technical_Report.pdf)
* [Political Reflection](./report/Group9_Transport_Company_Political_Reflection.pdf)

### Model Files
* Base model and interface files for the IJssel River, with specific modifications detailed in [problem_formulation.py](problem_formulation.py) for enhanced compatibility and functionality with the EMA workbench.

### Experimentation & Analysis Files (& Usage)
* Detailed descriptions and usage instructions for each file involved in the modeling approach are provided, focusing on replicating our results and understanding the impact of different policies under uncertainty.

### Other Files
* `README.md` - You are currently reading this file.

## Modeling Approach
Our modeling approach involves several stages of data processing, analysis, and optimization, structured to facilitate a deep understanding of the IJssel River Dike Heightening Project:

![MORDM Approach](./img/MORDM_image.png)  <!-- Insert your image here -->

The framework used in this analysis consists of four main steps:

**Problem Formulation**

The framework begins with problem formulation, where decision makers outline uncertainties, levers, relationships, and measures (XLRM) crucial for system performance improvement. Uncertainties are especially important in environmental planning. Initial exploratory analysis, including Sobol sensitivity assessment, Feature Scoring, and Dimensional Stacking, identifies key variables, aligning with the Transport Company's goals for the IJssel River.

**Generating Alternatives**

Next, decision makers employ multi-objective problem formulations to understand tradeoffs between performance measures. Multi-objective evolutionary algorithms (MOEAs) facilitate finding diverse solutions covering all relevant tradeoffs. Ensuring convergence to optimal solutions and maintaining diversity across scenarios, especially using the epsilon-NSGA II algorithm, helps in prioritizing scenarios that meet specific goals.

**Uncertainty Analysis**

Robustness metrics such as Signal-to-noise (SNR) ratio and Maximum Regret are used to assess how uncertainties affect candidate solutions. Constraints focusing on urban damage and fatalities streamline scenario complexity, striking a balance between comprehensive uncertainty exploration and computational efficiency.

**Scenario Discovery and Tradeoff Analysis**

Scenario discovery identifies vulnerabilities and evaluates decision levers based on predefined objectives. Systematic scenario analysis reveals how uncertainties impact outcomes, ensuring insights into when policies may fall short of desired goals. PRIM plays a critical role in scenario discovery, highlighting factors influencing policy performance and supporting robust decision-making.


For a detailed technical explanation, please refer to the [technical report](./report/Group9_Transport_Company_Technical_Report.pdf).

### Step 1: Run Initial Experiments with the "Base Case" Policy
- **File:** [1. Base_case.ipynb](1.%20Base_case.ipynb)
- **Purpose:** Generates baseline scenario results for comparison against policy interventions.
- **Output:** `.tar.gz` file containing scenario results, stored in `output/`.
- **Instructions:** Run the script with specified modes and scenarios.

### Step 2: Open Exploration: Uncertainty Analysis
- **Files:** [2.a. Global Sensitivity Analysis.ipynb](2.a.%20Global%20Sensitivity%20Analysis.ipynb), [2.b. Feature Scoring & Dimensional Stacking.ipynb](2.b.%20Feature%20Scoring%20&%20Dimensional%20Stacking.ipynb)
- **Purpose:** Identifies key uncertainties and their impacts on outcomes.
- **Output:** Plots and heatmaps detailing sensitivity and uncertainty impacts.
- **Instructions:** Execute Jupyter Notebooks to visualize uncertainty analysis results.

### Step 3: Open Exploration: Scenario Discovery & Selection
- **Step 3a: Scenario Discovery**
  - **File:** [3.a. Scenario_Discovery.ipynb](3.a.%20Scenario_Discovery.ipynb)
  - **Purpose:** Discovers critical scenarios leading to significant impacts.
  - **Output:** Graphs and a filtered CSV of critical scenarios.
  - **Instructions:** Review and run the notebook to filter scenarios.
- **Step 3b: Scenario Selection**
  - **File:** [3.b. scenario_diversity_evaluation.py](3.b.%20scenario_diversity_evaluation.py)
  - **Purpose:** Selects a diverse set of scenarios for robust testing.
  - **Output:** `selected_scenarios.csv` with the chosen scenarios.
  - **Instructions:** Run the script to generate and score scenario diversity.

### Step 4: Multi-Scenario, Multi-Objective Robust Policy Search
- **Step 4a: Generative Algorithm Policy Search**
  - **File:** [4.a. seeded_scenario_optimization.py](4.a.%20seeded_scenario_optimization.py)
  - **Purpose:** Optimizes policies to maximize performance across selected scenarios.
  - **Output:** CSV files detailing policy results and convergence metrics.
  - **Instructions:** Execute the script for each selected scenario with different seeds.
- **Step 4b: Convergence Testing & Initial Policy Filtering**
  - **File:** [4.b. Directed Search.ipynb](4.b.%20Directed%20Search.ipynb)
  - **Purpose:** Assesses and refines policy options based on convergence and constraints.
  - **Output:** Filtered and diversified policy sets.
  - **Instructions:** Analyze convergence and filter policies via the notebook.
- **Step 4c: Robustness Testing**
  - **Files:** [4. run_robustness.py](4.%20run_robustness.py), [4.c. Policy Robustness.ipynb](4.c.%20Policy%20Robustness.ipynb)
  - **Purpose:** Tests the robustness of filtered policies under various scenarios.
  - **Output:** Robustness metrics and comparative graphs.
  - **Instructions:** Run robustness scenarios and analyze policy performance.
- **Step 4d: Vulnerability Testing**
  - **Files:** [4. run_robustness.py](4.%20run_robustness.py), [4.d. Policy Vulnerability.ipynb](4.d.%20Policy%20Vulnerability.ipynb)
  - **Purpose:** Evaluates policy performance under the most challenging scenarios.
  - **Output:** Insights into policy vulnerabilities and recommendations.
  - **Instructions:** Conduct vulnerability testing and explore results.
