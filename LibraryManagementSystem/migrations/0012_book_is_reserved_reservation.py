# Generated by Django 5.1.1 on 2024-10-02 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryManagementSystem', '0011_rename_closing_times_libraryhours_closing_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('a', 'a'), ('y', 'c')], max_length=1)),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='LibraryManagementSystem.book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LibraryManagementSystem.member')),
            ],
        ),
    ]
