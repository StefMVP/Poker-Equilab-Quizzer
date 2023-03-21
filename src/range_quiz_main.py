import random
import file_handler
import os


def get_range_from_equilab_format(logger, range, hand):
    try:
        logger.debug("Entering get_range_from_equilab_format {} {}".format(range, hand))
        split = range.replace('{', '').replace('}', '').split(',')

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
                            return int(percent)
                        elif get_card_int_rank(hand_range[1]) < get_card_int_rank(hand[1][0]) and hand_range[-1] == "+":
                            logger.debug("Paired hand included {} {} {}".format(hand_range, hand, percent))
                            return int(percent)
                else:
                    if is_hand_range_suited(logger, hand_range):
                        if hand_range[0] == hand[0][0] and hand_range[1] == hand[1][0] and is_hand_suited(logger, hand):
                            logger.debug("Suited hand equal {} {} {}".format(hand_range, hand, percent))
                            return int(percent)
                        if hand_range[0] == hand[0][0] and get_card_int_rank(hand_range[1]) < get_card_int_rank(hand[1][0]) and hand_range[-1] == "+" and is_hand_suited(logger, hand):
                            logger.debug("Suited hand included {} {} {}".format(hand_range, hand, percent))
                            return int(percent)
                    else:
                        if hand_range[0] == hand[0][0] and hand_range[1] == hand[1][0]:
                            logger.debug("Hand equal {} {} {}".format(hand_range, hand, percent))
                            return int(percent)
                        if hand_range[0] == hand[0][0] and get_card_int_rank(hand_range[1]) < get_card_int_rank(hand[1][0]) and hand_range[-1] == "+":
                            logger.debug("Hand included {} {} {}".format(hand_range, hand, percent))
                            return int(percent)
        logger.debug("Not Found {} {}".format(hand, 0))
        return 0

    except Exception as e:
        logger.exception(e)
        return 0


def get_random_card(logger, exclude_cards):
    suits = ['s', 'h', 'd', 'c']
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


def get_card_int_rank(card):
    str_ranks = '23456789TJQKA'
    int_ranks = range(13)
    char_rank_to_int_rank = dict(zip(list(str_ranks), int_ranks))
    return char_rank_to_int_rank[card[0]]


def sort_cards(logger, cards):
    if get_card_int_rank(cards[0][0]) < get_card_int_rank(cards[1][0]):
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
        excluded_cards.append(card)
        cards.append(card)

    cards = sort_cards(logger, cards)

    logger.debug("get_random_hand {} with # of cards {}".format(cards, number_cards))
    return cards


def get_ranges_from_equilab_ini(logger, path):
    file = file_handler.open_file(logger, path)
    file = file.split('\n')
    ranges = []
    depth_1 = ''
    depth_2 = ''
    depth_3 = ''
    index = 1
    for line in file:
        if not line.startswith('.'):
            continue
        elif '{' not in line and '}' not in line:
            num_periods = line.count('.')
            line = line.replace('.', '')
            if num_periods == 1:
                depth_1 = line
                depth_2 = ''
                depth_3 = ''
            if num_periods == 2:
                depth_2 = line
                depth_3 = ''
            if num_periods == 3:
                depth_3 = line
        else:
            split_arr = line.replace('.', '').split(' {')
            title = (depth_1 + ':' + depth_2 + ':' + depth_3 + ':' + split_arr[0]).replace('::', ':')
            range = split_arr[1]
            ranges.append([index, title, range])
            index = index + 1
    return ranges


def console_select_range(logger, ranges):
    try:
        while True:
            for range in ranges:
                print(range)
            print("Please select a range by number, comma delimited, or *: ")
            selection = input()
            if selection == "*":
                return ranges
            selection = selection.split(',')
            final_ranges = []
            for select in selection:
                try:
                    select = int(select)
                    final_ranges.append(ranges[int(select)])
                except:
                    for range in ranges:
                        if select.lower() in range[1].lower():
                            final_ranges.append(range)
                #return [ranges[selection - 1]]
            return final_ranges
    except Exception as e:
        logger.exception(e)
        console_select_range(logger, ranges)


def get_str_from_list_hand(hand_arr):
    return '{}{}-{}{}'.format(hand_arr[0][0], hand_arr[0][1], hand_arr[1][0], hand_arr[1][1])


def main_loop(logger, const, config, ranges):
    try:
        selected_ranges = console_select_range(logger, ranges)
        wrong_hands = []
        correct = 0
        total = 0
        while True:
            selected_range = random.choice(selected_ranges)
            hand = get_random_hand(logger, const.NumberCards)
            #hand = ['AD','9D'] #Leave for testing
            percent = get_range_percent_from_hand(logger, selected_range[2], hand)
            os.system(const.ClearCommand)
            print('---------------------------------')
            print('{}'.format(selected_range[1]))
            if total != 0:
                print("Total: {} / {} ({}%)".format(correct, total, round((correct/total)*100), 2))
            if wrong_hands:
                print("Wrong Hands: {}".format(wrong_hands))
            print('---------------------------------')
            print('1: Infrequent (0%-25%)')
            print('2: Sometimes (25%-75%)')
            print('3: Frequent (75%-100%)')
            print('0: Back to main menu')
            print("Hand: {}".format(get_str_from_list_hand(hand)))
            try:
                answer = int(input())
            except:
                continue
            os.system(const.ClearCommand)
            print('---------------------------------')
            print('{}'.format(selected_range[1]))
            if total != 0:
                print("Total: {} / {} ({}%)".format(correct, total, round((correct/total)*100), 2))
            if wrong_hands:
                print("Wrong Hands: {}".format(wrong_hands))
            print('---------------------------------')
            print("Hand: {}".format(get_str_from_list_hand(hand)))
            if answer == 0:
                os.system(const.ClearCommand)
                wrong_hands = []
                correct = 0
                total = 0
                selected_range = console_select_range(logger, ranges)
                continue
            elif answer == 1:
                if percent > 25:
                    print("Incorrect - Exact:{}%".format(percent))
                    wrong_hands.append(get_str_from_list_hand(hand))
                else:
                    print("Correct - Infrequent - Exact:{}%".format(percent))
                    correct = correct + 1
            elif answer == 2:
                if percent < 25 or percent > 75:
                    print("Incorrect - Exact:{}%".format(percent))
                    wrong_hands.append(get_str_from_list_hand(hand))
                else:
                    print("Correct - Sometimes - Exact:{}%".format(percent))
                    correct = correct + 1
            elif answer == 3:
                if percent < 75:
                    print("Incorrect - Exact:{}%".format(percent))
                    wrong_hands.append(get_str_from_list_hand(hand))
                else:
                    print("Correct - Frequent - Exact:{}%".format(percent))
                    correct = correct + 1
            else:
                continue
            total = total + 1

            input("Press any key...")
    except Exception as e:
        logger.exception(e)
        main_loop(logger, const, config, ranges)


def main(logger, const, config):
    ranges = get_ranges_from_equilab_ini(logger, config.RangePath)
    main_loop(logger, const, config, ranges)

    #print("           %%%     %%%")
    #print("      %%%       D      %%%")
    #print("    %%%                     %%%")
    #print("  %%%  CO                 SB  %%%")
    #print(" %%%                           %%%")
    #print(" %%%                           %%%")
    #print("  %%%  HJ                 BB  %%%")
    #print("    %%%                     %%%")
    #print("      %%%       LJ     %%%")
    #print("           %%%     %%%")

