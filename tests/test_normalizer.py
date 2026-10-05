import unittest
from src.python.normalizer import normalize_text, normalize_pattern

class TestNormalizer(unittest.TestCase):
    def test_normalize_pattern(self):
        # Must strip accents, diacritics, spaces and convert to lowercase
        self.assertEqual(normalize_pattern("TÃO"), "tao")
        self.assertEqual(normalize_pattern("QUE"), "que")
        self.assertEqual(normalize_pattern("  éR "), "er")

    def test_normalize_text_case_and_accents(self):
        # Exemplo com acentos e maiúsculas
        raw = "Atenção! O cão veloz comeu maçã e pão."
        expected = ["atencao", "o", "cao", "veloz", "comeu", "maca", "e", "pao"]
        self.assertEqual(normalize_text(raw), expected)

    def test_normalize_text_punctuation_numbers_special(self):
        # Deve remover pontuações, números e caracteres especiais
        raw = "Cripto-101: Teste (2026), com 100% de precisão! @user #hashtag."
        expected = ["cripto", "teste", "com", "de", "precisao", "user", "hashtag"]
        self.assertEqual(normalize_text(raw), expected)

if __name__ == "__main__":
    unittest.main()
