# Claude prompts for extending the dashboard

## 1) Upgrade the scoring model
You are helping me extend a forensic market-microstructure dashboard. I have a Streamlit app and CSVs describing impugned days, entity economics, timeline events, market-structure metrics, and a Jan 17, 2024 reconstruction. I want you to improve the footprint scoring model for research attribution.

Tasks:
1. Treat this as a surveillance / forensics problem, not a live trading system.
2. Propose a statistically conservative scoring framework using small-positive-sample methods.
3. Compare a logistic baseline, KDE likelihood-ratio model, and regularized Gaussian mixture approach.
4. Define features around concentration, settlement-window intensity, options-vs-underlying imbalance, reversal strength, and directional exposure build.
5. Return Python code that plugs into a Streamlit app and outputs probability, confidence band, and feature contributions.
6. Include calibration and leave-one-out validation suggestions.

## 2) Improve the mechanistic simulator
I have a Streamlit dashboard with a stylized simulator based on a quantitative note. The current simulator uses:
- Index move in bps
- Delta coefficient
- Gamma coefficient
- Market-impact cost coefficient
- Net PnL = Delta * move + 0.5 * Gamma * move^2 - kappa * |move|

I want you to:
1. Keep the framing educational and forensic.
2. Extend the simulator to include optional vega / IV-lift terms, expiry decay, and constituent-weight sensitivity.
3. Produce clean Python code and charts suitable for Streamlit.
4. Add scenario presets for Jan 17, Jul 10, and May 15.
5. Include a sensitivity tornado chart and contour plot.

## 3) Build a cross-market research module
I want to extend the dashboard to study whether similar footprints appear in:
- South Korea block-trade regimes
- Crypto spot/perpetual/options venues

Please:
1. Define a unified feature schema that can transfer across markets.
2. Separate market-specific features from global features.
3. Provide a code architecture for market adapters.
4. Suggest how to compare footprint distributions across India, Korea, and crypto.
5. Return a Streamlit-ready design with tabs, charts, and data contracts.
