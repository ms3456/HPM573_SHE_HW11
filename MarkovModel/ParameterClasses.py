from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import InputData as Data
import scr.MarkovClasses as MarkovCls
import scr.RandomVariantGenerators as Random
import scr.FittingProbDist_MM as Est


class HealthStats(Enum):
    """ health states of patients with HIV """
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    DEATH = 3
    BACKGROUND_DEATH = 4

class Therapies(Enum):
    """ mono vs. combination therapy """
    NONE = 0
    ANTICOAG = 1


class ParametersFixed():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        self._adjDiscountRate = Data.DISCOUNT * Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.WELL

        # annual treatment cost
        if self._therapy == Therapies.NONE:
            self._annualTreatmentCost = 0
        if self._therapy == Therapies.ANTICOAG:
            self._annualTreatmentCost = 0

        # transition probability matrix of the selected therapy
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0


        if self._therapy == Therapies.NONE:
            self._annualStateCosts = Data.HEALTH_COST
        else:
            self._annualStateCosts = Data.ANTICOAG_COST

        #self._annualStateCosts = Data.HEALTH_COST

        self._annualStateUtilities = Data.HEALTH_UTILITY

        self._prob_matrix=[]

        if therapy==Therapies.NONE:
            self._prob_matrix[:], p=MarkovCls.continuous_to_discrete(Data.RATE_MATRIX_NONE,Data.DELTA_T)
        else:
            self._prob_matrix[:],p=MarkovCls.continuous_to_discrete(Data.RATE_MATRIX_ANTI, Data.DELTA_T)

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self, state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost



