import re

ticket_counts = {}
with open('04_input.txt') as f:
    for line in f:
        cns, winning_numbers, my_numbers = re.fullmatch(r'Card +(\d+): +(\d+(?: +\d+)*) \| +(\d+(?: +\d+)*)\n?', line).groups()
        card_number = int(cns)
        matches = len({int(n) for n in winning_numbers.split()} & {int(n) for n in my_numbers.split()})
        if card_number in ticket_counts:
            ticket_counts[card_number] += 1
        else:
            ticket_counts[card_number] = 1
        for prize_card_number in range(card_number+1, card_number+matches+1):
            if prize_card_number in ticket_counts:
                ticket_counts[prize_card_number] += ticket_counts[card_number]
            else:
                ticket_counts[prize_card_number] = ticket_counts[card_number]
print(sum(ticket_counts.values()))
