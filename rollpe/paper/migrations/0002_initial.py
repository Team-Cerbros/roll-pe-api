# Generated by Django 5.1.4 on 2025-01-18 11:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paper', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='hostFK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='paper_host', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paper',
            name='invitingUser',
            field=models.ManyToManyField(blank=True, related_name='inviting_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paper',
            name='receiverFK',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='paper_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paper',
            name='ratioFK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='paper_ratio', to='paper.queryindextable'),
        ),
        migrations.AddField(
            model_name='paper',
            name='sizeFk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='paper_size', to='paper.queryindextable'),
        ),
        migrations.AddField(
            model_name='paper',
            name='themeFK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='paper_theme', to='paper.queryindextable'),
        ),
    ]
