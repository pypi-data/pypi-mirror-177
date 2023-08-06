from test_package import HeatCapacity

# Some definitions
kB = 0.6022140857e24
NAv = 0.138064852e-22

# Inputs
Temperature = 1000  # K
Volume = 9e-6  # m3/mol-at
Pressure = 0  # GPa

# Instantiate the HeatCapacity object
ihc = HeatCapacity(kB, NAv)

# Call the Cv method
print(ihc.Cv(Temperature, Volume, Pressure))
