# Generated by Django 4.0.2 on 2022-03-02 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=48, primary_key=True, serialize=False, unique=True)),
                ('password', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('dateofcompletion', models.CharField(max_length=100)),
                ('status', models.CharField(default='NEW', max_length=20)),
                ('dateofcreation', models.DateTimeField(auto_now_add=True)),
                ('dateofmodification', models.DateTimeField(auto_now=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='todoapi.user')),
            ],
        ),
    ]
