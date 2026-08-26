from types import SimpleNamespace

from bot import should_block_transaction_reference


def test_same_user_rejected_reference_is_allowed():
    existing_payment = SimpleNamespace(user_id=7, status="REJECTED")

    assert should_block_transaction_reference(existing_payment, 7) is False


def test_same_user_pending_reference_is_blocked():
    existing_payment = SimpleNamespace(user_id=7, status="PENDING")

    assert should_block_transaction_reference(existing_payment, 7) is True


def test_other_user_reference_is_blocked():
    existing_payment = SimpleNamespace(user_id=9, status="PENDING")

    assert should_block_transaction_reference(existing_payment, 7) is True
