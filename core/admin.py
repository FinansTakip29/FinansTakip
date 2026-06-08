from django.contrib import admin

from .models import (
    BirikimHedefi,
    ButceHedefi,
    FinansAlani,
    Gelir,
    Gider,
    Kategori,
    KategoriButcesi,
    OdemeDonemi,
    TekrarlayanOdeme,
)


@admin.register(FinansAlani)
class FinansAlaniAdmin(admin.ModelAdmin):
    list_display = ("ad", "kullanici", "renk", "ikon", "olusturulma_tarihi")
    list_filter = ("olusturulma_tarihi",)
    search_fields = ("ad", "kullanici__username", "kullanici__email")


@admin.register(Gelir)
class GelirAdmin(admin.ModelAdmin):
    list_display = ("aciklama", "kullanici", "kategori", "tutar", "tarih", "finans_alani")
    list_filter = ("tarih", "kategori")
    search_fields = ("aciklama", "kategori", "kullanici__username", "kullanici__email")


@admin.register(Gider)
class GiderAdmin(admin.ModelAdmin):
    list_display = ("aciklama", "kullanici", "kategori", "tutar", "tarih", "finans_alani")
    list_filter = ("tarih", "kategori")
    search_fields = ("aciklama", "kategori", "kullanici__username", "kullanici__email")


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ("ad", "tur", "kullanici", "finans_alani")
    list_filter = ("tur",)
    search_fields = ("ad", "kullanici__username", "kullanici__email")


@admin.register(ButceHedefi)
class ButceHedefiAdmin(admin.ModelAdmin):
    list_display = ("kullanici", "finans_alani", "ay", "yil", "hedef_tutar")
    list_filter = ("yil", "ay")
    search_fields = ("kullanici__username", "kullanici__email")


@admin.register(KategoriButcesi)
class KategoriButcesiAdmin(admin.ModelAdmin):
    list_display = ("kategori", "kullanici", "finans_alani", "ay", "yil", "hedef_tutar")
    list_filter = ("yil", "ay")
    search_fields = ("kategori__ad", "kullanici__username", "kullanici__email")


@admin.register(BirikimHedefi)
class BirikimHedefiAdmin(admin.ModelAdmin):
    list_display = ("hedef_adi", "kullanici", "finans_alani", "hedef_tutar", "mevcut_tutar", "aktif")
    list_filter = ("aktif",)
    search_fields = ("hedef_adi", "kullanici__username", "kullanici__email")


@admin.register(TekrarlayanOdeme)
class TekrarlayanOdemeAdmin(admin.ModelAdmin):
    list_display = ("odeme_adi", "kullanici", "finans_alani", "kategori", "tutar", "aktif", "odeme_durumu")
    list_filter = ("aktif", "odeme_durumu")
    search_fields = ("odeme_adi", "kullanici__username", "kullanici__email", "kategori__ad")


@admin.register(OdemeDonemi)
class OdemeDonemiAdmin(admin.ModelAdmin):
    list_display = ("tekrarlayan_odeme", "donem_ay", "donem_yil", "vade_tarihi", "durum")
    list_filter = ("durum", "donem_yil", "donem_ay")
    search_fields = ("tekrarlayan_odeme__odeme_adi", "tekrarlayan_odeme__kullanici__username")
