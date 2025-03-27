# Generated by Django 4.2.10 on 2025-03-26 19:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('bio', models.TextField(help_text='Professional summary')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'CV',
                'verbose_name_plural': 'CVs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('proficiency', models.CharField(choices=[('BEG', 'Beginner'), ('INT', 'Intermediate'), ('ADV', 'Advanced'), ('EXP', 'Expert')], default='INT', max_length=3)),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='main.cv')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('url', models.URLField(blank=True, validators=[django.core.validators.URLValidator()])),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='main.cv')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_type', models.CharField(choices=[('EMAIL', 'Email'), ('PHONE', 'Phone'), ('LINKEDIN', 'LinkedIn'), ('GITHUB', 'GitHub'), ('WEBSITE', 'Website'), ('OTHER', 'Other')], max_length=20)),
                ('value', models.CharField(max_length=255)),
                ('is_primary', models.BooleanField(default=False)),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='main.cv')),
            ],
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(fields=('cv', 'contact_type', 'is_primary'), name='unique_primary_contact_type'),
        ),
    ]
