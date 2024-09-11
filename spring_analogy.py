import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Assuming 'data' is your DataFrame and 'volume_oscillator' is a column
volume_oscillator = data['volume_oscillator'].values

# Inverting the volume oscillator to find minima as peaks
inverted_vol_osc = -volume_oscillator

# Detecting minima (peaks in inverted data)
peaks, _ = find_peaks(inverted_vol_osc, distance=5)  # 'distance' can be adjusted

# Plotting to validate
plt.plot(volume_oscillator)
plt.plot(peaks, volume_oscillator[peaks], 'rx')
plt.title("Volume Oscillator with Minima")
plt.show()
import math

# Function to simulate the spring rebound effect
def spring_rebound(t, A, gamma, omega, phi=0):
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

# Parameters to control the spring effect
A = 1  # Initial amplitude (could be tied to the magnitude of the oscillator)
gamma = 0.05  # Damping factor (controls how fast the oscillations fade)
omega = 0.1   # Frequency (can be linked to market cycles)

# Create a time series of predicted price changes
time_steps = np.arange(0, 50, 0.1)  # Simulate for 50 time units
predicted_price_movements = spring_rebound(time_steps, A, gamma, omega)

# Plot the rebound effect
plt.plot(time_steps, predicted_price_movements)
plt.title("Spring Rebound Effect on Price")
plt.show()
# Initialize an array to store predicted price movements
predicted_prices = np.zeros_like(volume_oscillator)

# For each detected minima, apply the spring rebound
for peak in peaks:
    for t in range(len(time_steps)):
        if peak + t < len(predicted_prices):
            predicted_prices[peak + t] += spring_rebound(t, A, gamma, omega)

# Plotting actual vs. predicted price
plt.plot(data['price'], label='Actual Price')
plt.plot(predicted_prices, label='Predicted Price')
plt.title("Actual vs. Predicted Price with Spring Model")
plt.legend()
plt.show()
