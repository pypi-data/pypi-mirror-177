import os
import yaml
from yaml.loader import SafeLoader
from ambiance import Atmosphere


class AircraftEngines:

    def __init__(self, config_file_path):
        if not os.path.isfile(config_file_path):
            self.__create_config()
        self.__data = yaml.load(open(config_file_path), SafeLoader)

        self.__atm = Atmosphere(self.__data['height'])
        self.T0 = self.__atm.temperature
        self.P0 = self.__atm.pressure
        self.a0 = self.__atm.speed_of_sound

        self.M0 = self.__data['mach']
        self.gamma = self.__data['gamma']
        self.cp = self.__data['cp']
        self.hpr = self.__data['hpr']
        self.Tt4 = self.__data['Tt4']
        self.pi_c = self.__data['pi_c']

    def __create_config():
        data = {

        }

        with open('config.yml', 'w') as f:
            yaml.dump(data, f)

    def ideal_turbojet(self):
        R = (self.gamma - 1)/self.gamma * self.cp # J/(kg.K)
        V0 = self.a0 * self.M0 # m/s

        tau_r = 1 + (self.gamma - 1)/2 * self.M0**2

        tau_c = self.pi_c**((self.gamma - 1)/self.gamma)

        tau_lambda = self.Tt4/self.T0
        f = self.cp * self.T0/self.hpr * (tau_lambda - tau_r * tau_c) # kgFuel/kgAir

        tau_t = 1 - tau_r/tau_lambda * (tau_c - 1)
        V9_a0 = (2/(self.gamma - 1 )* tau_lambda/(tau_r * tau_c) * (tau_r * tau_c * tau_t - 1))**(1/2)

        F_m0 = self.a0 * (V9_a0 - self.M0) # N/(kg/s)
        S = f/F_m0 # (kgFuel/s)/N
        eta_T = 1 - 1/(tau_r * tau_c)
        eta_P = 2 * self.M0/(V9_a0 + self.M0)
        eta_Total = eta_P * eta_T

        print('Razao F/mo_p, (N/(kg/s))          = ', F_m0)
        print('Fuel air ratio, f         = ', f)
        print('Consumo especifico, S ((kg/s)/N)  = ', S)
        print('Eficiencia termica                = ', eta_T)
        print('Eficiencia propulsiva             = ', eta_P)
        print('Eficiencia total                  = ', eta_Total)

def main():
    test = AircraftEngines('config.yaml')

    test.ideal_turbojet()

if __name__ == '__main__': main()