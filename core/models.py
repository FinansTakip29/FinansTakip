from django.conf import settings
from django.db import models


FINANS_KISISEL = "kisisel"
FINANS_EV = "ev"
FINANS_ISYERI = "isyeri"

FINANS_TURU_SECENEKLERI = [
    (FINANS_KISISEL, "Kişisel Finans"),
    (FINANS_EV, "Ev Finans"),
    (FINANS_ISYERI, "İşyeri Finans"),
]


class FinansAlani(models.Model):
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.CharField(max_length=100)
    aciklama = models.TextField(blank=True)
    renk = models.CharField(max_length=20, default="#2563eb")
    ikon = models.CharField(max_length=50, default="wallet2")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("kullanici", "ad")
        ordering = ("ad",)

    def __str__(self):
        return self.ad


def _finans_turu_alan(instance):
    if not instance.finans_alani_id and instance.kullanici_id and instance.finans_turu:
        instance.finans_alani = FinansAlani.objects.filter(
            kullanici_id=instance.kullanici_id,
            id=instance.finans_turu,
        ).first()
    if instance.finans_alani_id:
        return str(instance.finans_alani_id)
    return instance.finans_turu or FINANS_KISISEL


class Gelir(models.Model):
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    finans_turu = models.CharField(max_length=64, default=FINANS_KISISEL)
    finans_alani = models.ForeignKey(FinansAlani, on_delete=models.SET_NULL, null=True, blank=True)
    tarih = models.DateField()
    aciklama = models.CharField(max_length=200)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.finans_turu = _finans_turu_alan(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.aciklama} - {self.tutar} TL"


class Gider(models.Model):
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    finans_turu = models.CharField(max_length=64, default=FINANS_KISISEL)
    finans_alani = models.ForeignKey(FinansAlani, on_delete=models.SET_NULL, null=True, blank=True)
    tarih = models.DateField()
    aciklama = models.CharField(max_length=200)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.finans_turu = _finans_turu_alan(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.aciklama


class ButceHedefi(models.Model):
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finans_turu = models.CharField(max_length=64, default=FINANS_KISISEL)
    finans_alani = models.ForeignKey(FinansAlani, on_delete=models.SET_NULL, null=True, blank=True)
    yil = models.PositiveIntegerField()
    ay = models.PositiveSmallIntegerField()
    hedef_tutar = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("kullanici", "finans_turu", "yil", "ay")

    def save(self, *args, **kwargs):
        self.finans_turu = _finans_turu_alan(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kullanici.username} - {self.ay}/{self.yil}: {self.hedef_tutar} TL"


class KategoriButcesi(models.Model):
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finans_turu = models.CharField(max_length=64, default=FINANS_KISISEL)
    finans_alani = models.ForeignKey(FinansAlani, on_delete=models.SET_NULL, null=True, blank=True)
    kategori = models.ForeignKey("Kategori", on_delete=models.CASCADE)
    yil = models.PositiveIntegerField()
    ay = models.PositiveSmallIntegerField()
    hedef_tutar = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("kullanici", "finans_turu", "kategori", "yil", "ay")

    def save(self, *args, **kwargs):
        self.finans_turu = _finans_turu_alan(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kategori.ad} - {self.ay}/{self.yil}: {self.hedef_tutar} TL"


class BirikimHedefi(models.Model):
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finans_turu = models.CharField(max_length=64, default=FINANS_KISISEL)
    finans_alani = models.ForeignKey(FinansAlani, on_delete=models.SET_NULL, null=True, blank=True)
    hedef_adi = models.CharField(max_length=120)
    hedef_tutar = models.DecimalField(max_digits=12, decimal_places=2)
    mevcut_tutar = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aylik_katki = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hedef_tarihi = models.DateField(null=True, blank=True)
    aktif = models.BooleanField(default=True)
    aciklama = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.finans_turu = _finans_turu_alan(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.hedef_adi} - {self.mevcut_tutar}/{self.hedef_tutar} TL"


class Kategori(models.Model):
    GELIR = "gelir"
    GIDER = "gider"

    TUR_SECENEKLERI = [
        (GELIR, "Gelir"),
        (GIDER, "Gider"),
    ]

    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finans_turu = models.CharField(max_length=64, default=FINANS_KISISEL)
    finans_alani = models.ForeignKey(FinansAlani, on_delete=models.SET_NULL, null=True, blank=True)
    ad = models.CharField(max_length=100)
    tur = models.CharField(max_length=10, choices=TUR_SECENEKLERI)

    class Meta:
        unique_together = ("kullanici", "finans_turu", "ad", "tur")

    def save(self, *args, **kwargs):
        self.finans_turu = _finans_turu_alan(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ad} ({self.get_tur_display()})"


class TekrarlayanOdeme(models.Model):
    BEKLIYOR = "bekliyor"
    ODENDI = "odendi"
    GECIKTI = "gecikti"
    IPTAL = "iptal"

    ODEME_DURUMU_SECENEKLERI = [
        (BEKLIYOR, "Bekliyor"),
        (ODENDI, "Ödendi"),
        (GECIKTI, "Gecikti"),
        (IPTAL, "İptal edildi"),
    ]

    GUNLUK = "gunluk"
    HAFTALIK = "haftalik"
    AYLIK = "aylik"
    YILLIK = "yillik"
    OZEL = "ozel"

    TEKRAR_TURU_SECENEKLERI = [
        (GUNLUK, "Günlük"),
        (HAFTALIK, "Haftalık"),
        (AYLIK, "Aylık"),
        (YILLIK, "Yıllık"),
        (OZEL, "Özel"),
    ]

    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finans_turu = models.CharField(max_length=64, default=FINANS_KISISEL)
    finans_alani = models.ForeignKey(FinansAlani, on_delete=models.SET_NULL, null=True, blank=True)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    odeme_adi = models.CharField(max_length=100)
    aciklama = models.CharField(max_length=200, blank=True)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    baslangic_tarihi = models.DateField()
    tekrar_turu = models.CharField(max_length=20, choices=TEKRAR_TURU_SECENEKLERI, default=AYLIK)
    tekrar_araligi = models.PositiveIntegerField(default=1)
    aktif = models.BooleanField(default=True)
    odeme_durumu = models.CharField(max_length=20, choices=ODEME_DURUMU_SECENEKLERI, default=BEKLIYOR)
    son_olusturma_tarihi = models.DateField(null=True, blank=True)
    son_gider = models.ForeignKey(Gider, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.finans_turu = _finans_turu_alan(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.odeme_adi} - {self.tutar} TL"


class OdemeDonemi(models.Model):
    BEKLIYOR = "bekliyor"
    ODENDI = "odendi"
    GECIKTI = "gecikti"
    IPTAL = "iptal"

    DURUM_SECENEKLERI = [
        (BEKLIYOR, "Bekliyor"),
        (ODENDI, "Ödendi"),
        (GECIKTI, "Gecikti"),
        (IPTAL, "İptal Edildi"),
    ]

    tekrarlayan_odeme = models.ForeignKey(TekrarlayanOdeme, on_delete=models.CASCADE)
    donem_yil = models.PositiveIntegerField()
    donem_ay = models.PositiveSmallIntegerField()
    vade_tarihi = models.DateField()
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default=BEKLIYOR)

    class Meta:
        unique_together = ("tekrarlayan_odeme", "donem_yil", "donem_ay")

    def __str__(self):
        return f"{self.tekrarlayan_odeme.odeme_adi} - {self.donem_ay}/{self.donem_yil}"
