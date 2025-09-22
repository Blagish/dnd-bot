import json

from app.game_data.pf2_new.classes.spells import Spell
from app.game_data.pf2_new.classes.feats import Feat
from app.game_data.pf2_new.searcher import (initialize_spell_indexer,
                                            search_items)
from app.enums.PackType import PackType

if __name__ == "__main__":
    initialize_spell_indexer()

    # Демонстрируем поиск заклинаний по фразе
    query = "Fireball"
    type_ = PackType.spell
    print(f"=== Поиск штук по фразе '{query}' ===")
    detect_spells = search_items(query, [type_])
    for result in detect_spells:
        print(
            f"- {result['name']} (рейтинг: {result['score']}, тип: {result['match_type']})"
        )

    print(f"\nВсего найдено штук с '{query}': {len(detect_spells)}")

    if detect_spells:
        print(f"\n=== Загружаем штуку: {detect_spells[0]['name']} ===")
        spell_path = detect_spells[0]["path"]
        with open(spell_path, "r") as file:
            data = json.loads(file.read())
            print(data)
            match type_:
                case PackType.SPELLS:
                    cls_ = Spell
                case PackType.FEATS:
                    cls_ = Feat
            spell = cls_.from_json(data)
        print(vars(spell))
        res = spell.to_embed()
        embed = res.embed
        print(embed.title)
        print(embed.description)
        print(embed.footer)
        if res.file:
            print(res.file.filename)
