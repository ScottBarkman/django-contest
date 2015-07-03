import random
from datetime import datetime

from django.db.models import Sum
# Decouple logic from model methods - boo fat madels!


def prizes_available(contest):
    if contest.daily:
        today = datetime.today()
        winners = contest.entry_set.filter(
            created__year=today.year, created__month=today.month, created__day=today.day, winner=True)
        prizes_available = contest.prize_set.filter(
            date_available=today).aggregate(pa=Sum('number_available'))['pa']
    else:
        winners = contest.entry_set.filters(winner=True)
        prizes_available = contest.prize_set.aggregate(pa=Sum('number_available'))

    if winners.count() >= prizes_available:
        return False

    return True


def instant_win(entry):
    # double check contest

    if entry.contest.instant_win and entry.contest.prizes_available():
        for x in range(0, 3):
            winner = random.randint(1, entry.contest.instant_win_odds)
        # arbitrary number to look for in random number
        if winner == 1:
            today = datetime.today()
            entry.winner = True
            prizes_available = entry.contest.prize_set.filter(date_available=today).order_by('?')
            for p in prizes_available:
                if p.number_available > entry.contest.entry_set.filter(prize=p).count():
                    entry.prize = p
                    break

            entry.save()
            return True
        else:
            entry.winner = False
            entry.prize = None
            entry.save()
            return False
    else:
        entry.winner = False
        entry.prize = None
        entry.save()
        return False
