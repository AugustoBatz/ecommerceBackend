# Generated by Django 3.1.1 on 2020-09-14 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('category', models.CharField(max_length=25)),
                ('brand', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('color_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.color')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('detail_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productdetail')),
            ],
        ),
        migrations.AddField(
            model_name='productdetail',
            name='size_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.size'),
        ),
    ]
