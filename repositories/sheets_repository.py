"""
sheets_repository.py

Google Sheets repository using the official Google Sheets API.
"""

from __future__ import annotations

from typing import List

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from domain.account import Account
from domain.transaction import Transaction


class SheetsRepository:

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    def __init__(
        self,
        credentials_file: str,
        spreadsheet_id: str,
    ):

        credentials = Credentials.from_service_account_file(
            credentials_file,
            scopes=self.SCOPES,
        )

        service = build(
            "sheets",
            "v4",
            credentials=credentials,
        )

        self.sheet = service.spreadsheets()
        self.spreadsheet_id = spreadsheet_id

    # ----------------------------------------
    # Generic
    # ----------------------------------------

    def _read(self, worksheet: str):

        result = (
            self.sheet.values()
            .get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{worksheet}!A:ZZ",
            )
            .execute()
        )

        values = result.get("values", [])

        if not values:
            return []

        headers = values[0]

        return [
            dict(zip(headers, row))
            for row in values[1:]
        ]

    def _write(
        self,
        worksheet: str,
        rows: list[dict],
    ):

        if not rows:
            return

        headers = list(rows[0].keys())

        values = [headers]

        for row in rows:
            values.append(
                [row.get(column, "") for column in headers]
            )

        body = {
            "values": values
        }

        self.sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f"{worksheet}!A1",
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()

    # ----------------------------------------
    # Accounts
    # ----------------------------------------

    def load_accounts(self) -> List[Account]:

        rows = self._read("Accounts")

        return [
            Account.from_dict(row)
            for row in rows
        ]

    def save_accounts(
        self,
        accounts: List[Account],
    ):

        rows = [
            account.to_dict()
            for account in accounts
        ]

        self._write(
            "Accounts",
            rows,
        )

    # ----------------------------------------
    # Transactions
    # ----------------------------------------

    def load_transactions(
        self,
    ) -> List[Transaction]:

        rows = self._read(
            "Transactions"
        )

        return [
            Transaction.from_dict(row)
            for row in rows
        ]

    def save_transactions(
        self,
        transactions: List[Transaction],
    ):

        rows = [
            transaction.to_dict()
            for transaction in transactions
        ]

        self._write(
            "Transactions",
            rows,
        )