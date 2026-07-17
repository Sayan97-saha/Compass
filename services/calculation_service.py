"""
calculation_service.py

Business logic for financial calculations.

Responsibilities:
- Net worth
- Cash flow
- Savings rate
- Budget usage
- Goal progress
- Emergency fund
- Credit utilization
- Portfolio allocation
"""

from __future__ import annotations

from typing import List

from domain.account import Account
from domain.asset import Asset
from domain.budget import Budget
from domain.goal import Goal
from domain.investment import Investment
from domain.transaction import Transaction, TransactionType


class CalculationService:

    @staticmethod
    def calculate_net_worth(
        assets: List[Asset],
        liabilities: List[Account],
    ) -> float:
        total_assets = sum(asset.current_value for asset in assets)
        total_liabilities = sum(
            account.current_balance for account in liabilities
        )
        return total_assets - total_liabilities

    @staticmethod
    def calculate_cash_balance(
        accounts: List[Account],
    ) -> float:
        return sum(account.current_balance for account in accounts)

    @staticmethod
    def calculate_income(
        transactions: List[Transaction],
    ) -> float:
        return sum(
            t.amount
            for t in transactions
            if t.transaction_type == TransactionType.INCOME
        )

    @staticmethod
    def calculate_expenses(
        transactions: List[Transaction],
    ) -> float:
        return sum(
            t.amount
            for t in transactions
            if t.transaction_type == TransactionType.EXPENSE
        )

    @staticmethod
    def calculate_cash_flow(
        transactions: List[Transaction],
    ) -> float:
        return (
            CalculationService.calculate_income(transactions)
            - CalculationService.calculate_expenses(transactions)
        )

    @staticmethod
    def calculate_savings_rate(
        transactions: List[Transaction],
    ) -> float:

        income = CalculationService.calculate_income(transactions)

        if income == 0:
            return 0.0

        expenses = CalculationService.calculate_expenses(transactions)

        return round(((income - expenses) / income) * 100, 2)

    @staticmethod
    def calculate_budget_usage(
        budget: Budget,
        spent: float,
    ) -> float:

        if budget.amount == 0:
            return 0.0

        return round((spent / budget.amount) * 100, 2)

    @staticmethod
    def calculate_goal_progress(
        goal: Goal,
    ) -> float:

        if goal.target_amount == 0:
            return 0.0

        return round(
            (goal.current_amount / goal.target_amount) * 100,
            2,
        )

    @staticmethod
    def calculate_emergency_fund_months(
        emergency_fund: float,
        monthly_expenses: float,
    ) -> float:

        if monthly_expenses == 0:
            return 0.0

        return round(
            emergency_fund / monthly_expenses,
            2,
        )

    @staticmethod
    def calculate_credit_utilization(
        used_credit: float,
        total_limit: float,
    ) -> float:

        if total_limit == 0:
            return 0.0

        return round(
            (used_credit / total_limit) * 100,
            2,
        )

    @staticmethod
    def calculate_portfolio_value(
        investments: List[Investment],
    ) -> float:

        return sum(
            investment.current_value
            for investment in investments
        )

    @staticmethod
    def calculate_portfolio_allocation(
        investments: List[Investment],
    ) -> dict[str, float]:

        total = CalculationService.calculate_portfolio_value(
            investments
        )

        if total == 0:
            return {}

        allocation = {}

        for investment in investments:
            allocation[investment.name] = round(
                (investment.current_value / total) * 100,
                2,
            )

        return allocation