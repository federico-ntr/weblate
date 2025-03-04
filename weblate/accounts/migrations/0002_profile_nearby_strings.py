# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Generated by Django 3.0.7 on 2020-06-22 13:41

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_squashed_0019_auto_20200403_2004"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="nearby_strings",
            field=models.SmallIntegerField(
                default=settings.NEARBY_MESSAGES,
                help_text="Number of nearby strings to show in each direction in the full editor.",
                verbose_name="Number of nearby strings",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(50),
                ],
            ),
        ),
    ]
