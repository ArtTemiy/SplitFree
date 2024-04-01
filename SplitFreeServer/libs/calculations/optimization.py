import collections
import logging
import typing
from dataclasses import dataclass
from split.models.split import Split


@dataclass
class Payout:
    user_from: str
    user_to: str
    amount: float


def optimize(splits: list[Split]) -> list[Payout]:
    # Find total debts
    balances: dict[str, float] = collections.defaultdict(lambda : 0)
    for split in splits:
        for spend in split.spends.all():
            balances[spend.user.username] += spend.amount

    positives = sorted(
        [(username, amount) for username, amount in balances.items() if amount > 0],
        key=lambda x: x[0],
        reverse=True
    )  # From big to small
    negatives = sorted(
        [(username, -amount) for username, amount in balances.items() if amount < 0],
        key=lambda x: x[0]
    )  # From small to big

    # Build result
    result: list[Payout] = []
    neg_amount = 0
    pos_amount = 0
    neg_user = None

    for pos_user, pos_amount in positives:
        def _pay_from_left():
            nonlocal neg_amount, pos_amount, pos_user, neg_user

            pay_amount = min(neg_amount, pos_amount)
            neg_amount -= pay_amount
            pos_amount -= pay_amount
            result.append(
                Payout(
                    user_from=pos_user,
                    user_to=neg_user,
                    amount=pay_amount
                )
            )

            if neg_amount == 0:
                neg_user = None

        if neg_amount > 0:
            _pay_from_left()

        while pos_amount != 0 and len(negatives) > 0:
            neg_user, neg_amount = negatives.pop()
            _pay_from_left()

    if pos_amount > 0 or neg_amount != 0:
        logging.error(f'Bad optimization: {pos_amount=}, {neg_amount=}')
    return result
