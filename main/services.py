import os
import gspread
from typing import List
from django.conf import settings
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_credentials() -> dict:
    """
    Return gspread credentials.
    """
    return {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
    }

def initialize_gspread():
    """
    Inicializa e retorna o cliente gspread.
    """
    return gspread.service_account_from_dict(get_credentials())

GSPREAD_CLIENT = initialize_gspread()

def get_all_rows(doc_name: str, sheet_name: str = None) -> List[dict]:
    sh = GSPREAD_CLIENT.open(doc_name)
    worksheet = sh.worksheet(sheet_name) if sheet_name else sh.get_worksheet(0)
    rows = worksheet.get_all_records()

    for row in rows:
        row["data"] = datetime.strptime(row["data"], "%Y-%m-%d")

    sorted_rows = sorted(rows, key=lambda x: x["data"])

    return sorted_rows