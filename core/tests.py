import json
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import FinansAlani, Gelir, Gider, Kategori


class YedeklemeRegressionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="backup_user",
            email="backup@example.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="backup_other_user",
            email="backup-other@example.com",
            password="StrongPass123!",
        )
        self.client.defaults["HTTP_HOST"] = "localhost"
        self.client.force_login(self.user)
        self.kisisel_alan = FinansAlani.objects.create(
            kullanici=self.user,
            ad="Kişisel Finans",
            aciklama="Varsayılan finans alanı",
            renk="#2563eb",
            ikon="wallet2",
        )
        self.other_kisisel_alan = FinansAlani.objects.create(
            kullanici=self.other_user,
            ad="Kişisel Finans",
            aciklama="Varsayılan finans alanı",
            renk="#2563eb",
            ikon="wallet2",
        )

    def test_aktif_alan_kisisel_yedekleme_sayfasi_200(self):
        response = self.client.get(reverse("yedekleme"), {"finans_turu": "kisisel"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yedekleme")

    def test_kisisel_alan_bosken_yedekleme_sayfasi_200(self):
        response = self.client.get(reverse("yedekleme"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gelirler")

    def test_kisisel_alanda_veri_varken_yedekleme_json_dogru_verileri_doner(self):
        alan = self.kisisel_alan
        Kategori.objects.create(
            kullanici=self.user,
            finans_turu=str(alan.id),
            finans_alani=alan,
            ad="Maaş",
            tur=Kategori.GELIR,
        )
        Gelir.objects.create(
            kullanici=self.user,
            finans_turu=str(alan.id),
            finans_alani=alan,
            tarih=date(2026, 8, 31),
            aciklama="Ağustos maaşı",
            tutar=Decimal("25000.00"),
            kategori="Maaş",
        )

        response = self.client.get(reverse("yedekleme_json"))
        payload = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(payload["gelirler"]), 1)
        self.assertEqual(payload["gelirler"][0]["aciklama"], "Ağustos maaşı")
        self.assertEqual(payload["meta"]["username"], self.user.username)

    def test_baska_finans_alani_yedekleme_sayfasi_200(self):
        alan = FinansAlani.objects.create(
            kullanici=self.user,
            ad="Ev",
            aciklama="Ev bütçesi",
            renk="#16a34a",
            ikon="house",
        )

        response = self.client.get(reverse("yedekleme"), {"finans_turu": str(alan.id)})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yedekleme")

    def test_gecersiz_alan_degeri_500_vermez(self):
        response = self.client.get(reverse("yedekleme"), {"finans_turu": "gecersiz-alan"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yedekleme")

    def test_kullanici_izolasyonu_korunur(self):
        kendi_alan = self.kisisel_alan
        diger_alan = self.other_kisisel_alan
        Gelir.objects.create(
            kullanici=self.user,
            finans_turu=str(kendi_alan.id),
            finans_alani=kendi_alan,
            tarih=date(2026, 8, 31),
            aciklama="Kendi gelir",
            tutar=Decimal("100.00"),
            kategori="Test",
        )
        Gider.objects.create(
            kullanici=self.other_user,
            finans_turu=str(diger_alan.id),
            finans_alani=diger_alan,
            tarih=date(2026, 8, 31),
            aciklama="Başka kullanıcı gider",
            tutar=Decimal("999.00"),
            kategori="Test",
        )

        response = self.client.get(reverse("yedekleme_json"))
        payload = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(payload["gelirler"]), 1)
        self.assertEqual(len(payload["giderler"]), 0)
        self.assertEqual(payload["gelirler"][0]["aciklama"], "Kendi gelir")


class TopluKategoriEklemeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bulk_category_user",
            email="bulk-category@example.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="bulk_category_other",
            email="bulk-category-other@example.com",
            password="StrongPass123!",
        )
        self.kisisel_alan = FinansAlani.objects.create(
            kullanici=self.user,
            ad="Kişisel Finans",
            aciklama="Varsayılan finans alanı",
            renk="#2563eb",
            ikon="wallet2",
        )
        self.ev_alani = FinansAlani.objects.create(
            kullanici=self.user,
            ad="Ev",
            aciklama="Ev bütçesi",
            renk="#16a34a",
            ikon="house",
        )
        self.diger_alan = FinansAlani.objects.create(
            kullanici=self.other_user,
            ad="Kişisel Finans",
            aciklama="Varsayılan finans alanı",
            renk="#2563eb",
            ikon="wallet2",
        )
        self.client.defaults["HTTP_HOST"] = "localhost"
        self.client.force_login(self.user)

    def _toplu_ekle(self, alan, tur, metin):
        return self.client.post(reverse("kategoriler"), {
            "islem": "toplu_kategori_ekle",
            "finans_turu": str(alan.id),
            "toplu_tur": tur,
            "kategori_adlari": metin,
        })

    def test_birden_fazla_kategori_ekler(self):
        response = self._toplu_ekle(self.kisisel_alan, Kategori.GIDER, "Market\nAkaryakıt\nElektrik")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Kategori.objects.filter(kullanici=self.user, finans_turu=str(self.kisisel_alan.id), tur=Kategori.GIDER).count(),
            3,
        )

    def test_bos_satirlari_atlar(self):
        self._toplu_ekle(self.kisisel_alan, Kategori.GIDER, "\nMarket\n\n  \nSu\n")

        adlar = set(Kategori.objects.filter(kullanici=self.user).values_list("ad", flat=True))
        self.assertEqual(adlar, {"Market", "Su"})

    def test_ayni_giris_icerisindeki_tekrar_eden_isimleri_atlar(self):
        self._toplu_ekle(self.kisisel_alan, Kategori.GIDER, "Market\n market \nMARKET\nAkaryakıt")

        self.assertEqual(Kategori.objects.filter(kullanici=self.user).count(), 2)
        self.assertTrue(Kategori.objects.filter(kullanici=self.user, ad="Market").exists())
        self.assertTrue(Kategori.objects.filter(kullanici=self.user, ad="Akaryakıt").exists())

    def test_mevcut_kategoriyi_tekrar_olusturmaz(self):
        Kategori.objects.create(
            kullanici=self.user,
            finans_turu=str(self.kisisel_alan.id),
            finans_alani=self.kisisel_alan,
            ad="Market",
            tur=Kategori.GIDER,
        )

        self._toplu_ekle(self.kisisel_alan, Kategori.GIDER, "market\nElektrik")

        self.assertEqual(
            Kategori.objects.filter(kullanici=self.user, finans_turu=str(self.kisisel_alan.id), tur=Kategori.GIDER).count(),
            2,
        )
        self.assertEqual(Kategori.objects.filter(kullanici=self.user, ad__iexact="market").count(), 1)

    def test_gelir_gider_turu_dogru_kaydedilir(self):
        self._toplu_ekle(self.kisisel_alan, Kategori.GELIR, "Maaş\nPrim")

        self.assertEqual(Kategori.objects.filter(kullanici=self.user, tur=Kategori.GELIR).count(), 2)
        self.assertFalse(Kategori.objects.filter(kullanici=self.user, tur=Kategori.GIDER).exists())

    def test_kullanici_izolasyonu_korunur(self):
        Kategori.objects.create(
            kullanici=self.other_user,
            finans_turu=str(self.diger_alan.id),
            finans_alani=self.diger_alan,
            ad="Market",
            tur=Kategori.GIDER,
        )

        self._toplu_ekle(self.kisisel_alan, Kategori.GIDER, "Market")

        self.assertEqual(Kategori.objects.filter(kullanici=self.user, ad="Market").count(), 1)
        self.assertEqual(Kategori.objects.filter(kullanici=self.other_user, ad="Market").count(), 1)

    def test_finans_alani_izolasyonu_korunur(self):
        Kategori.objects.create(
            kullanici=self.user,
            finans_turu=str(self.ev_alani.id),
            finans_alani=self.ev_alani,
            ad="Market",
            tur=Kategori.GIDER,
        )

        self._toplu_ekle(self.kisisel_alan, Kategori.GIDER, "Market")

        self.assertEqual(Kategori.objects.filter(kullanici=self.user, ad="Market").count(), 2)
        self.assertEqual(Kategori.objects.filter(kullanici=self.user, finans_turu=str(self.kisisel_alan.id)).count(), 1)
        self.assertEqual(Kategori.objects.filter(kullanici=self.user, finans_turu=str(self.ev_alani.id)).count(), 1)
