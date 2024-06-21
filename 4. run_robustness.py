import argparse
import pandas as pd
from ema_workbench import (
    Policy,
    Scenario,
    ema_logging,
    MultiprocessingEvaluator,
    save_results,
)
from problem_formulation import get_model_for_problem_formulation

ema_logging.log_to_stderr(ema_logging.INFO)


def run_experiments(mode, num_scenarios):
    scenarios = None
    N_scenarios = num_scenarios

    # Set parameters for experiments based on program mode
    if mode == 'base_case':
        dike_model, planning_steps = get_model_for_problem_formulation(6)

        # "Do Nothing" case
        policies = []
        policies.append(Policy("Base Case", **{L.name: 0 for L in dike_model.levers}, ))

        # 5000 scenarios: limited by compute time
        if N_scenarios == 0:
            N_scenarios = 5000

    elif mode == 'robustness':
        dike_model, planning_steps = get_model_for_problem_formulation(6)

        # 50 policies from file
        policies_df = pd.read_csv('./output/policies__constraints_filtered__diverse_set_50.csv',
                                  index_col='Policy Name')
        policies_df = policies_df[[L.name for L in dike_model.levers]]

        policies = []
        for name, policy in policies_df.iterrows():
            policies.append(Policy(str(name), **policy.to_dict()))

        # 1000 scenarios: limited by compute time x 50 policies
        if N_scenarios == 0:
            N_scenarios = 1000

    elif mode == 'vulnerability':
        dike_model, planning_steps = get_model_for_problem_formulation(6)

        # ~3-7 policies from final Robustness analysis
        policies_df = pd.read_csv('./output/policies__final_set.csv',
                                  index_col='Policy Name')
        policies_df = policies_df[[L.name for L in dike_model.levers]]

        policies = []
        for name, policy in policies_df.iterrows():
            policies.append(Policy(str(name), **policy.to_dict()))

        # PRIM-box scenarios from original DFE
        scenarios_fn = 'base_case_results__5000_scenarios__prim_filtered.csv'
        scenarios_df = pd.read_csv(f'./output/{scenarios_fn}')
        scenarios_df = scenarios_df[[U.name for U in dike_model.uncertainties]]

        scenarios = []
        for name, scenario in scenarios_df.iterrows():
            scenarios.append(Scenario(str(name), **scenario.to_dict()))

    # Perform actual experiment run using the EMA workbench
    if scenarios is not None:
        with MultiprocessingEvaluator(dike_model) as evaluator:
            results = evaluator.perform_experiments(scenarios, policies)
        N_scenarios = len(scenarios)
    else:
        with MultiprocessingEvaluator(dike_model) as evaluator:
            results = evaluator.perform_experiments(N_scenarios, policies)

    # Save results to an output file based on mode
    filename = './output/robustness.tar.gz' if mode == 'robustness' else f'./output/{mode}_results__{N_scenarios}_scenarios.tar.gz'

    save_results(results, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='run_experiments',
        description='Performs IJssel River water basin model runs'
    )
    parser.add_argument('--mode', '-M',
                        default='base_case',
                        required=False)
    parser.add_argument('--num_scenarios', '-N',
                        type=int,
                        default=0,
                        required=False)
    args = parser.parse_args()

    run_experiments(args.mode, args.num_scenarios)
