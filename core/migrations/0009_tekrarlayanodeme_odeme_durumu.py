from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_fix_tekrarlayanodeme_tekrar_alanlari"),
    ]

    operations = [
        migrations.AddField(
            model_name="tekrarlayanodeme",
            name="odeme_durumu",
            field=models.CharField(
                choices=[
                    ("bekliyor", "Bekliyor"),
                    ("odendi", "Ödendi"),
                    ("gecikti", "Gecikti"),
                    ("iptal", "İptal edildi"),
                ],
                default="bekliyor",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="tekrarlayanodeme",
            name="son_gider",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.gider",
            ),
        ),
    ]
