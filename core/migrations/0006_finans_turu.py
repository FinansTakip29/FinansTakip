from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_kategori'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='butcehedefi',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='kategori',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='butcehedefi',
            name='finans_turu',
            field=models.CharField(choices=[('kisisel', 'Kişisel Finans'), ('ev', 'Ev Finans'), ('isyeri', 'İşyeri Finans')], default='kisisel', max_length=20),
        ),
        migrations.AddField(
            model_name='gelir',
            name='finans_turu',
            field=models.CharField(choices=[('kisisel', 'Kişisel Finans'), ('ev', 'Ev Finans'), ('isyeri', 'İşyeri Finans')], default='kisisel', max_length=20),
        ),
        migrations.AddField(
            model_name='gider',
            name='finans_turu',
            field=models.CharField(choices=[('kisisel', 'Kişisel Finans'), ('ev', 'Ev Finans'), ('isyeri', 'İşyeri Finans')], default='kisisel', max_length=20),
        ),
        migrations.AddField(
            model_name='kategori',
            name='finans_turu',
            field=models.CharField(choices=[('kisisel', 'Kişisel Finans'), ('ev', 'Ev Finans'), ('isyeri', 'İşyeri Finans')], default='kisisel', max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='butcehedefi',
            unique_together={('kullanici', 'finans_turu', 'yil', 'ay')},
        ),
        migrations.AlterUniqueTogether(
            name='kategori',
            unique_together={('kullanici', 'finans_turu', 'ad', 'tur')},
        ),
    ]
