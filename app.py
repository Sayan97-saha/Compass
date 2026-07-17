"""
app.py

Application entry point for Compass.
"""

from config import (
    CREDENTIALS_FILE,
    SPREADSHEET_ID,
)
from repositories.sheets_repository import SheetsRepository
from services.calculation_service import CalculationService


def main() -> None:
    print("===================================")
    print("        Compass v1.0.0")
    print("===================================\n")

    repository = SheetsRepository(
        credentials_file=str(CREDENTIALS_FILE),
        spreadsheet_id=SPREADSHEET_ID,
    )

    accounts = repository.load_accounts()
    transactions = repository.load_transactions()

    print(f"Accounts Loaded     : {len(accounts)}")
    print(f"Transactions Loaded : {len(transactions)}")

    cash_balance = CalculationService.calculate_cash_balance(
        accounts
    )

    cash_flow = CalculationService.calculate_cash_flow(
        transactions
    )

    print(f"\nCash Balance : ₹{cash_balance:,.2f}")
    print(f"Cash Flow    : ₹{cash_flow:,.2f}")

    print("\nCompass initialized successfully.")


if __name__ == "__main__":
    main()