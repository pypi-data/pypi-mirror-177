# Generated by Django 4.0.2 on 2022-03-03 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("spid_cie_oidc_relying_party", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="oidcauthentication",
            old_name="issuer",
            new_name="provider",
        ),
        migrations.RenameField(
            model_name="oidcauthentication",
            old_name="issuer_id",
            new_name="provider_id",
        ),
    ]
