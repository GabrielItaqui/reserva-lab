import os
import gspread
from typing import List
from django.conf import settings
from datetime import datetime


def initialize_gspread() -> gspread.client.Client:
    """
    Initialize a gspread client with the given credentials.
    """
    return gspread.service_account_from_dict(
        get_credentials()
    )  # Note: we could move this to settings to do this once.


def get_credentials() -> dict:
    """
    Return gspread credentials.
    """
    return {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        # Substitua '\n' por quebras de linha reais
        "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
    }


def get_all_rows(doc_name: str, sheet_name: str = None) -> List[dict]:
    sh = settings.GSPREAD_CLIENT.open(doc_name)
    worksheet = sh.worksheet(sheet_name) if sheet_name else sh.get_worksheet(0)
    rows = worksheet.get_all_records()

    # Converta a data de string para datetime e ordene
    for row in rows:
        row["data"] = datetime.strptime(
            row["data"], "%Y-%m-%d"  # Ajuste o formato aqui
        )

    # Ordene as reservas pela data
    sorted_rows = sorted(rows, key=lambda x: x["data"])

    return sorted_rows
