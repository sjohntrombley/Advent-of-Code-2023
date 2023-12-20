with open('07_input.txt') as f:
    hands = [line.split() for line in f.read().strip().split('\n')]

card_values = dict(zip('J23456789TQKA', range(13)))
hands = [
    (
        (pre_joker[0]+hand.count('J'), *pre_joker[1:])
            if len(pre_joker := sorted((hand.count(c) for c in set(hand)-{'J'}), reverse=True)) > 0
            else (5,),
        tuple(map(card_values.get, hand)),
        int(bid)
    ) for hand, bid in hands
]
hands.sort()
print(sum(rank*bid for rank, (_, _, bid) in enumerate(hands, 1)))
