# Generated by Django 3.2.12 on 2022-03-03 02:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='category name')),
                ('description', models.CharField(blank=True, default='', max_length=500, verbose_name='category description')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county_coverage', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('AB', 'Alba'), ('AR', 'Arad'), ('AG', 'Argeș'), ('BC', 'Bacău'), ('BH', 'Bihor'), ('BN', 'Bistrița-Năsăud'), ('BT', 'Botoșani'), ('BV', 'Brașov'), ('BR', 'Brăila'), ('B', 'București'), ('BZ', 'Buzău'), ('CL', 'Călărași'), ('CS', 'Caraș-Severin'), ('CJ', 'Cluj'), ('CT', 'Constanța'), ('CV', 'Covasna'), ('DB', 'Dâmbovița'), ('DJ', 'Dolj'), ('GL', 'Galați'), ('GR', 'Giurgiu'), ('GJ', 'Gorj'), ('HR', 'Harghita'), ('HD', 'Hunedoara'), ('IL', 'Ialomița'), ('IS', 'Iași'), ('IF', 'Ilfov'), ('MM', 'Maramureș'), ('MH', 'Mehedinți'), ('MS', 'Mureș'), ('NT', 'Neamț'), ('OT', 'Olt'), ('PH', 'Prahova'), ('SM', 'Satu Mare'), ('SJ', 'Sălaj'), ('SB', 'Sibiu'), ('SV', 'Suceava'), ('TR', 'Teleorman'), ('TM', 'Timiș'), ('TL', 'Tulcea'), ('VS', 'Vaslui'), ('VL', 'Vâlcea'), ('VN', 'Vrancea')], max_length=124, null=True, verbose_name='county coverage')),
                ('town', models.CharField(blank=True, max_length=100, null=True, verbose_name='town')),
                ('description', models.CharField(blank=True, default='', max_length=500, verbose_name='description')),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='added on')),
                ('status', models.CharField(choices=[('NV', 'Not Verified'), ('V', 'Verified'), ('D', 'Deactivated'), ('C', 'Complete')], default='NV', max_length=5, verbose_name='status')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='resource name')),
                ('available_until', models.DateField(null=True, verbose_name='resource available until')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_other.category', verbose_name='category')),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='donor')),
            ],
            options={
                'verbose_name': 'other offer',
                'verbose_name_plural': 'other offer',
            },
        ),
        migrations.CreateModel(
            name='OtherRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county_coverage', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('AB', 'Alba'), ('AR', 'Arad'), ('AG', 'Argeș'), ('BC', 'Bacău'), ('BH', 'Bihor'), ('BN', 'Bistrița-Năsăud'), ('BT', 'Botoșani'), ('BV', 'Brașov'), ('BR', 'Brăila'), ('B', 'București'), ('BZ', 'Buzău'), ('CL', 'Călărași'), ('CS', 'Caraș-Severin'), ('CJ', 'Cluj'), ('CT', 'Constanța'), ('CV', 'Covasna'), ('DB', 'Dâmbovița'), ('DJ', 'Dolj'), ('GL', 'Galați'), ('GR', 'Giurgiu'), ('GJ', 'Gorj'), ('HR', 'Harghita'), ('HD', 'Hunedoara'), ('IL', 'Ialomița'), ('IS', 'Iași'), ('IF', 'Ilfov'), ('MM', 'Maramureș'), ('MH', 'Mehedinți'), ('MS', 'Mureș'), ('NT', 'Neamț'), ('OT', 'Olt'), ('PH', 'Prahova'), ('SM', 'Satu Mare'), ('SJ', 'Sălaj'), ('SB', 'Sibiu'), ('SV', 'Suceava'), ('TR', 'Teleorman'), ('TM', 'Timiș'), ('TL', 'Tulcea'), ('VS', 'Vaslui'), ('VL', 'Vâlcea'), ('VN', 'Vrancea')], max_length=124, null=True, verbose_name='county coverage')),
                ('town', models.CharField(blank=True, max_length=100, null=True, verbose_name='town')),
                ('description', models.CharField(blank=True, default='', max_length=500, verbose_name='description')),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='added on')),
                ('status', models.CharField(choices=[('NV', 'Not Verified'), ('V', 'Verified'), ('D', 'Deactivated'), ('C', 'Complete')], default='NV', max_length=5, verbose_name='status')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_other.category', verbose_name='category')),
                ('made_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='requested by')),
            ],
            options={
                'verbose_name': 'other request',
                'verbose_name_plural': 'other requests',
            },
        ),
        migrations.CreateModel(
            name='ResourceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_other.otherrequest', verbose_name='request')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_other.otheroffer', verbose_name='donation')),
            ],
            options={
                'verbose_name': 'Offer - Request',
                'verbose_name_plural': 'Offer - Request',
            },
        ),
    ]
