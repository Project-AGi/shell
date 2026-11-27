import unittest

from aiva_cryptic_signal_core import CrypticSignalCore


class CrypticSignalCoreTest(unittest.TestCase):
    def setUp(self):
        self.core = CrypticSignalCore()

    def test_default_scheme_round_trips_utf8(self):
        for text in ("", "Hello, AIVA!", "こんにちは 🌱", "spaces  and\nnewlines", "café"):
            with self.subTest(text=text):
                signal, pulse = self.core.encode(text)
                self.assertEqual(self.core.default_scheme(), "ternary_utf8_v1")
                self.assertEqual(self.core.decode(signal, pulse), text)

    def test_unknown_scheme_fails_closed_for_encode_and_decode(self):
        with self.assertRaisesRegex(ValueError, "Unsupported AIVA signal scheme"):
            self.core.encode("Hello", "missing-v2")
        with self.assertRaisesRegex(ValueError, "Unsupported AIVA signal scheme"):
            self.core.decode(b"", 0, "missing-v2")

    def test_decode_rejects_mismatched_length_and_invalid_pulse(self):
        signal, pulse = self.core.encode("A")
        with self.assertRaisesRegex(ValueError, "does not match symbol_count"):
            self.core.decode(signal + b"\x00", pulse)
        with self.assertRaisesRegex(ValueError, "multiple of six"):
            self.core.decode(signal, pulse - 1)

    def test_registered_scheme_uses_its_encoder_and_decoder(self):
        self.core.register_scheme(
            "reverse", lambda text: (text[::-1].encode(), len(text)),
            lambda signal, _pulse: signal.decode()[::-1],
        )
        encoded, pulse = self.core.encode("AIVA", "reverse")
        self.assertEqual(encoded, b"AVIA")
        self.assertEqual(self.core.decode(encoded, pulse, "reverse"), "AIVA")


if __name__ == "__main__":
    unittest.main()
