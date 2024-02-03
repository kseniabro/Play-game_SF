from random import choice

from bot_zoo.texts.answer_button_text import *
from bot_zoo.database.all_animals import ALL_ANIMALS


async def get_totem_animal(proxy_dict: dict) -> dict:
    chat_id = proxy_dict.get('user_id')
    proxy_dict.pop('user_id')

    hidden_results = {}
    only_qualities = []

    for animal_dict in ALL_ANIMALS.values():
        for quality in animal_dict['ANIMAL_QUALITIES']:
            only_qualities.append(quality)

    quals_set = set(only_qualities)

    for qual in quals_set:
        hidden_results[qual] = 0

    # ------------
    # 1st question
    if proxy_dict['1st_question'] == answer_1_1:
        hidden_results['скорость'] += 1
        hidden_results['безбашенность'] += 1
    if proxy_dict['1st_question'] == answer_1_2:
        hidden_results['скрытность'] += 1
        hidden_results['спокойствие'] += 1
    if proxy_dict['1st_question'] == answer_1_3:
        hidden_results['теплолюбивость'] += 1
        hidden_results['неуклюжесть'] += 1
    if proxy_dict['1st_question'] == answer_1_4:
        hidden_results['редкость'] += 1
        hidden_results['стадность'] += 1

    # ------------
    # 2nd question
    if proxy_dict['2nd_question'] == answer_2_1:
        hidden_results['теплолюбивость'] += 1
        hidden_results['спокойствие'] += 1
    if proxy_dict['2nd_question'] == answer_2_2:
        hidden_results['скорость'] += 1
        hidden_results['скрытность'] += 1
    if proxy_dict['2nd_question'] == answer_2_3:
        hidden_results['одиночка'] += 1
        hidden_results['безбашенность'] += 1
    if proxy_dict['2nd_question'] == answer_2_4:
        hidden_results['храбрость'] += 1
        hidden_results['стадность'] += 1

    # ------------
    # 3rd question
    if proxy_dict['3rd_question'] == answer_3_1:
        hidden_results['скорость'] += 1
        hidden_results['безбашенность'] += 1
    if proxy_dict['3rd_question'] == answer_3_2:
        hidden_results['редкость'] += 1
        hidden_results['ловкость'] += 1
    if proxy_dict['3rd_question'] == answer_3_3:
        hidden_results['теплолюбивость'] += 1
        hidden_results['одиночка'] += 1
    if proxy_dict['3rd_question'] == answer_3_4:
        hidden_results['скрытность'] += 1
        hidden_results['спокойствие'] += 1

    # ------------
    # 4th question
    if proxy_dict['4th_question'] == answer_4_1:
        hidden_results['неуклюжесть'] += 1
        hidden_results['стадность'] += 1
    if proxy_dict['4th_question'] == answer_4_2:
        hidden_results['одиночка'] += 1
        hidden_results['скорость'] += 1
    if proxy_dict['4th_question'] == answer_4_3:
        hidden_results['спокойствие'] += 1
        hidden_results['скрытность'] += 1
    if proxy_dict['4th_question'] == answer_4_4:
        hidden_results['храбрость'] += 1
        hidden_results['безбашенность'] += 1

    # ------------
    # 5th question
    if proxy_dict['5th_question'] == answer_5_1:
        hidden_results['теплолюбивость'] += 1
        hidden_results['скрытность'] += 1
    if proxy_dict['5th_question'] == answer_5_2:
        hidden_results['спокойствие'] += 1
        hidden_results['одиночка'] += 1
    if proxy_dict['5th_question'] == answer_5_3:
        hidden_results['скорость'] += 1
        hidden_results['ловкость'] += 1

    # это кнопка про бинтуронга
    if proxy_dict['5th_question'] == answer_5_4:
        return {
            'chat_id': chat_id,
            'photo': ALL_ANIMALS['ANIMAL_1']['ANIMAL_IMAGE'],
            'caption': ALL_ANIMALS['ANIMAL_1']['ANIMAL_DESCRIPTION'],
            'reply_markup': ALL_ANIMALS['ANIMAL_1']['ANIMAL_KB'],
        }

    max_value = max(hidden_results.values())

    max_quals_dict = {key: value for key, value in hidden_results.items() if value == max_value}
    top_qualities_list = [q for q in max_quals_dict.keys()]
    print('top_qualities_list = ', top_qualities_list)

    filtered_animals = []

    for quality in top_qualities_list:
        for animal, dict_ in ALL_ANIMALS.items():
            for anim_qual in dict_['ANIMAL_QUALITIES']:
                if quality == anim_qual:
                    filtered_animals.append(animal)

    print('hidden_results = ', hidden_results)
    print('filtered_animals = ', filtered_animals)

    if len(filtered_animals) == 1:
        return {
            'chat_id': chat_id,
            'photo': ALL_ANIMALS[f'{filtered_animals[0]}']['ANIMAL_IMAGE'],
            'caption': ALL_ANIMALS[f'{filtered_animals[0]}']['ANIMAL_DESCRIPTION'],
            'reply_markup': ALL_ANIMALS[f'{filtered_animals[0]}']['ANIMAL_KB'],
        }

    else:
        winners = {animal: 0 for animal in filtered_animals}

        for filtered_animal in filtered_animals:
            for top_quality in top_qualities_list:
                for qual in only_qualities:
                    if top_quality == qual:
                        winners[filtered_animal] += 1

        print('winners = ', winners)
        max_points = max(winners.values())
        winner_dict = {key: value for key, value in winners.items() if value == max_points}
        print('winners_dict = ', winner_dict)

        if len(winner_dict) == 1:
            return {
                'chat_id': chat_id,
                'photo': ALL_ANIMALS[f'{list(winner_dict.keys())[0]}']['ANIMAL_IMAGE'],
                'caption': ALL_ANIMALS[f'{list(winner_dict.keys())[0]}']['ANIMAL_DESCRIPTION'],
                'reply_markup': ALL_ANIMALS[f'{list(winner_dict.keys())[0]}']['ANIMAL_KB'],
            }

        else:
            rand_winner = choice(list(winner_dict.keys()))
            print(rand_winner)

            return {
                'chat_id': chat_id,
                'photo': ALL_ANIMALS[f'{rand_winner}']['ANIMAL_IMAGE'],
                'caption': ALL_ANIMALS[f'{rand_winner}']['ANIMAL_DESCRIPTION'],
                'reply_markup': ALL_ANIMALS[f'{rand_winner}']['ANIMAL_KB'],
            }