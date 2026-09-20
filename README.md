# Does the Invisible Hand Matter for Economic Decisions?
### A Study of India's Short-Term Electricity Market (Power Exchange Market)

Term paper for HS5704 (History of Economic Thought), applying Adam Smith's
invisible-hand and Hayek's price-discovery ideas to India's short-term
power exchange market (IEX / PXIL / HPX), using the CERC price-cap episode
(2022–present) and the ongoing market-coupling litigation as natural
experiments.

## Contents

- `docs/` — the term paper (Word document), including the OLS regression
  results and interpretation in the Findings section.
- `data/`
  - `iex_dam_monthly_mcp_2017_2026.csv` — raw IEX day-ahead market (DAM)
    monthly average clearing price series, January 2017 – March 2026,
    plus CERC price-ceiling reference points and exchange market-share
    figures used for the HHI calculation.
  - `regression_data_with_regressors.csv` — the same price series with
    the constructed regressors (`Trend`, `Cap`, `CoalShock`, `Summer`)
    used in the regression model.
- `analysis/regress.py` — Python script that builds the regressors and
  estimates the OLS model:

  ```
  MCP_t = β0 + β1·Trend_t + β2·Cap_t + β3·CoalShock_t + β4·Summer_t + ε_t
  ```

  Run with `python3 analysis/regress.py` (requires `pandas`, `numpy`,
  `scipy`).

## Key result

| Variable | Coefficient | p-value |
|---|---|---|
| Intercept | 3.823 | < 0.001 |
| Trend | -0.018 | 0.004 |
| Cap (post-Apr 2022) | 2.461 | < 0.001 |
| CoalShock (Oct 2021–Apr 2022) | 2.681 | < 0.001 |
| Summer (Apr–Jun) | 0.412 | 0.064 |

n = 111, R² = 0.46, F(4,106) = 22.83, p < 0.001. See the term paper's
Findings section for full interpretation and caveats (notably
autocorrelated residuals, Durbin–Watson = 0.90).

## Sources

CERC Annual Reports on the Short-Term Power Market (2022–24); IEX monthly
power-market updates and filings; Grid-India shadow-pilot reports on
market coupling (Jan & Jun 2025); Business Standard, Mercom India, Saur
Energy, Powerline, Kotak-CNBC-Awaaz coverage of the Supreme Court
proceedings.
