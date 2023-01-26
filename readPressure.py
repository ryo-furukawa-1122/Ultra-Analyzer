import numpy as np
import sys
import matplotlib.pyplot as plt
import os
import glob

csv_files = glob.glob('*.csv')  #

sensFactor = [27, 29, 30, 33, 36, 38, 40]  #300-900 Hz, in (nV/Pa)

for file in csv_files:
    save_name = file[0] + '.' + file[2]
    data = np.loadtxt(file, delimiter=',', skiprows=12, encoding='utf-8')
    
    t = data[:, 0]
    p = data[:, 1]

    p /= 10  #プレアンプ
    p /= 30 * 1e-9  #signal scale nV/Pa

    samp_time = t[1] - t[0]  #[s]

    #FFT
    F1 = np.fft.fft(p)
    freq = np.fft.fftfreq(t.size, d=samp_time)

    #BPF
    F2 = np.copy(F1)
    fc_l = 1e6  #カットオフ周波数(LPF)
    fc_h = 100e3  #カットオフ周波数(HPF)
    F2[freq > fc_l] = 0  #LPF
    F2[freq < fc_h] = 0  #HPF
    F2_ifft = np.fft.ifft(F2)
    F2_ifft_real = F2_ifft.real * 2
    F2_ifft = np.fft.ifft(F2)

    #Figure
    plt.plot(t * 1e6, F2_ifft_real * 1e-3, label='Filtered data', color='blue')
    plt.plot(t * 1e6, p * 1e-3, label='Raw data', color='black')
    plt.legend(loc='best')
    plt.xlabel('Time [\u03bcs]')
    plt.ylabel('Acoustic pressure [kPa]')
    #plt.show()
    os.chdir("Filtered data/")
    print(os.getcwd())
    plt.savefig(save_name + 'MHz.png')  #save
    plt.close()

    #csv
    save_csv = np.c_[t, F2_ifft_real]
    np.savetxt('Filtered_' + save_name + 'MHz.csv', save_csv, delimiter=',')
    os.chdir("../")
    print(os.getcwd())
        
