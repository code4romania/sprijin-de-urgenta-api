from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.utils import timezone
import pandas as pd
from io import BytesIO

from app_item.models import ItemOffer, ItemRequest


class Command(BaseCommand):
    help = "Dumps Models into Excel and sends email with xlsx as attachement"

    def add_arguments(self, parser):
        parser.add_argument(
            "emails",
            nargs="+",
            help="email addresses to send email to. space separated",
        )

    def handle(self, *args, **kwargs):

        email_addresses = kwargs["emails"]
        now = timezone.now()
        hours_ago_24 = now - timezone.timedelta(hours=24)

        item_offer_data_mapping = {
            "county_coverage": "Judete Acoperite",
            "town": "Oras",
            "description": "Descriere",
            "added_on": "Adaugat in",
            "status": "Stare",
            "donor__username": "Donator",
            "category__name": "Categorie",
            "name": "Nume",
            "quantity": "Cantitate",
            "packaging_type": "Ambalaj",
            "unit_type": "UM",
            "expiration_date": "Data de Expirare",
            "stock": "Stoc",
            "textile_category__name": "Categorie Textile",
            "kids_age": "Varsta Copii",
            "other_textiles": "Alte Textile",
            "tent_capacity": "Capacitate Cort",
        }

        item_request_data_mapping = {
            "county_coverage": "Judete Acoperite",
            "town": "Oras",
            "description": "Descriere",
            "added_on": "Adaugat in",
            "status": "Stare",
            "made_by__username": "Oferit de",
            "category__name": "Categorie",
            "name": "Nume",
            "quantity": "Cantitate",
            "packaging_type": "Ambalaj",
            "unit_type": "UM",
            "stock": "Stoc",
            "textile_category__name": "Categorie Textile",
            "kids_age": "Varsta Copii",
            "other_textiles": "Alte Textile",
            "tent_capacity": "Capacitate Cort",
        }

        item_offers = self.get_dataframe_with_objects(hours_ago_24, ItemOffer, item_offer_data_mapping)
        item_requests = self.get_dataframe_with_objects(hours_ago_24, ItemRequest, item_request_data_mapping)

        data = [
            (item_offers, "Donatii Produse"),
            (item_requests, "Cereri Produse"),
        ]

        bio = BytesIO()

        writer = pd.ExcelWriter(bio, engine="xlsxwriter")

        for df, sheet in data:
            if df.size == 0:
                continue
            df["Judete Acoperite"] = df["Judete Acoperite"].agg(lambda x: ", ".join(map(str, x)))
            df["Adaugat in"] = df["Adaugat in"].dt.tz_localize(None)

            df.to_excel(writer, sheet_name=sheet, index=False)

        writer.save()
        bio.seek(0)

        email = EmailMessage(
            subject="Raport zilnic situatie management resurse",
            from_email=settings.FROM_EMAIL,
            body=(
                "Situatia centralizata a datelor din sistemul integrat de management de "
                f"resurse si voluntari sprijindeurgenta.ro pentru intevalul {hours_ago_24.strftime('%c')} - {now.strftime('%c')}"
            ),
            to=email_addresses,
        )
        email.attach(
            "situatia_zilnica_sdu.xlsx",
            bio.getvalue(),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        email.send()

    @staticmethod
    def get_dataframe_with_objects(hours_ago_24, object_model, data_mapping):
        item_data = object_model.objects.filter(added_on__gte=hours_ago_24).values(*data_mapping.keys())
        item_data = item_data if len(item_data) > 0 else pd.np.empty((0, len(data_mapping.keys())))
        items = pd.DataFrame(item_data)
        items.columns = list(data_mapping.values())
        return items
