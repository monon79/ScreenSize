import unittest
import pandas as pd
from soil_lab.calculations import clean_sieve_data, calculate_sieve_results, soil_parameters, design_filter_pack

class SieveCalculationTests(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'sieve_mm': [4.75, 2.0, 0.425, 0.25, 0.15, 0.075, 0.0],
            'retained_g': [25, 45, 110, 90, 100, 80, 50],
        })

    def test_sorting_and_mass_recovery(self):
        result = calculate_sieve_results(self.data, 500)
        self.assertEqual(result.iloc[0]['sieve_mm'], 4.75)
        self.assertAlmostEqual(result.attrs['mass_recovery_pct'], 100.0)
        self.assertAlmostEqual(result.iloc[-1]['percent_passing'], 0.0)

    def test_reject_mass_overrun(self):
        with self.assertRaises(ValueError):
            calculate_sieve_results(self.data, 400)

    def test_reject_duplicate_sieve(self):
        bad = pd.concat([self.data, self.data.iloc[[0]]], ignore_index=True)
        with self.assertRaises(ValueError):
            clean_sieve_data(bad)

    def test_characteristic_parameters(self):
        result = calculate_sieve_results(self.data, 500)
        params = soil_parameters(result)
        self.assertGreater(params['D10'], 0)
        self.assertGreater(params['D30'], params['D10'])
        self.assertGreater(params['Cu'], 1)

    def test_filter_pack_d30_ratio_and_cu(self):
        curve, pack = design_filter_pack(0.1, factor=5, target_cu=2.0)
        self.assertAlmostEqual(pack['D30'], 0.5, places=10)
        self.assertAlmostEqual(pack['Cu'], 2.0, places=10)
        self.assertEqual(len(curve), 300)

if __name__ == '__main__':
    unittest.main()
