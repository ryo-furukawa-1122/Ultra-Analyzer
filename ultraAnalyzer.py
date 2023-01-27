import numpy as np
import matplotlib.pyplot as plt
import glob

csv_files = glob.glob('*.csv')  # From AP-Acquisition

sens = [27, 29, 30, 33, 36, 38, 40]  # 300-900 Hz, in (nV/Pa)
f_sens = np.arange(300, 900, 100)

target = '.'

for file in csv_files:
    data = np.loadtxt(file, delimiter=',', skiprows=0, encoding='utf-8')
    
    idx = file.find(target)
    
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
