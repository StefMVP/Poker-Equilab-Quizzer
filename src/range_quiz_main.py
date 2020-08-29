import random


def get_range_from_equilab_format(logger, range, hand):
    try:
        logger.debug("Entering get_range_from_equilab_format {} {}".format(range, hand))
        cleaned_range = range.split('{')[1].split('}')[0]
        split = cleaned_range.split(',')

        final = []
        cur = []
        for item in split:
            if ':' in item:
                if cur:
                    final.append(cur)
                item2 = item.split(':')
                percent = item2[0]
                hand_range = item2[1]
                cur = [percent, []]
                cur[1].append(hand_range)
            else:
                cur[1].append(item)
        logger.debug("get_range_from_equilab_format return range_arr {}".format(final))
        return final
    except Exception as e:
        logger.exception(e)


def is_hand_paired(logger, hand):
    if hand[0][0] == hand[1][0]:
        logger.debug("hand IS paired {}".format(hand))
        return True
    else:
        logger.debug("hand is NOT paired {}".format(hand))
        return False


def is_hand_range_paired(logger, hand_range):
    if hand_range[0] == hand_range[1]:
        logger.debug("hand range IS paired {}".format(hand_range))
        return True
    else:
        logger.debug("hand range is NOT paired {}".format(hand_range))
        return False


def is_hand_suited(logger, hand):
    if hand[0][1] == hand[1][1]:
        logger.debug("hand IS suited {}".format(hand))
        return True
    else:
        logger.debug("hand is NOT suited {}".format(hand))
        return False


def is_hand_range_suited(logger, hand_range):
    hand_range = hand_range.replace('+', '')
    if hand_range[-1] == 's':
        logger.debug("hand range IS suited {}".format(hand_range))
        return True
    else:
        logger.debug("hand range is NOT suited {}".format(hand_range))
        return False


def get_range_percent_from_hand(logger, range, hand):
    try:
        range_with_percent_arr = get_range_from_equilab_format(logger, range, hand)

        for percent, hand_range_arr in range_with_percent_arr:
            for hand_range in hand_range_arr:
                if is_hand_paired(logger, hand):
                    if is_hand_range_paired(logger, hand_range):
                        if hand_range[0] == hand[0][0]:
                            logger.debug("Paired hand equal {} {}".format(hand_range, hand, percent))
                            return percent
                        elif hand_range[0] < hand[0][0] and hand_range[-1] == "+":
                            logger.debug("Paired hand included {} {} {}".format(hand_range, hand, percent))
                            return percent
                else:
                    if is_hand_range_suited(logger, hand_range):
                        if hand_range[0] == hand[0][0] and hand_range[1][0] == hand[1][0] and is_hand_suited(logger, hand):
                            logger.debug("Suited hand equal {} {} {}".format(hand_range, hand, percent))
                            return percent
                        if hand_range[0] == hand[0][0] and hand_range[1][0] < hand[1][0] and hand_range[-1] == "+" and is_hand_suited(logger, hand):
                            logger.debug("Suited hand included {} {} {}".format(hand_range, hand, percent))
                            return percent
                    else:
                        if hand_range[0] == hand[0][0] and hand_range[1][0] == hand[1][0]:
                            logger.debug("Hand equal {} {} {}".format(hand_range, hand, percent))
                            return percent
                        if hand_range[0] == hand[0][0] and hand_range[1][0] < hand[1][0] and hand_range[-1] == "+":
                            logger.debug("Hand included {} {} {}".format(hand_range, hand, percent))
                            return percent
        logger.debug("Not Found {} {}".format(hand, 0))
        return 0

    except Exception as e:
        logger.exception(e)
        return 0


def get_random_card(logger, exclude_cards):
    suits = ['S', 'H', 'D', 'C']
    faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    while True:
        chosen_face = random.choice(faces)
        chosen_suit = random.choice(suits)
        hand = [chosen_face, chosen_suit]
        if not exclude_cards:
            break
        elif hand not in exclude_cards:
            break

    logger.debug("get_random_card {} with excluded_cards {}".format(hand, exclude_cards))
    return hand


def sort_cards(logger, cards):
    STR_RANKS = '23456789TJQKA'
    INT_RANKS = range(13)
    CHAR_RANK_TO_INT_RANK = dict(zip(list(STR_RANKS), INT_RANKS))
    if CHAR_RANK_TO_INT_RANK[cards[0][0]] < CHAR_RANK_TO_INT_RANK[cards[1][0]]:
        temp = cards[0]
        cards[0] = cards[1]
        cards[1] = temp

    logger.debug("sort cards {}".format(cards))
    return cards


def get_random_hand(logger, number_cards):
    cards = []
    excluded_cards = []

    for i in range(0, number_cards):
        card = get_random_card(logger, excluded_cards)
        cards.append(card)

    cards = sort_cards(logger, cards)

    logger.debug("get_random_hand {} with # of cards {}".format(cards, number_cards))
    return cards


def main(logger, const, config):
    range = '...BU {100:22+,A2s+,K2s+,Q3s+,J4s+,T6s+,96s+,86s+,75s+,64s+,54s,A5o+,K9o+,Q9o+,J9o+,T8o+,24:A4o,92:K8o,19:J8o,84:98o,98:85s,7:Q2s}'
    number_cards = 2
    hand = get_random_hand(logger, number_cards)
    get_range_percent_from_hand(logger, range, hand)
