import pandas as pd
import numpy as np

df = pd.read_csv("Electricity_power_exchange_analysis__-_IEX_DAM_monthly_MCP_Jan2017_Mar2026.csv")
df = df[['Month','Calendar_Year','IEX_DAM_Average_MCP_Rs_per_kWh']].dropna()
df = df.rename(columns={'IEX_DAM_Average_MCP_Rs_per_kWh':'MCP'})

# Parse month
def parse_month(m):
    mon, yr = m.split('-')
    return pd.Period(f"{mon} {yr}", freq='M')

df['Period'] = df['Month'].apply(parse_month)
df = df.sort_values('Period').reset_index(drop=True)
df['Trend'] = np.arange(1, len(df)+1)

month_num = df['Period'].dt.month
df['Cap'] = (df['Period'] >= pd.Period('2022-04', freq='M')).astype(int)
df['CoalShock'] = df['Period'].between(pd.Period('2021-10','M'), pd.Period('2022-04','M')).astype(int)
df['Summer'] = month_num.isin([4,5,6]).astype(int)

print(df[['Month','MCP','Trend','Cap','CoalShock','Summer']].to_string())
print("N =", len(df))

y = df['MCP'].values.astype(float)
X = df[['Trend','Cap','CoalShock','Summer']].values.astype(float)
X1 = np.column_stack([np.ones(len(X)), X])

# OLS
beta, residuals, rank, sv = np.linalg.lstsq(X1, y, rcond=None)
yhat = X1 @ beta
resid = y - yhat
n, k = X1.shape
dof = n - k
mse = np.sum(resid**2) / dof
XtX_inv = np.linalg.inv(X1.T @ X1)
se = np.sqrt(np.diag(mse * XtX_inv))
tvals = beta / se

# R2
ss_res = np.sum(resid**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res/ss_tot
adj_r2 = 1 - (1-r2)*(n-1)/(n-k)

# F-stat
ss_reg = ss_tot - ss_res
df_reg = k - 1
f_stat = (ss_reg/df_reg) / (ss_res/dof)

from scipy import stats
pvals = 2*(1 - stats.t.cdf(np.abs(tvals), dof))
f_pval = 1 - stats.f.cdf(f_stat, df_reg, dof)

names = ['Intercept','Trend','Cap','CoalShock','Summer']
print("\nCoefficients:")
for nme, b, s, t, p in zip(names, beta, se, tvals, pvals):
    print(f"{nme:12s} beta={b:.5f}  se={s:.5f}  t={t:.3f}  p={p:.4f}")

print(f"\nR2 = {r2:.4f}, Adj R2 = {adj_r2:.4f}")
print(f"F({df_reg},{dof}) = {f_stat:.3f}, p={f_pval:.6f}")
print(f"n={n}")

# Durbin-Watson
dw = np.sum(np.diff(resid)**2) / np.sum(resid**2)
print(f"Durbin-Watson = {dw:.3f}")

df.to_csv("regression_data.csv", index=False)
