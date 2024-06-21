"""
Created on Wed Mar 21 17:34:11 2018

Edited by: Group 9 - EPA141A - Indonesian Quartet
@author: ciullo
"""
from ema_workbench import (
    Model,
    CategoricalParameter,
    ArrayOutcome,
    ScalarOutcome,
    IntegerParameter,
    RealParameter,
)
from dike_model_function import DikeNetwork  # @UnresolvedImport

import numpy as np


def sum_over(*args):
    numbers = []
    for entry in args:
        try:
            value = sum(entry)
        except TypeError:
            value = entry
        numbers.append(value)

    return sum(numbers)


def sum_over_time(*args):
    data = np.asarray(args)
    summed = data.sum(axis=0)
    return summed


def get_model_for_problem_formulation(problem_formulation_id):
    """Convenience function to prepare DikeNetwork in a way it can be input in the EMA-workbench.
    Specify uncertainties, levers, and outcomes of interest.

    Parameters
    ----------
    problem_formulation_id : str
                             problem formulations differ with respect to the objectives
                             'Urban Dikes' : Dike Heightening of A3 & A5 (Urban Area) (Death, Damage, and Dike Investment Cost)
                             'All Dikes' : Dike Heightening of all area



    """
    # Load the model:
    function = DikeNetwork()
    # workbench model:
    dike_model = Model("dikesnet", function=function)

    # Uncertainties and Levers:
    # Specify uncertainties range:
    Real_uncert = {"Bmax": [30, 350], "pfail": [0, 1]}  # m and [.]
    # breach growth rate [m/day]
    cat_uncert_loc = {"Brate": (1.0, 1.5, 10)}

    cat_uncert = {
        f"discount rate {n}": (1.5, 2.5, 3.5, 4.5) for n in function.planning_steps
    }

    Int_uncert = {"A.0_ID flood wave shape": [0, 132]}
    # Range of dike heightening:
    dike_lev = {"DikeIncrease": [0, 10]}  # dm

    # Series of five Room for the River projects:
    rfr_lev = [f"{project_id}_RfR" for project_id in range(0, 5)]

    # Time of warning: 0, 1, 2, 3, 4 days ahead from the flood
    EWS_lev = {"EWS_DaysToThreat": [0, 4]}  # days

    uncertainties = []
    levers = []

    for uncert_name in cat_uncert.keys():
        categories = cat_uncert[uncert_name]
        uncertainties.append(CategoricalParameter(uncert_name, categories))

    for uncert_name in Int_uncert.keys():
        uncertainties.append(
            IntegerParameter(
                uncert_name, Int_uncert[uncert_name][0], Int_uncert[uncert_name][1]
            )
        )

    # RfR levers can be either 0 (not implemented) or 1 (implemented)
    for lev_name in rfr_lev:
        for n in function.planning_steps:
            lev_name_ = f"{lev_name} {n}"
            levers.append(IntegerParameter(lev_name_, 0, 1))

    # Early Warning System lever
    for lev_name in EWS_lev.keys():
        levers.append(
            IntegerParameter(lev_name, EWS_lev[lev_name][0], EWS_lev[lev_name][1])
        )

    for dike in function.dikelist:
        # uncertainties in the form: locationName_uncertaintyName
        for uncert_name in Real_uncert.keys():
            name = f"{dike}_{uncert_name}"
            lower, upper = Real_uncert[uncert_name]
            uncertainties.append(RealParameter(name, lower, upper))

        for uncert_name in cat_uncert_loc.keys():
            name = f"{dike}_{uncert_name}"
            categories = cat_uncert_loc[uncert_name]
            uncertainties.append(CategoricalParameter(name, categories))

        # location-related levers in the form: locationName_leversName
        for lev_name in dike_lev.keys():
            for n in function.planning_steps:
                name = f"{dike}_{lev_name} {n}"
                levers.append(
                    IntegerParameter(name, dike_lev[lev_name][0], dike_lev[lev_name][1])
                )

    # load uncertainties and levers in dike_model:
    dike_model.uncertainties = uncertainties
    dike_model.levers = levers

    # Problem formulations:
    # Outcomes are all costs, thus they have to minimized:
    direction = ScalarOutcome.MINIMIZE



    # Urban PF:
    if problem_formulation_id == 'Urban Dikes':

        outcomes = []

        # A3 and A5 Deaths and Damages
        for dike in function.dikelist:
            for entry in [
                "Expected Annual Damage",
                "Expected Number of Deaths",
                "Dike Investment Costs",
            ]:
                outcome_name = ''.join(dike.split('.'))
                outcome_name += '' + ''.join(entry.split(' '))
                if dike == "A.3" or dike == "A.5":
                    outcomes.append(
                        ScalarOutcome(
                            outcome_name,
                            variable_name=f"{dike}_{entry}",
                            function=sum_over,
                            kind=direction,
                        )
                    )

        total_dike_investment = []
        total_dike_investment.extend(
            [f"{dike}_Dike Investment Costs" for dike in function.dikelist]
        )


        total_damage_variables = []
        total_damage_variables.extend(
            [f"{dike}_Expected Annual Damage" for dike in function.dikelist]
        )

        total_casualty_variables = []
        total_casualty_variables.extend(
            [f"{dike}_Expected Number of Deaths" for dike in function.dikelist]
        )

