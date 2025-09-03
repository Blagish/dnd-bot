import json
from app.game_data.pf2_new.searcher import initialize_spell_indexer, find_spell, search_spells
from app.game_data.pf2_new.classes import Spell



if __name__ == '__main__':
    initialize_spell_indexer()

    # Демонстрируем поиск заклинаний по фразе
    query = 'Dragon Form'
    print(f"=== Поиск заклинаний по фразе '{query}' ===")
    detect_spells = search_spells(query)
    for result in detect_spells:
        print(f"- {result['name']} (рейтинг: {result['score']}, тип: {result['match_type']})")

    print(f"\nВсего найдено заклинаний с '{query}': {len(detect_spells)}")

    # Загружаем одно конкретное заклинание
    if detect_spells:
        print(f"\n=== Загружаем заклинание: {detect_spells[0]['name']} ===")
        spell_path = detect_spells[0]['path']
        with open(spell_path, 'r') as file:
            spell = Spell.from_json(json.loads(file.read()))
        print(vars(spell))
        res = spell.to_embed()
        embed = res.embed
        print(embed.title)
        print(embed.description)
        print(embed.footer)
        print(res.file.filename)

