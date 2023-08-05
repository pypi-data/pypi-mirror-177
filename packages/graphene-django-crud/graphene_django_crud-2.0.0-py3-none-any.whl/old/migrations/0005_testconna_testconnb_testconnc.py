# Generated by Django 3.2.1 on 2021-05-11 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gdc_test', '0004_merge_20210510_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestConnA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=100, null=True)),
                ('nb', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestConnC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=100, null=True)),
                ('nb', models.IntegerField(blank=True, null=True)),
                ('test_conn_a', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_conn_cs', to='gdc_test.testconna')),
            ],
        ),
        migrations.CreateModel(
            name='TestConnB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=100, null=True)),
                ('nb', models.IntegerField(blank=True, null=True)),
                ('test_conn_a', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_conn_bs', to='gdc_test.testconna')),
            ],
        ),
    ]
