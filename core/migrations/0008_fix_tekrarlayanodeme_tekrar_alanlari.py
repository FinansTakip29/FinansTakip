from django.db import migrations


def eksik_tekrar_alanlarini_ekle(apps, schema_editor):
    tablo_adi = "core_tekrarlayanodeme"
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        mevcut_tablolar = connection.introspection.table_names(cursor)
        if tablo_adi not in mevcut_tablolar:
            return

        mevcut_kolonlar = {
            kolon.name
            for kolon in connection.introspection.get_table_description(cursor, tablo_adi)
        }

        if "tekrar_turu" not in mevcut_kolonlar:
            cursor.execute(
                f"ALTER TABLE {tablo_adi} "
                "ADD COLUMN tekrar_turu varchar(20) NOT NULL DEFAULT 'aylik'"
            )

        if "tekrar_araligi" not in mevcut_kolonlar:
            cursor.execute(
                f"ALTER TABLE {tablo_adi} "
                "ADD COLUMN tekrar_araligi integer NOT NULL DEFAULT 1"
            )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_tekrarlayanodeme"),
    ]

    operations = [
        migrations.RunPython(
            eksik_tekrar_alanlarini_ekle,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