# Aggregated Investment, Damage, and Death
        outcomes.append(
            ScalarOutcome(
                "Total_Dike_Investment",
                variable_name=[var for var in total_dike_investment],
                function=sum_over,
                kind=direction,
            )
        )

        outcomes.append(
            ScalarOutcome(
                "Total_Expected_Annual_Damage",
                variable_name=[var for var in total_damage_variables],
                function=sum_over,
                kind=direction,
            )
        )
        outcomes.append(
            ScalarOutcome(
                "Total_Expected_Number_of_Deaths",
                variable_name=[var for var in total_casualty_variables],
                function=sum_over,
                kind=direction,
            )
        )

        dike_model.outcomes=outcomes

    elif problem_formulation_id == 'All Dikes':
        outcomes = []

        # All Dike Ring Deaths and Damages
        for dike in function.dikelist:
            for entry in [
                "Expected Annual Damage",
                "Dike Investment Costs",
                "Expected Number of Deaths",
            ]:
                outcome_name = ''.join(dike.split('.'))
                outcome_name += '_' + '_'.join(entry.split(' '))


                outcomes.append(
                    ScalarOutcome(
                        outcome_name,
                        variable_name=f"{dike}_{entry}",
                        function=sum_over,
                        kind= direction,
                    )
                )

        # Aggregated Costs
        outcomes.append(
            ScalarOutcome(
                "RfR Total Costs",
                variable_name="RfR Total Costs",
                function=sum_over,
                kind=direction,
            )
        )

        # Aggregated Cost and Damages (for convenience)
        total_damage_variables = []
        total_damage_variables.extend(
            [f"{dike}_Expected Annual Damage" for dike in function.dikelist]
        )

        total_dike_investment_variables = []
        total_dike_investment_variables.extend(
            [f"{dike}_Dike Investment Costs" for dike in function.dikelist]
        )

        total_casualty_variables = []
        total_casualty_variables.extend(
            [f"{dike}_Expected Number of Deaths" for dike in function.dikelist]
        )

        outcomes.append(
            ScalarOutcome(
                "Total_Expected_Annual_Damage",
                variable_name=[var for var in total_damage_variables],
                function=sum_over,
                kind=direction,
            )
        )
        outcomes.append(
            ScalarOutcome(
                "Total_Dike_Investment_Costs",
                variable_name=[var for var in total_dike_investment_variables],
                function=sum_over,
                kind=direction,
            )
        )
        outcomes.append(
            ScalarOutcome(
                "Total_Expected_Number_of_Deaths",
                variable_name=[var for var in total_casualty_variables],
                function=sum_over,
                kind=direction,
            )
        )
        dike_model.outcomes = outcomes
    else:
        raise TypeError("unknown identifier")

    return dike_model, function.planning_steps


if __name__ == "__main__":
    get_model_for_problem_formulation('All Dikes')
