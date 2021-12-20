#!/usr/bin/env python3
import functools
from typing import List
import cvxpy


def cond_utilitarian_budget(total: float, subject: List[str], pref: List[List[str]]):
    """
    This method will calculate a conditional utilitarian budget
    total - total budget
    subject - list of subject to be funded
    pref - list of lists that represents the preferences of each participant
    """
    # number of subjects
    m = len(subject)
    # number of participants
    n = len(pref)
    util = []
    contributions = []
    allocations = cvxpy.Variable(m)

    print(f"Total budget: {total}\n")
    for participant in pref:
        u = 0
        for p in participant:
            u += allocations[subject.index(p)]
        util.append(u)

    for i in range(n):
        contributions.append(total / n)

    sum_logs = cvxpy.sum([cvxpy.log(u) for u in util])
    # any budget must be non-negative
    constraint1 = [v >= 0 for v in allocations]
    # the sum of all budget allocation must be equal to donation each participant make (the total budget)
    constraint2 = [cvxpy.sum(allocations) == sum(contributions)]
    # find optimal values for the maximal sum of the logs
    problem = cvxpy.Problem(
        cvxpy.Maximize(sum_logs), constraints=constraint1 + constraint2
    )
    problem.solve()

    # How the budget will be divided
    budget = "Budget divided as: \n"
    for sub, funds in enumerate(allocations):
        budget += f"\t{subject[sub]} = {funds.value}\n"
    print(budget)

    # the "תועלת" of each participant
    utility_vals = [u.value for u in util]

    toelet = "Utility value for participants:\n"
    for participant, u in enumerate(utility_vals):
        toelet += f"\tParticipant {participant} : {u}\n"

    print(toelet)
    # How much each participant will give for what cause
    print("How much will each participant give for each subject?")
    for i in range(n):
        for j in range(m):
            if subject[j] in pref[i]:
                contribution = allocations[j].value * contributions[i] / util[i].value
                if contribution > 0.001:
                    print(f"\tCitizen {i} gives {contribution} to {subject[j]}")


if __name__ == "__main__":
    # using a scenario explained in class
    total = 6000
    subjects = ["Basketball", "Chess", "Library"]
    util = [["Basketball", "Chess"], ["Chess", "Library"]]
    cond_utilitarian_budget(total, subjects, util)
