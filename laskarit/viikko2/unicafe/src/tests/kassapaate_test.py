import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_alussa_0_edullista_lounasta_myytynä(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_alussa_0_maukasta_lounasta_myytynä(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_edullisen_osto_kateisella_toimii_jos_maksu_riittava(self):
        self.kassapaate.syo_edullisesti_kateisella(300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_maukkaan_osto_kateisella_toimii_jos_maksu_riittava(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_syo_edullisesti_kateisella_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)

    def test_syo_maukkaasti_kateisella_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

    def test_syo_edullisesti_kateisella_kasvattaa_myytyja_lounaita(self):
        self.kassapaate.syo_edullisesti_kateisella(300)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_maukkaasti_kateisella_kasvattaa_myytyja_lounaita(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_saldo_ei_muutu_jos_kateismaksu_ei_riita_edulliseen(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_saldo_ei_muutu_jos_kateismaksu_ei_riita_maukkaaseen(self):
        self.kassapaate.syo_maukkaasti_kateisella(350)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kaikki_rahat_palautetaan_jos_maksu_ei_riita_edulliseen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)

    def test_kaikki_rahat_palautetaan_jos_maksu_ei_riita_maukkaaseen(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(350), 350)

    def test_myytyjen_edullisten_maara_ei_muutu_jos_kateismaksu_ei_riittava(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_myytyjen_maukkaiden_maara_ei_muutu_jos_kateismaksu_ei_riittava(self):
        self.kassapaate.syo_maukkaasti_kateisella(350)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kortilla_veloittaa_summan_oikein(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 760)

    def test_syo_maukkaasti_kortilla_veloittaa_summan_oikein(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 600)

    def test_edullinen_korttiosto_true_jos_tarpeeksi_saldoa(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)

    def test_maukas_korttiosto_true_jos_tarpeeksi_saldoa(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)

    def test_syo_edullisesti_kortilla_kasvattaa_myytyja_lounaita(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_maukkaasti_kortilla_kasvattaa_myytyja_lounaita(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kortin_saldo_ei_muutu_jos_ei_riita_edulliseen(self):
        kortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 200)

    def test_kortin_saldo_ei_muutu_jos_ei_riita_maukkaaseen(self):
        kortti = Maksukortti(350)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 350)

    def test_lounaiden_maara_ei_muutu_jos_kortin_saldo_ei_riita_edulliseen(self):
        kortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_lounaiden_maara_ei_muutu_jos_kortin_saldo_ei_riita_maukkaaseen(self):
        kortti = Maksukortti(350)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_edullisesti_kortilla_false_jos_ei_tarpeeksi_saldoa(self):
        kortti = Maksukortti(200)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), False)

    def test_syo_maukkaasti_kortilla_false_jos_ei_tarpeeksi_saldoa(self):
        kortti = Maksukortti(350)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), False)

    def test_syo_edullisesti_kortilla_ei_muuta_kassan_saldoa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_syo_maukkaasti_kortilla_ei_muuta_kassan_saldoa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kortille_rahan_lataaminen_muuttaa_saldoa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)
        self.assertEqual(self.maksukortti.saldo, 1500)

    def test_negatiivinen_lataus_kortille_ei_muuta_saldoa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -200)
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_kortille_lataaminen_kasvattaa_kassan_saldoa_oikein(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)


    



    
