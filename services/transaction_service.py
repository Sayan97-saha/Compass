"""
transaction_service.py

Business logic for processing financial transactions.

Responsibilities:
- Create transactions
- Update account balances
- Handle transfers
- Reverse transactions
- Validate business rules
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from domain.account import Account
from domain.category import Category
from domain.merchant import Merchant
from domain.transaction import (
    Transaction,
    TransactionStatus,
    TransactionType,
)


class TransactionService:
    """Service responsible for transaction processing."""

    @staticmethod
    def create_transaction(
        *,
        account: Account,
        category: Category,
        amount: float,
        transaction_type: TransactionType,
        merchant: Optional[Merchant] = None,
        transaction_date: Optional[datetime] = None,
        description: Optional[str] = None,
        reference_number: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Transaction:
        """
        Create a transaction and update the account balance.
        """

        if amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        transaction = Transaction(
            account_id=account.id,
            category_id=category.id,
            merchant_id=merchant.id if merchant else None,
            transaction_type=transaction_type,
            status=TransactionStatus.COMPLETED,
            amount=amount,
            transaction_date=transaction_date or datetime.now(),
            description=description,
            reference_number=reference_number,
            notes=notes,
        )

        if transaction_type == TransactionType.INCOME:
            account.current_balance += amount

        elif transaction_type == TransactionType.EXPENSE:
            account.current_balance -= amount

        else:
            raise ValueError(
                "Transfers must be created using transfer()."
            )

        account.updated_at = datetime.now()

        return transaction

    @staticmethod
    def transfer(
        *,
        from_account: Account,
        to_account: Account,
        amount: float,
        transaction_date: Optional[datetime] = None,
        description: Optional[str] = None,
        reference_number: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> tuple[Transaction, Transaction]:
        """
        Transfer money between two accounts.
        Creates one debit transaction and one credit transaction.
        """

        if from_account.id == to_account.id:
            raise ValueError("Source and destination accounts cannot be the same.")

        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")

        timestamp = transaction_date or datetime.now()

        debit_transaction = Transaction(
            account_id=from_account.id,
            category_id="TRANSFER",
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.COMPLETED,
            amount=amount,
            transaction_date=timestamp,
            description=description,
            reference_number=reference_number,
            notes=notes,
        )

        credit_transaction = Transaction(
            account_id=to_account.id,
            category_id="TRANSFER",
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.COMPLETED,
            amount=amount,
            transaction_date=timestamp,
            description=description,
            reference_number=reference_number,
            notes=notes,
        )

        from_account.current_balance -= amount
        to_account.current_balance += amount

        now = datetime.now()
        from_account.updated_at = now
        to_account.updated_at = now

        return debit_transaction, credit_transaction

    @staticmethod
    def update_transaction(
        transaction: Transaction,
        *,
        amount: Optional[float] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        reference_number: Optional[str] = None,
    ) -> Transaction:
        """
        Update editable transaction fields.
        Balance recalculation is handled separately.
        """

        if amount is not None:
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            transaction.amount = amount

        if description is not None:
            transaction.description = description

        if notes is not None:
            transaction.notes = notes

        if reference_number is not None:
            transaction.reference_number = reference_number

        transaction.updated_at = datetime.now()

        return transaction

    @staticmethod
    def reverse_transaction(
        transaction: Transaction,
        account: Account,
    ) -> None:
        """
        Reverse a completed transaction.
        """

        if transaction.status != TransactionStatus.COMPLETED:
            raise ValueError("Only completed transactions can be reversed.")

        if transaction.transaction_type == TransactionType.INCOME:
            account.current_balance -= transaction.amount

        elif transaction.transaction_type == TransactionType.EXPENSE:
            account.current_balance += transaction.amount

        transaction.status = TransactionStatus.CANCELLED

        now = datetime.now()
        transaction.updated_at = now
        account.updated_at = now

    @staticmethod
    def delete_transaction(
        transaction: Transaction,
        account: Account,
    ) -> None:
        """
        Soft delete a transaction.
        """

        TransactionService.reverse_transaction(transaction, account)
        transaction.is_active = False
        transaction.updated_at = datetime.now()

    @staticmethod
    def validate_account(account: Account) -> None:
        """
        Validate an account before processing a transaction.
        """

        if not account.is_active:
            raise ValueError("Account is inactive.")

    @staticmethod
    def validate_transaction(transaction: Transaction) -> None:
        """
        Validate a transaction.
        """

        if not transaction.is_active:
            raise ValueError("Transaction is inactive.")

        if transaction.status == TransactionStatus.CANCELLED:
            raise ValueError("Transaction has been cancelled.")

        if transaction.amount <= 0:
            raise ValueError("Invalid transaction amount.")

    @staticmethod
    def can_withdraw(
        account: Account,
        amount: float,
    ) -> bool:
        """
        Check whether the account has sufficient balance.
        """

        return account.current_balance >= amount

    @staticmethod
    def get_balance(account: Account) -> float:
        """
        Return the current account balance.
        """

        return account.current_balance