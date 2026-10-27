"""
SafeCrime Quickstart Example
----------------------------
Demonstrates how to import the safecrime library, load data,
calculate risk scores, cluster states, and generate forecasts.
"""

from safecrime import SafeCrimePipeline, CrimeDataLoader, DataCleaner, RiskIndexCalculator

def main():
    print("--- SafeCrime Quickstart Demo ---")

    # Option 1: High-Level Unified Pipeline
    pipeline = SafeCrimePipeline('crime_data.csv')
    results = pipeline.run()

    print(f"Model Version: {results['metadata']['model_version']}")
    print(f"Predictive R2 Score: {results['metadata']['r2_score']:.4f}")
    print(f"Top 3 High Risk States: {[s['state'] for s in results['wsri_leaderboard'][:3]]}")
    print(f"Top 3 Safest States: {[s['state'] for s in results['wsri_leaderboard'][-3:]]}")

    # Option 2: Modular Step-by-Step Usage
    loader = CrimeDataLoader('crime_data.csv')
    cleaner = DataCleaner()
    calculator = RiskIndexCalculator()

    raw_df = loader.load()
    clean_df = cleaner.clean(raw_df)
    baseline = cleaner.get_clean_baseline(clean_df, max_year=2019)
    wsri_scores, state_averages = calculator.compute(baseline)

    print(f"\nSuccessfully evaluated {len(wsri_scores)} States & UTs.")
    print("Quickstart completed successfully.")

if __name__ == '__main__':
    main()
