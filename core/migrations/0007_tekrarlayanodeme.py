from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_finans_turu'),
    ]

    operations = [
        migrations.CreateModel(
            name='TekrarlayanOdeme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finans_turu', models.CharField(choices=[('kisisel', 'Kişisel Finans'), ('ev', 'Ev Finans'), ('isyeri', 'İşyeri Finans')], default='kisisel', max_length=20)),
                ('odeme_adi', models.CharField(max_length=100)),
                ('aciklama', models.CharField(blank=True, max_length=200)),
                ('tutar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('baslangic_tarihi', models.DateField()),
                ('tekrar_turu', models.CharField(choices=[('gunluk', 'Günlük'), ('haftalik', 'Haftalık'), ('aylik', 'Aylık'), ('yillik', 'Yıllık'), ('ozel', 'Özel')], default='aylik', max_length=20)),
                ('tekrar_araligi', models.PositiveIntegerField(default=1)),
                ('aktif', models.BooleanField(default=True)),
                ('son_olusturma_tarihi', models.DateField(blank=True, null=True)),
                ('kategori', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.kategori')),
                ('kullanici', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
