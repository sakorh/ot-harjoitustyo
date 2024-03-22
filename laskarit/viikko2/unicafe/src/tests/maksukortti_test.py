import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(2500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 35.0)

    def test_saldo_vahenee_oikein_jos_tarpeeksi_rahaa(self):
        self.maksukortti.ota_rahaa(200)
        self.assertEqual(self.maksukortti.saldo_euroina(), 8.0)

    def test_saldo_ei_muutu_jos_liian_vahan_rahaa(self):
        self.maksukortti.ota_rahaa(1100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_rahan_ottaminen_palauttaa_true_jos_tarpeeksi_saldoa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(200), True)

    def test_rahan_ottaminen_palauttaa_false_jos_liian_vahan_rahaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1100), False)

