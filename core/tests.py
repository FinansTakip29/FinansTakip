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
