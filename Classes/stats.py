import statistics as stat
import numpy as np
import matplotlib.pyplot as plt
import math
from pathlib import Path

class Stats:
    def __init__(self, name, data, year, type, division, gender, ac, wc):
        self.name = name
        self.data = data
        self.year = year
        self.wc = wc
        self.type = type
        self.division = division
        self.gender = gender
        self.ac = ac
        self.stats = self.calculate_stats()

    def calculate_stats(self):
        return {
            'mean': stat.mean(self.data),
            'median': stat.median(self.data),
            'mode': stat.mode(self.data),
            'std': stat.stdev(self.data),
            'var': stat.variance(self.data),
            'min': np.min(self.data),
            'max': np.max(self.data)
        }

    def print_stats(self):
        print(f"Statistiques {self.name} - {self.year} - {self.wc}")
        for key, value in self.stats.items():
            print(f"{key}: {value:.2f}")

    def plot_histogram(self, bins=None, save_dir=f"histograms/"):
        output_dir = Path(save_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        if bins is None:
            bins = math.ceil(np.sqrt(len(self.data)))
        plt.hist(self.data, bins=bins, edgecolor='black', alpha=0.7)
        plt.xlabel(self.name)
        plt.ylabel('Fréquence')
        plt.title(f'Histogramme des {self.name} chez les {self.wc} {self.ac} en {self.year}')
        save_path = output_dir / f"histogram_{self.name.lower()}.png"
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.show()
        plt.show()
