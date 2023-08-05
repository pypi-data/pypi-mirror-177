import numpy as np
class HeatCapacity:
    def __init__(self, k_B, N_Av):
        """
        Instantiate the object for
        heat capacity.
        :param float k_B: Boltzmann constant.
        :param float N_Av: Avogadro's number.
        """

        self.kB = k_B
        self.NAv = N_Av

    def Cv(self, T, V, P):
        """
        Heat capacity
        :param float T: the temperature in K.
        :param float V: the volume in m3/mol-at.
        :param float P: the pressure in Pa.
        :return float: the heat capacity.
        """

        return np.dot(3, np.dot(self.kB, self.NAv))
