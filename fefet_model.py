import math
import numpy as np
import scipy
import scipy.constants
import random

class FeFET:
    """Represents a FeFET. Can get pulses and read out states"""
    def __init__(self, name: str, homog: bool=False) -> None:
        """Sample number of positive and negative nucleation sites"""
        self.pos_nuc_count = self.sample_pos_nuc_count()
        self.neg_nuc_count = self.sample_neg_nuc_count()

        """Create the positive and negative nucleation sites"""
        self.pos_nuc_sites = self.sample_pos_sites(self.pos_nuc_count, homog)
        self.neg_nuc_sites = self.sample_neg_sites(self.neg_nuc_count, homog)

        """Sample max nucleation rate (lambda_0)"""
        self.lam_not = self.sample_lam_not()

        """Generate polatization coefficient"""
        self.pol_coef = self.get_pol_coef()

        """Other variables; True = HVT, False = LVT"""
        self.hvt = True
        self.pos_nuc_states = [True]*self.pos_nuc_count
        self.neg_nuc_states = [True]*self.pos_nuc_count

    def reset_hvt(self) -> None:
        self.hvt = True
        self.pos_nuc_states = [True]*self.pos_nuc_count
        self.neg_nuc_states = [True]*self.pos_nuc_count

    def send_pos_pulse(self, voltage: float, time: float) -> None:

        #calculate E
        E = 1

        for i in range(self.pos_nuc_count):
            if(self.pos_nuc_states[i]):
                lam = self.lam_not * math.exp(self.pol_coef \
                    * self.pos_nuc_sites[i] * E / \
                    (scipy.constants.Boltzmann * 300))
                prob = 1 - math.exp(-1*lam*time)
                # print(prob)
                flip = random.random()
                # print(flip)
                if (flip <= prob):
                    self.pos_nuc_states[i] = False

        self.hvt = any(self.pos_nuc_states)


    def read_value(self) -> None: #should this include read voltage?
        return self.hvt

    def sample_pos_nuc_count(self) -> int:
        return 10

    def sample_neg_nuc_count(self) -> int:
        return 10

    def sample_pos_sites(self, count, homog) -> int:
        return [1]*count

    def sample_neg_sites(self, count, homog) -> int:
        return [1]*count

    def sample_lam_not(self) -> int:
        return 1

    def get_pol_coef(self) -> int:
        return 0.00000000000000000001
