from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Timezone",
            fields=[
                (
                    "tz",
                    models.CharField(
                        max_length=200,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Timezone",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkDay",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("openfrom", models.TimeField(verbose_name="Open from")),
                ("closedafter", models.TimeField(verbose_name="Closed after")),
                (
                    "dayofweek",
                    models.CharField(
                        choices=[
                            ("monday", "Monday"),
                            ("tuesday", "Tuesday"),
                            ("wednesday", "Wednesday"),
                            ("thursday", "Thursday"),
                            ("friday", "Friday"),
                            ("saturday", "Saturday"),
                            ("sunday", "Sunday"),
                        ],
                        max_length=20,
                        verbose_name="Day of the week",
                    ),
                ),
            ],
        ),
    ]
