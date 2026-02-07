# Econophysics: Entropy-Volatility State Analysis

This project implements an **advanced market dynamics analyzer** that transcends traditional finance by applying concepts from **statistical mechanics** and **information theory**. By shifting the focus from price levels to **Information Entropy**, it detects hidden market regimes and quantifies the "disorder" that precedes high-risk events.

---

## 1. Why Econophysics & Entropy?

Traditional finance often assumes markets are "normal." However, real markets exhibit **Fat Tails** and **clustering of volatility**. This project uses:
* **Shannon Entropy**: To measure the uncertainty and complexity of the price return distribution.
* **Dynamic Coupling**: Analyzing how "market disorder" (Entropy) relates to "market fear" (Volatility).
* **Regime Detection**: Identifying periods where the market moves from a stable state to a chaotic state.

---

## 2. The Mechanics of Market Entropy

Unlike standard deviation which only measures the "spread" of returns, **Shannon Entropy** ($H$) quantifies the amount of information or "surprise" in the market. 

The entropy $H$ of the return distribution is calculated as:

$$H(X) = - \sum_{i=1}^{n} P(x_i) \log_e P(x_i)$$

**Where:**
* **$P(x_i)$**: The probability density of a return falling into a specific bin $i$.
* **$n$**: The total number of bins in the histogram.

---

## 3. Market State & Regime Analysis

### 3.1 Volatility vs. Entropy Coupling
This analysis compares normalized Volatility and Entropy to detect **informational divergence**. While they typically correlate, a decoupling - where Entropy rises while Volatility remains flat - often suggests a "simmering" instability where the distribution of returns is becoming more disordered before a major price breakout.

![Normalized Metrics](assets/01_normalized_metrics.png?v=1)

### 3.2 Phase Space Analysis (The System's Trajectory)
By plotting Volatility against Entropy, we move from time-series to **topology**. This "Phase Space" reveals the system's attractor. 
* **Stable Orbits:** Tight clusters at low Vol/low Ent.
* **Chaotic Escapes:** Rapid movements toward the top-right corner, indicating a transition from a Gaussian-like state to a high-disorder crisis state. The color gradient tracks the temporal evolution of these transitions.

![Phase Space](assets/02_phase_space.png?v=1)

### 3.3 Returns Distribution (The Fat Tail Proof)
This chart provides empirical evidence for the project's necessity. By overlaying a Kernel Density Estimate (KDE) on the histogram, we visualize **excess kurtosis**. The significant "Fat Tails" (extreme values) demonstrate why Gaussian models fail to capture the 5-sigma events that Econophysics tools are designed to monitor.

![Distribution](assets/03_returns_distribution.png?v=1)

---

## 4. Risk Dynamics & Sensitivity

### 4.1 Rolling Correlation (Risk-Disorder Link)
We compute a 60-day rolling correlation between Volatility and Entropy. This metric tracks the **informational efficiency** of the market. 
* **High Correlation:** Standard panic where risk and disorder move in lockstep.
* **Correlation Drops:** May indicate "hidden" regimes where price swings don't match the internal complexity of the market, often seen in manipulated or highly illiquid environments.

![Correlation](assets/04_rolling_correlation.png?v=1)

### 4.2 High Entropy Regime Detection (Thresholding)
Using a **90th percentile threshold**, we isolate "Extreme Disorder" events. Unlike simple volatility spikes, these shaded regions highlight periods where the market's internal structure is breaking down. This acts as a signal for **non-stationary regimes** where traditional trading models are most likely to fail.

![Regime Detection](assets/05_regime_detection.png?v=1)

### 4.3 Risk Surface: Multi-Scale Bin Sensitivity
This heatmap is a **robustness test**. Entropy calculation is sensitive to the number of bins (resolution). 
* **Signal Stability:** A consistent horizontal color gradient indicates that our findings are "scale-invariant" and not an artifact of specific binning. 
* **Interpretation:** Smooth transitions across the y-axis (bins 5 to 50) validate that the detected market regimes are a fundamental property of the data, ensuring the model's reliability across different market conditions.

![Risk Surface](assets/06_risk_surface.png?v=1)
