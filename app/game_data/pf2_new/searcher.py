import json
from pathlib import Path
from typing import Dict, Optional, Union, List
from app.enums.PackType import PackType


class Pf2Indexer:
    def __init__(self, packs_directory: str = None):
        if packs_directory is None:
            current_dir = Path(__file__).parent
            self.packs_directory = current_dir / "packs"
        else:
            self.packs_directory = Path(packs_directory)

        # Структура: {pack_type: {item_name: file_path}}
        self.indices: Dict[str, Dict[str, str]] = {}
        self._build_all_indices()

    def _build_all_indices(self) -> None:
        """
        Строит индексы для всех типов паков.
        """
        print(f"Начинаем индексацию PF2e данных из {self.packs_directory}")

        if not self.packs_directory.exists():
            print(f"Директория {self.packs_directory} не найдена!")
            return

        total_items = 0

        # Проходим через все доступные типы паков
        for pack_type in PackType:
            pack_dir = self.packs_directory / pack_type.value
            if pack_dir.exists() and pack_dir.is_dir():
                print(f"Обрабатываем пак: {pack_type.value}")
                pack_items = self._build_pack_index(pack_type, pack_dir)
                total_items += pack_items
            else:
                print(f"Пак {pack_type.value} не найден, пропускаем")

        print(f"Индексация завершена! Обработано {total_items} элементов.")

    def _build_pack_index(self, pack_type: PackType, pack_dir: Path) -> int:
        """
        Строит индекс для конкретного типа пака.
        
        Args:
            pack_type: Тип пака
            pack_dir: Путь к директории пака
        
        Returns:
            Количество проиндексированных элементов
        """
        pack_index = {}
        total_items = 0

        # Рекурсивно обходим все файлы в паке
        for json_file in pack_dir.rglob("*.json"):
            # Пропускаем служебные файлы
            if json_file.name.startswith("_"):
                continue

            try:
                item_data = self._load_item_data(json_file)
                if item_data and "name" in item_data:
                    item_name = item_data["name"]

                    # Проверяем на дубликаты
                    if item_name in pack_index:
                        print(
                            f"Предупреждение: элемент '{item_name}' уже существует в {pack_type.value}! "
                            f"Старый путь: {pack_index[item_name]}, "
                            f"Новый путь: {json_file}"
                        )

                    # Сохраняем относительный путь
                    relative_path = json_file.relative_to(self.packs_directory.parent)
                    pack_index[item_name] = str(relative_path)
                    total_items += 1

            except Exception as e:
                print(f"Ошибка при обработке файла {json_file}: {e}")

        self.indices[pack_type.value] = pack_index
        print(f"Проиндексировано {total_items} элементов в {pack_type.value}")
        return total_items

    def _load_item_data(self, item_file: Path) -> Optional[dict]:
        """
        Загружает данные элемента из JSON файла.
        
        Args:
            item_file: Путь к файлу элемента
        
        Returns:
            Словарь с данными элемента или None в случае ошибки
        """
        try:
            with open(item_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Не удалось загрузить {item_file}: {e}")
            return None

    def find_item(self, item_name: str, pack_types: Optional[List[PackType]] = None) -> Optional[dict]:
        """
        Ищет элемент по точному названию.
        
        Args:
            item_name: Название элемента для поиска
            pack_types: Список типов паков для поиска (если None, ищет во всех)
        
        Returns:
            Словарь с информацией о найденном элементе или None
        """
        search_packs = pack_types or PackType.all_types()
        
        for pack_type in search_packs:
            if isinstance(pack_type, PackType):
                pack_key = pack_type.value
            else:
                pack_key = pack_type
                
            if pack_key in self.indices:
                if item_name in self.indices[pack_key]:
                    return {
                        'name': item_name,
                        'path': self.indices[pack_key][item_name],
                        'pack_type': pack_key
                    }
        return None

    def find_item_case_insensitive(self, item_name: str, pack_types: Optional[List[PackType]] = None) -> Optional[dict]:
        """
        Ищет элемент по названию без учета регистра.
        
        Args:
            item_name: Название элемента для поиска
            pack_types: Список типов паков для поиска (если None, ищет во всех)
        
        Returns:
            Словарь с информацией о найденном элементе или None
        """
        search_packs = pack_types or PackType.all_types()
        item_name_lower = item_name.lower()
        
        for pack_type in search_packs:
            if isinstance(pack_type, PackType):
                pack_key = pack_type.value
            else:
                pack_key = pack_type
                
            if pack_key in self.indices:
                for name, path in self.indices[pack_key].items():
                    if name.lower() == item_name_lower:
                        return {
                            'name': name,
                            'path': path,
                            'pack_type': pack_key
                        }
        return None

    def get_all_item_names(self, pack_types: Optional[List[PackType]] = None) -> Dict[str, List[str]]:
        """
        Возвращает все названия элементов, сгруппированные по типам паков.
        
        Args:
            pack_types: Список типов паков (если None, возвращает все)
        
        Returns:
            Словарь: {pack_type: [item_names]}
        """
        search_packs = pack_types or PackType.all_types()
        result = {}
        
        for pack_type in search_packs:
            if isinstance(pack_type, PackType):
                pack_key = pack_type.value
            else:
                pack_key = pack_type
                
            if pack_key in self.indices:
                result[pack_key] = list(self.indices[pack_key].keys())
        
        return result

    def get_total_count(self) -> int:
        """
        Возвращает общее количество проиндексированных элементов.
        
        Returns:
            Общее количество элементов
        """
        return sum(len(index) for index in self.indices.values())

    def get_pack_count(self, pack_type: PackType) -> int:
        """
        Возвращает количество элементов в конкретном паке.
        
        Args:
            pack_type: Тип пака
        
        Returns:
            Количество элементов в паке
        """
        pack_key = pack_type.value if isinstance(pack_type, PackType) else pack_type
        return len(self.indices.get(pack_key, {}))

    def search_items_by_partial_name(self, partial_name: str, pack_types: Optional[List[PackType]] = None) -> list[dict]:
        """
        Ищет элементы по частичному совпадению названия.
        
        Args:
            partial_name: Часть названия элемента
            pack_types: Список типов паков для поиска (если None, ищет во всех)
        
        Returns:
            Список словарей с информацией о найденных элементах
        """
        search_packs = pack_types or PackType.all_types()
        partial_name_lower = partial_name.lower()
        results = []

        for pack_type in search_packs:
            if isinstance(pack_type, PackType):
                pack_key = pack_type.value
            else:
                pack_key = pack_type
                
            if pack_key in self.indices:
                for name, path in self.indices[pack_key].items():
                    if partial_name_lower in name.lower():
                        results.append({
                            'name': name,
                            'path': path,
                            'pack_type': pack_key
                        })

        return results

    def search_items(self, query: str, pack_types: Optional[List[PackType]] = None, max_results: int = 50) -> list[dict]:
        """
        Расширенный поиск элементов с ранжированием результатов.

        Args:
            query: Поисковый запрос
            pack_types: Список типов паков для поиска (если None, ищет во всех)
            max_results: Максимальное количество результатов

        Returns:
            Список словарей с информацией о найденных элементах
            Каждый словарь содержит: name, path, pack_type, score, match_type
        """
        if not query or not query.strip():
            return []

        search_packs = pack_types or PackType.all_types()
        query = query.strip().lower()
        results = []

        for pack_type in search_packs:
            if isinstance(pack_type, PackType):
                pack_key = pack_type.value
            else:
                pack_key = pack_type
                
            if pack_key not in self.indices:
                continue

            for item_name, item_path in self.indices[pack_key].items():
                item_name_lower = item_name.lower()
                score = 0
                match_type = ""

                # Точное совпадение названия (наивысший приоритет)
                if item_name_lower == query:
                    score = 100
                    match_type = "exact"

                # Начинается с запроса (высокий приоритет)
                elif item_name_lower.startswith(query):
                    score = 90
                    match_type = "starts_with"

                # Содержит запрос как отдельное слово (средний приоритет)
                elif self._contains_as_word(item_name_lower, query):
                    score = 70
                    match_type = "word_match"

                # Содержит запрос как подстроку (низкий приоритет)
                elif query in item_name_lower:
                    score = 50
                    match_type = "substring"

                # Частичное совпадение слов (очень низкий приоритет)
                elif self._partial_word_match(item_name_lower, query):
                    score = 30
                    match_type = "partial"

                if score > 0:
                    results.append(
                        {
                            "name": item_name,
                            "path": item_path,
                            "pack_type": pack_key,
                            "score": score,
                            "match_type": match_type,
                        }
                    )

        # Сортируем по убыванию рейтинга, затем по алфавиту
        results.sort(key=lambda x: (-x["score"], x["name"].lower()))

        return results[:max_results]

    def _contains_as_word(self, text: str, word: str) -> bool:
        """
        Проверяет, содержится ли слово в тексте как отдельное слово.

        Args:
            text: Текст для поиска
            word: Искомое слово

        Returns:
            True, если слово найдено как отдельное слово
        """
        import re

        pattern = r"\b" + re.escape(word) + r"\b"
        return bool(re.search(pattern, text))

    def _partial_word_match(self, text: str, query: str) -> bool:
        """
        Проверяет частичное совпадение с любым словом в названии.

        Args:
            text: Текст заклинания
            query: Поисковый запрос

        Returns:
            True, если запрос частично совпадает с любым словом
        """
        words = text.split()
        for word in words:
            if len(query) >= 3 and query in word:
                return True
        return False

    def search_items_advanced(
        self, query: str, pack_types: Optional[List[PackType]] = None, include_description: bool = False, max_results: int = 50
    ) -> list[dict]:
        """
        Продвинутый поиск элементов с возможностью поиска по описанию.

        Args:
            query: Поисковый запрос
            pack_types: Список типов паков для поиска (если None, ищет во всех)
            include_description: Включать ли поиск по описанию элементов
            max_results: Максимальное количество результатов

        Returns:
            Список словарей с подробной информацией о найденных элементах
        """
        if not query or not query.strip():
            return []

        # Сначала ищем по названиям
        name_results = self.search_items(query, pack_types, max_results)

        if not include_description:
            return name_results

        # Если включен поиск по описанию, загружаем и ищем в описаниях
        description_results = []
        query_lower = query.lower()

        # Избегаем дублирования с результатами поиска по названию
        found_names = {result["name"] for result in name_results}

        search_packs = pack_types or PackType.all_types()
        
        for pack_type in search_packs:
            if isinstance(pack_type, PackType):
                pack_key = pack_type.value
            else:
                pack_key = pack_type
                
            if pack_key not in self.indices:
                continue

            for item_name, item_path in self.indices[pack_key].items():
                if item_name in found_names:
                    continue

                item_data = self._load_item_data(
                    Path(self.packs_directory.parent) / item_path
                )
                if item_data:
                    description = (
                        item_data.get("system", {}).get("description", {}).get("value", "")
                    )
                    if query_lower in description.lower():
                        description_results.append(
                            {
                                "name": item_name,
                                "path": item_path,
                                "pack_type": pack_key,
                                "score": 25,  # Низкий рейтинг для поиска по описанию
                                "match_type": "description",
                            }
                        )

        # Объединяем результаты
        all_results = name_results + description_results
        all_results.sort(key=lambda x: (-x["score"], x["name"].lower()))

        return all_results[:max_results]


# Глобальный экземпляр индексатора
_pf2_indexer: Optional[Pf2Indexer] = None


def initialize_pf2_indexer(packs_directory: str = None) -> Pf2Indexer:
    """
    Инициализирует глобальный индексатор PF2e данных.
    
    Args:
        packs_directory: Путь к директории packs (опционально)
    
    Returns:
        Экземпляр Pf2Indexer
    """
    global _pf2_indexer
    _pf2_indexer = Pf2Indexer(packs_directory)
    return _pf2_indexer


def get_pf2_indexer() -> Optional[Pf2Indexer]:
    """
    Возвращает глобальный экземпляр индексатора PF2e данных.
    
    Returns:
        Экземпляр Pf2Indexer или None, если не инициализирован
    """
    return _pf2_indexer


def find_item(item_name: str, pack_types: Optional[List[PackType]] = None) -> Optional[dict]:
    """
    Удобная функция для поиска элемента по названию.

    Args:
        item_name: Название элемента
        pack_types: Список типов паков для поиска

    Returns:
        Словарь с информацией о найденном элементе или None
    """
    if _pf2_indexer is None:
        print("Индексатор PF2e данных не инициализирован!")
        return None

    return _pf2_indexer.find_item_case_insensitive(item_name, pack_types)


def search_items(query: str, pack_types: Optional[List[PackType]] = None, max_results: int = 50) -> list[dict]:
    """
    Удобная функция для поиска элементов по запросу.

    Args:
        query: Поисковый запрос
        pack_types: Список типов паков для поиска
        max_results: Максимальное количество результатов

    Returns:
        Список словарей с информацией о найденных элементах
    """
    if _pf2_indexer is None:
        print("Индексатор PF2e данных не инициализирован!")
        return []

    return _pf2_indexer.search_items(query, pack_types, max_results)


def search_items_advanced(
    query: str, pack_types: Optional[List[PackType]] = None, include_description: bool = False, max_results: int = 50
) -> list[dict]:
    """
    Удобная функция для продвинутого поиска элементов.

    Args:
        query: Поисковый запрос
        pack_types: Список типов паков для поиска
        include_description: Включать ли поиск по описанию элементов
        max_results: Максимальное количество результатов

    Returns:
        Список словарей с подробной информацией о найденных элементах
    """
    if _pf2_indexer is None:
        print("Индексатор PF2e данных не инициализирован!")
        return []

    return _pf2_indexer.search_items_advanced(
        query, pack_types, include_description, max_results
    )


# Backward compatibility functions for spells
def find_spell(spell_name: str) -> Optional[str]:
    """
    Функция обратной совместимости для поиска заклинания.
    
    Args:
        spell_name: Название заклинания
    
    Returns:
        Путь к файлу заклинания или None, если не найдено
    """
    result = find_item(spell_name, [PackType.SPELLS])
    return result['path'] if result else None


def search_spells(query: str, max_results: int = 50) -> list[dict]:
    """
    Функция обратной совместимости для поиска заклинаний.
    
    Args:
        query: Поисковый запрос
        max_results: Максимальное количество результатов
    
    Returns:
        Список словарей с информацией о найденных заклинаниях
    """
    return search_items(query, [PackType.SPELLS], max_results)


# Alias for backward compatibility
initialize_spell_indexer = initialize_pf2_indexer


if __name__ == "__main__":
    indexer = Pf2Indexer()
    print("Индексы:", list(indexer.indices.keys()))
    for pack_type, index in indexer.indices.items():
        print(f"{pack_type}: {len(index)} элементов")
