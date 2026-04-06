import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
wl_list = []
abs_list = []

try:
    num_readings = int(input("How many wavelength readings did you take? "))
    for i in range(num_readings):
        w = float(input(f" Reading #{i+1} - Wavelength (nm): "))
        a = float(input(f" Reading #{i+1} - Absorbance: "))
        wl_list.append(w)
        abs_list.append(a)
except ValueError:
    print("Invalid input. Please enter numbers only.")
    exit()

max_idx = np.argmax(abs_list)
lambda_max = wl_list[max_idx]
max_abs = abs_list[max_idx]

print(f"\n{'='*40}")
print(f"OPTIMAL WAVELENGTH (λ_max): {lambda_max} nm")
print(f"Peak Absorbance: {max_abs}")
print(f"{'='*40}\n")
plt.figure(figsize=(8, 5))
plt.plot(wl_list, abs_list, marker='o', color='darkred', label='Absorption Spectrum')
plt.axvline(x=lambda_max, color='blue', linestyle='--', label=f'Peak: {lambda_max}nm')
plt.title("Phase 1: Finding λ_max")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance")
plt.legend()
plt.show()

print("Now proceeding to your Concentration Calibration...")
try:
    num_standards = int(input("How many standard solutions (including blank)? "))
    if num_standards < 2:
        print("Error: You need at least 2 standards to create a calibration curve.")
        exit()
except ValueError:
    print("Please enter a valid number.")
    exit()

volumes = []
concs = []
abs_values = []

for i in range(num_standards):
    print(f"\nStandard #{i+1}:")
    try:
        v = float(input(f"  Enter Volume (mL): "))
        c = float(input(f"  Enter Concentration: "))
        a = float(input(f"  Enter Absorbance: "))

        volumes.append(v)
        concs.append(c)
        abs_values.append(a)
    except ValueError:
        print("Invalid numerical input. Please restart.")
        exit()

X_train = np.array(abs_values).reshape(-1, 1)
y_train = np.array(concs).reshape(-1, 1)

model = LinearRegression()
model.fit(X_train, y_train)

reliability_score = model.score(X_train, y_train)

print("\n" + "="*40)
print(f"CALIBRATION RELIABILITY: {reliability_score:.4f}")

if reliability_score >= 0.98:
    print("Status: Excellent Precision.")
elif reliability_score >= 0.90:
    print("Status: Good (Minor experimental error).")
else:
    print("Status: LOW RELIABILITY. Check your data.")
print("="*40)

try:
    unknown_abs = float(input("\nEnter Absorbance of the UNKNOWN sample: "))
except ValueError:
    print("Invalid numerical input.")
    exit()

predicted_conc = model.predict(np.array([[unknown_abs]]))[0][0]

print(f"\n>> PREDICTED CONCENTRATION: {predicted_conc:.4f} <<")

plt.figure(figsize=(10, 6))

plt.scatter(X_train, y_train, color='blue', label='Lab Standards', s=100)
plt.text(0.5, 0.1, 'Developed by Harsh', fontsize=10, color='gray',alpha=0.5, transform=plt.gca().transAxes)

x_range = np.linspace(min(X_train)[0]*0.8, max(X_train)[0]*1.2, 100).reshape(-1, 1)
y_range = model.predict(x_range)
plt.plot(x_range, y_range, color='red', linestyle='--', label=f'Best Fit Line (Reliability: {reliability_score:.4f})')


plt.scatter([unknown_abs], [predicted_conc], color='green', marker='*', s=120,
            label=f'Predicted Unknown: {predicted_conc:.2f}', edgecolor='black', linewidth=1.0, zorder=10)

plt.title('Fe3+ Calibration Curve (Absorbance vs Concentration)', fontsize=14)
plt.xlabel('Absorbance ($A$)', fontsize=12)
plt.ylabel('Concentration ($C$)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

plt.show()


