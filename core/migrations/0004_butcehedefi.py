from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_gelir_kullanici_gider_kullanici'),
    ]

    operations = [
        migrations.CreateModel(
            name='ButceHedefi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yil', models.PositiveIntegerField()),
                ('ay', models.PositiveSmallIntegerField()),
                ('hedef_tutar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('kullanici', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('kullanici', 'yil', 'ay')},
            },
        ),
    ]
