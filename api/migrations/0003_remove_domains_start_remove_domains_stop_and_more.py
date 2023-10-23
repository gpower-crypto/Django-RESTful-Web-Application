# Generated by Django 4.2 on 2023-06-30 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_delete_pfam_id_domains_domain_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domains',
            name='start',
        ),
        migrations.RemoveField(
            model_name='domains',
            name='stop',
        ),
        migrations.CreateModel(
            name='domain_coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.IntegerField()),
                ('stop', models.IntegerField()),
                ('protein_domain_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.protein_domain_link')),
            ],
        ),
    ]