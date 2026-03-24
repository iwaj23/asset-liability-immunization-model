import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

liability_times = np.array([1,2,3,4,5], dtype=float)
liability_cash_flows = np.array([50000, 60000, 80000, 100000, 120000], dtype =float)

print("Liability Times:", liability_times)
print("Liability Cash Flows:", liability_cash_flows)

def present_value(cash_flows, times, i):
    cash_flows = np.array(cash_flows, dtype = float)
    times = np.array(times, dtype=float)

    pv = np.sum(cash_flows / (1+i) ** times)
    return pv

interest_rate = 0.05

pv_liabilities = present_value(liability_cash_flows, liability_times, interest_rate)

print("Present Value of Liabilities:", pv_liabilities)

def macaulay_duration(cash_flows, times, i):
    cash_flows = np.array(cash_flows, dtype=float)
    times = np.array(times, dtype=float)

    pv_cash_flows = cash_flows / (1+i) ** times
    pv_total = np.sum(pv_cash_flows)

    duration = np.sum(times * pv_cash_flows) / pv_total
    return duration

duration_liabilities = macaulay_duration(
    liability_cash_flows,
    liability_times,
    interest_rate
)

print("Liability Duration:", duration_liabilities)




def convexity(cash_flows, times, i):
    cash_flows = np.array(cash_flows, dtype=float)
    times = np.array(times, dtype=float)

    pv_cash_flows = cash_flows / (1+i)** times
    pv_total = np.sum(pv_cash_flows)

    conv = np.sum(times * (times +1) * pv_cash_flows)/ (pv_total * (1+i)**2)
    return conv

conv_liabilities = convexity(
    liability_cash_flows,
    liability_times,
    interest_rate
)

print("Liability Convexity:", conv_liabilities)
def bond_cash_flows(face, coupon_rate, maturity):
    times = np.arange(1, maturity +1)
    coupons = np.full(maturity, face * coupon_rate, dtype=float)
    coupons[-1] += face
    return coupons, times

def bond_price(face, coupon_rate, maturity, y):
    cash_flows, times = bond_cash_flows(face,coupon_rate, maturity)
    return present_value(cash_flows, times, y)

def bond_duration(face, coupon_rate, maturity,y):
    cash_flows, times = bond_cash_flows(face, coupon_rate, maturity)
    return macaulay_duration(cash_flows, times, y)

def bond_convexity(face, coupon_rate, maturity, y):
    cash_flows, times = bond_cash_flows(face, coupon_rate, maturity)
    return convexity(cash_flows, times, y)

bond_a = {"face": 1000, "coupon_rate": 0.04, "maturity": 3}
bond_b = {"face": 1000, "coupon_rate": 0.06, "maturity": 8}
bond_c = {"face": 1000, "coupon_rate": 0.05, "maturity": 5}


price_a = bond_price(**bond_a, y= interest_rate)
duration_a = bond_duration(**bond_a, y= interest_rate)

price_b = bond_price(**bond_b, y=interest_rate)
duration_b = bond_duration(**bond_b, y=interest_rate)

price_c = bond_price(**bond_c, y=interest_rate)
duration_c = bond_duration(**bond_c, y=interest_rate)
conv_c = bond_convexity(**bond_c, y=interest_rate)

conv_a = bond_convexity(**bond_a, y=interest_rate)
conv_b = bond_convexity(**bond_b, y=interest_rate)

print("\nBond A Price:", price_a)
print("Bond A Duration:", duration_a)

print("\nBond B Price:", price_b)
print("Bond B Duration:", duration_b)


#  Solve immuniztion equations
#
# 2x2 system A = np.array([
#     [price_a, price_b],
#     [price_a * duration_a, price_b * duration_b]
# ])
#
# b = np.array([
#     pv_liabilities,
#     pv_liabilities * duration_liabilities
# ])
#
# units_a, units_b = np.linalg.solve(A,b)

A = np.array([
    [price_a, price_b, price_c],
    [price_a * duration_a, price_b * duration_b, price_c * duration_c],
    [price_a * conv_a, price_b * conv_b, price_c * conv_c]
])

