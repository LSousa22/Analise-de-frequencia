import unittest
import subprocess
import tempfile
from pathlib import Path
from src.python.config import SCANNER_BIN

class TestScannerE2E(unittest.TestCase):
    def test_scanner_execution_pt(self):
        self.assertTrue(SCANNER_BIN.exists(), f"Executável {SCANNER_BIN} não encontrado")

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = Path(tmpdir) / "test_corpus.txt"
            output_csv = Path(tmpdir) / "output.csv"

            # 4 palavras: queijo, queijo, banana, aaa
            # Em 'aaa' o padrao 'aa' ocorre 2 vezes (overlap)
            # Em 'queijo' o padrao 'qu' ocorre 1 vez (2x no total), 'que' 1 vez (2x no total)
            content = "# DOC: sample\nqueijo queijo banana aaa\n"
            input_file.write_text(content, encoding="utf-8")

            res = subprocess.run(
                [str(SCANNER_BIN), "pt", str(input_file), str(output_csv)],
                capture_output=True,
                text=True
            )
            self.assertEqual(res.returncode, 0, f"Scanner falhou: {res.stderr}")
            self.assertTrue(output_csv.exists())

            lines = output_csv.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(lines[0], "# total_words,4")
            self.assertEqual(lines[1], "pattern,type,count")

            counts = {}
            for line in lines[2:]:
                pattern, p_type, count = line.split(",")
                counts[pattern] = int(count)

            self.assertEqual(counts["qu"], 2)
            self.assertEqual(counts["que"], 2)

if __name__ == "__main__":
    unittest.main()
