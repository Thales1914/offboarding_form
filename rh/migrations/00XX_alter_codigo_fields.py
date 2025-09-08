from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("rh", "XXXX_last_migration"),  # ⚠️ Substitua pelo nome/ID da sua última migration
    ]

    operations = [
        migrations.AlterField(
            model_name="desligamento",
            name="codigo",
            field=models.CharField(
                "Código",
                max_length=20,
                db_index=True,   # só índice, sem unique
            ),
        ),
        migrations.AlterField(
            model_name="admissao",
            name="codigo",
            field=models.CharField(
                "Código RCA",
                max_length=20,
                db_index=True,   # só índice, sem unique
            ),
        ),
    ]
