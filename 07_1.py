with open('07_input.txt') as f:
    hands = [line.split() for line in f.read().strip().split('\n')]
#hands = [
#    ('32T3K', '765'),
#    ('T55J5', '684'),
#    ('KK677', '28'),
#    ('KTJJT', '220'),
#    ('QQQJA', '483')
#]

card_values = dict(zip('23456789TJQKA', range(13)))
hands = [
    (
        tuple(sorted((hand.count(c) for c in set(hand)), reverse=True)),
        tuple(map(card_values.get, hand)),
        int(bid)
    ) for hand, bid in hands
]
hands.sort()
print(sum(rank*bid for rank, (_, _, bid) in enumerate(hands, 1)))
