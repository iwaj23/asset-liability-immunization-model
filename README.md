# Asset–Liability Immunization Model

This project implements an asset–liability management (ALM) model in Python to demonstrate how a bond portfolio can be constructed to immunize interest rate risk against a stream of future liabilities.

---

## Objective

The goal of this project is to model how actuaries and financial analysts manage interest rate risk by matching:

- Present Value (PV)
- Macaulay Duration
- Convexity

between assets and liabilities.

---

## Model Overview

### Liability Model
- Defined a schedule of future liability cash flows
- Calculated present value, duration, and convexity

### Asset Model
- Modeled multiple bonds with different maturities and coupon rates
- Calculated bond price, duration, and convexity

### Portfolio Construction
- Solved a system of equations to match:
  - PV of assets = PV of liabilities
  - Duration of assets = Duration of liabilities
  - Convexity of assets = Convexity of liabilities

---

## Interest Rate Shock Analysis

The model evaluates asset, liability, and surplus values under different interest rate scenarios.

### Key Result:
- Immunized portfolio maintains stable surplus near the target interest rate
- Non-immunized portfolio shows large sensitivity to rate changes

---

## Visualizations

### Assets vs Liabilities
![Assets vs Liabilities](Assets%20vs%20Liabilities%20Under%20Interest%20Rate%20Shocks.png)

### Surplus Sensitivity
![Surplus](Surplus%20Sensitivity%20to%20Interest%20Rates.png)

### Immunized vs Non-Immunized
![Comparison](Immunized%20vs%20Non-Immunized%20Portfolio.png)

---

## Tools Used

- Python
- NumPy
- Pandas
- Matplotlib

---

## Key Takeaways

- Duration matching provides first-order protection against interest rate changes
- Convexity matching improves stability under larger rate movements
- Asset–liability matching is a core actuarial and financial risk management technique
