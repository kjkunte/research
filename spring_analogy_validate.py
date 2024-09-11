import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load your data
data = pd.read_csv('your_data.csv')  # Replace with your actual data source
price = data['price'].values
volume_oscillator = data['volume_oscillator'].values

# 2. Detect minima in the volume oscillator
inverted_vol_osc = -volume_oscillator
peaks, _ = find_peaks(inverted_vol_osc, distance=5)

# 3. Define the spring rebound function
def spring_rebound(t, A, gamma, omega, phi=0):
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

# 4. Initialize model parameters
A = 1.0
gamma = 0.05
omega = 0.1
phi = 0
time_steps = np.arange(0, 50, 0.1)
scaling_factor = 0.1

# 5. Initialize predicted prices
predicted_prices = np.zeros_like(price)

# 6. Apply the spring model at each detected minima
for peak in peaks:
    A_peak = scaling_factor * abs(volume_oscillator[peak] - np.mean(volume_oscillator))
    rebound = spring_rebound(time_steps, A_peak, gamma, omega, phi)
    for i, t in enumerate(time_steps):
        idx = peak + i
        if idx < len(predicted_prices):
            predicted_prices[idx] += rebound[i]

# 7. Normalize predicted prices (optional)
predicted_prices = predicted_prices / np.max(np.abs(predicted_prices)) * np.std(price)

# 8. Overlay the actual and predicted prices
plt.figure(figsize=(14, 6))
plt.plot(price, label='Actual Price', color='blue')
plt.plot(predicted_prices, label='Predicted Price (Spring Model)', color='orange', alpha=0.7)
plt.title("Actual vs. Predicted Price with Spring Model")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()

# 9. Quantitative Validation
rmse = np.sqrt(mean_squared_error(price, predicted_prices))
r2 = r2_score(price, predicted_prices)
print(f"Root Mean Square Error (RMSE): {rmse:.4f}")
print(f"Coefficient of Determination (R²): {r2:.4f}")
