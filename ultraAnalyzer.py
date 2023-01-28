import numpy as np
import matplotlib.pyplot as plt
import glob
from scipy import integrate

csv_files = glob.glob('*.csv')  # From AP-Acquisition

sens = [27, 29, 30, 33, 36, 38, 40]  # 300-900 Hz, in (nV/Pa)
f_sens = np.arange(300, 900, 100)

# Read signals representing acoustic pressures
for file in csv_files:
    data = np.loadtxt(file, delimiter=',', skiprows=0, encoding='utf-8')
    
    idx = file.find('.')
    
    f = file[:idx]  # file name i.e., frequency
    t = data[:, 0]
    p = data[:, 1]
    
    # Chose the suitable sensitivity
    f_round = round(f, -2)
    for i in sens:
        if f_round == f_sens[i]:
            scale = sens[i]

    p /= 10  # pre amplifire
    p /= scale * 1e-9  #signal scale nV/Pa

    # Figure
    plt.plot(t * 1e6, p * 1e-3, color='black')
    plt.xlabel('Time (\u03bcs)')
    plt.ylabel('Acoustic pressure (kPa)')
    plt.savefig(f'data/{f}.png')  #save
    plt.close()

    # csv
    save_csv = np.c_[t, p]
    np.savetxt(f'data/{f}_pressure.csv', save_csv, delimiter=',')

# Analyze acoustic pressure
p_files = glob.glob('data/*.csv')

rho = 997  # in kg/m^3
c = 1.480e3  # in m/s

frequency = []
pressure = []
intensity = []

for p_file in p_files:
    data_p = np.loadtxt(p_file, delimiter=',', skiprows=0, encoding='utf-8')

    t = data_p[:, 0]
    p = data_p[:, 1]
    
    idy = p_file.find('_')
    
    freq = p_file[:idy]
    freq = float(freq)  # in kHz
    
    # Amplitude of acoustic pressure
    pmax = max(p)  # in Pa
    pmax *= 1e-3  # in kPa
    
    # Calculation of intensity
    pii = integrate.cumtrapz(p**2 / (rho*c), t, initial=0)
    I_sppa = pii[len(t)-1] / (t[len(t)-1] * 2)  # in W/m^2
    I_sppa *= 1e-4  # in W/cm^2
    
    frequency.append(freq)
    pressure.append(pmax)
    intensity.append(I_sppa)

# Summarize in this channel
summary_csv = np.c_[frequency, pressure, intensity]
np.savetxt('data/freq_summary.csv', summary_csv, delimiter=',')