b = np.array([
    pv_liabilities,
    pv_liabilities * duration_liabilities,
    pv_liabilities * conv_liabilities
])

units_a, units_b, units_c = np.linalg.solve(A,b)

print("\n--- Fully Immunized Portfolio ---")
print("Units of Bond A:", units_a)
print("Units of Bond B:", units_b)
print("Units of Bond C:", units_c)


# Verify the Match

# asset_pv = units_a * price_a + units_b * price_b
# asset_dollar_duration = units_a * price_a *duration_a + units_b *price_b * duration_b
# asset_duration = asset_dollar_duration / asset_pv

asset_pv = (
    units_a * price_a +
    units_b * price_b +
    units_c * price_c
)

asset_dollar_duration = (
    units_a * price_a * duration_a +
    units_b * price_b * duration_b +
    units_c * price_c * duration_c
)

asset_duration = asset_dollar_duration / asset_pv

asset_convexity_dollar = ( units_a * price_a *conv_a +
                           units_b* price_b * conv_b +
                           units_c * price_c * conv_c
                           )

asset_convexity = asset_convexity_dollar / asset_pv

print("\n--- Verification ---")
print("Asset PV:", asset_pv)
print("Liability PV:", pv_liabilities)

print("\nAsset Duration:", asset_duration)
print("Liability Duration:", duration_liabilities)

print("\nAsset Convexity:", asset_convexity)
print("Liability Convexity:", conv_liabilities)
# Non Immunized Portfolio
# pv will match at 5%
# Duration will not match
units_a_bad = pv_liabilities / price_a
units_b_bad = 0


# Interest rate shock analysis

shock_rates = np.array([0.03, 0.04, 0.05, 0.06, 0.07])

results = []

for y in shock_rates:
    # Revalue liabilities
    liab_value = present_value(liability_cash_flows, liability_times,y)

    # Revalue Bonds
    price_a_shock = bond_price(**bond_a, y=y)
    price_b_shock = bond_price(**bond_b, y=y)

    # asset_value = units_a * price_a_shock + units_b * price_b_shock

    price_c_shock = bond_price(**bond_c, y=y)

    asset_value= (
        units_a * price_a_shock +
        units_b * price_b_shock +
        units_c * price_c_shock
    )

    surplus = asset_value - liab_value

    # Non Immunized Portfolio value
    asset_value_bad = units_a_bad * price_a_shock
    surplus_bad = asset_value_bad - liab_value

    results.append({
        "Rate": y,
        "Assets": asset_value,
        "Liabilities": liab_value,
        "Surplus": surplus,
        "Surplus_Bad": surplus_bad
    })

results_df = pd.DataFrame(results)

print("\n--- Rate Shock Analysis ---")
print(results_df)

plt.figure(figsize=(8,5))
plt.plot(results_df["Rate"], results_df["Assets"], marker="o", label="Assets")
plt.plot(results_df["Rate"], results_df["Liabilities"], marker= "o", label= "Liabilities")

plt.xlabel("Interest Rate")
plt.ylabel("Present Value")
plt.title("Assets vs Liabilities Under Interest Rate Shocks")
plt.legend()

plt.tight_layout()
# plt.show()

plt.figure(figsize=(8,5))

plt.plot(results_df["Rate"], results_df["Surplus"], marker="o")
plt.axhline(0, linestyle='--')

plt.xlabel("Interest Rate")
plt.ylabel("Surplus")
plt.title("Surplus Sensitivity to Interest Rates")

plt.tight_layout()
# plt.show()

plt.figure(figsize=(8,5))

plt.plot(results_df["Rate"], results_df["Surplus"], marker="o", label="Immunized")
plt.plot(results_df["Rate"], results_df["Surplus_Bad"],  marker="o", label= "Non-Immunized")

plt.axhline(0, linestyle="--")


plt.xlabel("Interest Rate")
plt.ylabel("Surplus")
plt.title("Immunized vs Non-immunized Portfolio")

plt.legend()
plt.tight_layout()
plt.show()

