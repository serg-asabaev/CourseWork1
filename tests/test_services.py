import pytest


from src.services import physical_transactions


def test_physical_transactions(phys_transactions):
    assert physical_transactions() == phys_transactions
