import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os
from scipy.stats import entropy, skew, kurtosis


class EconophysicsAnalyzer:
    def __init__(self, ticker, start, end):
        self.ticker = ticker.replace("^", "")
        self.start = start
        self.end = end
        self.data = None
        self.results = pd.DataFrame()
        if not os.path.exists('assets'):
            os.makedirs('assets')

    def fetch_market_data(self):
        t_id = "^GSPC" if self.ticker == "GSPC" else self.ticker
        df = yf.download(t_id, start=self.start, end=self.end, progress=False)
        self.data = df['Close'].pct_change().dropna()
        if isinstance(self.data, pd.DataFrame): 
            self.data = self.data.iloc[:, 0]

    def compute_metrics(self, window=20, bins=15):
        vol = self.data.rolling(window).std() * np.sqrt(252)
        
        def _get_entropy(x):
            p, _ = np.histogram(x, bins=bins, density=True)
            return entropy(p + 1e-10)

        ent = self.data.rolling(window).apply(_get_entropy, raw=False)
        self.results = pd.DataFrame({
            'Volatility': vol, 'Entropy': ent,
            'Vol_Norm': (vol - vol.min()) / (vol.max() - vol.min()),
            'Ent_Norm': (ent - ent.min()) / (ent.max() - ent.min())
        }).dropna()

    def generate_outputs(self):
        if self.results.empty: self.compute_metrics()
        
        plt.rcParams.update({'font.size': 10, 'font.family': 'sans-serif'})
        plt.style.use('ggplot')

        # 1. Normalized Series
        plt.figure(figsize=(10, 6))
        plt.plot(self.results['Vol_Norm'], label='Vol', alpha=0.7)
        plt.plot(self.results['Ent_Norm'], label='Ent', linestyle='--')
        plt.title("Volatility vs Entropy (Normalized)")
        plt.legend()
        plt.savefig("assets/01_normalized_metrics.png", dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Phase Space
        plt.figure(figsize=(10, 6))
        sc = plt.scatter(self.results['Volatility'], self.results['Entropy'], 
                         c=range(len(self.results)), cmap='viridis', s=10)
        plt.title("Phase Space: Entropy-Volatility")
        plt.colorbar(sc, label='Time Flow')
        plt.savefig("assets/02_phase_space.png", dpi=300, bbox_inches='tight')
        plt.close()

        # 3. Distribution
        plt.figure(figsize=(10, 6))
        self.data.hist(bins=60, alpha=0.4, color='gray', density=True)
        self.data.plot(kind='kde', color='red')
        plt.title("Non-Gaussian Returns Distribution")
        plt.savefig("assets/03_returns_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()

        # 4. Correlation
        plt.figure(figsize=(10, 6))
        corr = self.results['Volatility'].rolling(60).corr(self.results['Entropy'])
        avg_corr = corr.mean()
        plt.plot(corr, color='purple')
        plt.axhline(avg_corr, color='black', ls=':', label=f'Mean: {avg_corr:.2f}')
        plt.title("Rolling Correlation (60D)")
        plt.legend()
        plt.savefig("assets/04_rolling_correlation.png", dpi=300, bbox_inches='tight')
        plt.close()

        # 5. Regime Detection
        plt.figure(figsize=(10, 6))
        q90 = self.results['Entropy'].quantile(0.90)
        plt.plot(self.results['Entropy'], color='darkred')
        plt.axhline(q90, color='black', ls='--', label=f'90th: {q90:.2f}')
        plt.fill_between(self.results.index, self.results['Entropy'], q90, 
                         where=(self.results['Entropy'] >= q90), color='red', alpha=0.2)
        plt.title("Market Regime Detection")
        plt.legend()
        plt.savefig("assets/05_regime_detection.png", dpi=300)
        plt.close()

        # 6. Risk Surface
        plt.figure(figsize=(10, 6))
        bins_range = range(5, 55, 5)
        surface = [self.data.rolling(20).apply(lambda x: entropy(np.histogram(x, bins=b)[0]+1e-10)).values for b in bins_range]
        mat = np.array([s[-min(map(len, surface)):] for s in surface])
        plt.imshow(mat, aspect='auto', cmap='magma', extent=[0, mat.shape[1], 50, 5])
        plt.title("Risk Surface: Bin Sensitivity")
        plt.colorbar()
        plt.savefig("assets/06_risk_surface.png", dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    model = EconophysicsAnalyzer("^GSPC", "2019-01-01", "2025-01-01")
    model.fetch_market_data()
    model.generate_outputs()
