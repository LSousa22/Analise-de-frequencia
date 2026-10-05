import unittest
import tempfile
from pathlib import Path
from src.python.analytics import load_counts, compute_metrics

class TestAnalytics(unittest.TestCase):
    def test_load_and_compute_metrics(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "counts.csv"
            # Simulando saída do scanner com 1000 palavras no total
            csv_content = (
                "# total_words,1000\n"
                "pattern,type,count\n"
                "de,digrama,50\n"
                "que,trigrama,20\n"
                "er,digrama,30\n"
            )
            csv_path.write_text(csv_content, encoding="utf-8")

            total_words, df = load_counts(csv_path)
            self.assertEqual(total_words, 1000)

            df_metrics = compute_metrics(df, total_words)

            # Verificar ranking (ordenação decrescente por count)
            self.assertEqual(df_metrics.iloc[0]["pattern"], "de")
            self.assertEqual(df_metrics.iloc[0]["count"], 50)
            self.assertAlmostEqual(df_metrics.iloc[0]["relative_frequency"], 0.05)

            self.assertEqual(df_metrics.iloc[1]["pattern"], "er")
            self.assertEqual(df_metrics.iloc[1]["count"], 30)
            self.assertAlmostEqual(df_metrics.iloc[1]["relative_frequency"], 0.03)

            self.assertEqual(df_metrics.iloc[2]["pattern"], "que")
            self.assertEqual(df_metrics.iloc[2]["count"], 20)
            self.assertAlmostEqual(df_metrics.iloc[2]["relative_frequency"], 0.02)

if __name__ == "__main__":
    unittest.main()
