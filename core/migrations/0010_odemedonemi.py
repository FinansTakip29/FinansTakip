from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_tekrarlayanodeme_odeme_durumu"),
    ]

    operations = [
        migrations.CreateModel(
            name="OdemeDonemi",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("donem_yil", models.PositiveIntegerField()),
                ("donem_ay", models.PositiveSmallIntegerField()),
                ("vade_tarihi", models.DateField()),
                (
                    "durum",
                    models.CharField(
                        choices=[
                            ("bekliyor", "Bekliyor"),
                            ("odendi", "Ödendi"),
                            ("gecikti", "Gecikti"),
                            ("iptal", "İptal Edildi"),
                        ],
                        default="bekliyor",
                        max_length=20,
                    ),
                ),
                (
                    "tekrarlayan_odeme",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.tekrarlayanodeme"),
                ),
            ],
            options={
                "unique_together": {("tekrarlayan_odeme", "donem_yil", "donem_ay")},
            },
        ),
    ]
