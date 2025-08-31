import os
import json
from typing import Dict, Optional
from pathlib import Path


class SpellIndexer:
    def __init__(self, packs_directory: str = None):
        if packs_directory is None:
            current_dir = Path(__file__).parent
            self.packs_directory = current_dir / "packs"
        else:
            self.packs_directory = Path(packs_directory)
        
        self.spell_index: Dict[str, str] = {}
        self._build_index()
    
    def _build_index(self) -> None:
        print(f"Начинаем индексацию заклинаний из {self.packs_directory}")
        
        if not self.packs_directory.exists():
            print(f"Директория {self.packs_directory} не найдена!")
            return
        
        total_spells = 0
        
        # Проходим через все подпапки в packs (например, spells, items и т.д.)
        for pack_dir in self.packs_directory.iterdir():
            if not pack_dir.is_dir():
                continue
                
            print(f"Обрабатываем пак: {pack_dir.name}")
            pack_spells = self._index_pack(pack_dir)
            total_spells += pack_spells
        
        print(f"Индексация завершена! Обработано {total_spells} заклинаний.")
    
    def _index_pack(self, pack_dir: Path) -> int:
        spell_count = 0
        
        # Проходим через все подпапки в паке (например, 1st-rank, 2nd-rank и т.д.)
        for rank_dir in pack_dir.iterdir():
            if not rank_dir.is_dir():
                continue
            
            # Пропускаем служебные файлы
            if rank_dir.name.startswith('_'):
                continue
                
            spell_count += self._index_rank_directory(rank_dir)
        
        return spell_count
    
    def _index_rank_directory(self, rank_dir: Path) -> int:
        spell_count = 0
        
        # Проходим через все JSON файлы в директории
        for spell_file in rank_dir.glob("*.json"):
            try:
                spell_data = self._load_spell_data(spell_file)
                if spell_data and 'name' in spell_data:
                    spell_name = spell_data['name']
                    
                    # Проверяем на дубликаты
                    if spell_name in self.spell_index:
                        print(f"Предупреждение: заклинание '{spell_name}' уже существует! "
                              f"Старый путь: {self.spell_index[spell_name]}, "
                              f"Новый путь: {spell_file}")
                    
                    # Сохраняем относительный путь для более удобного использования
                    relative_path = spell_file.relative_to(self.packs_directory.parent)
                    self.spell_index[spell_name] = str(relative_path)
                    spell_count += 1
                    
            except Exception as e:
                print(f"Ошибка при обработке файла {spell_file}: {e}")
        
        return spell_count
    
    def _load_spell_data(self, spell_file: Path) -> Optional[dict]:
        try:
            with open(spell_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Не удалось загрузить {spell_file}: {e}")
            return None
    
    def find_spell(self, spell_name: str) -> Optional[str]:
        return self.spell_index.get(spell_name)
    
    def find_spell_case_insensitive(self, spell_name: str) -> Optional[str]:
        spell_name_lower = spell_name.lower()
        for name, path in self.spell_index.items():
            if name.lower() == spell_name_lower:
                return path
        return None
    
    def get_all_spell_names(self) -> list[str]:
        return list(self.spell_index.keys())
    
    def get_spell_count(self) -> int:
        return len(self.spell_index)
    
    def search_spells_by_partial_name(self, partial_name: str) -> list[tuple[str, str]]:
        partial_name_lower = partial_name.lower()
        results = []
        
        for name, path in self.spell_index.items():
            if partial_name_lower in name.lower():
                results.append((name, path))
        
        return results
    
    def search_spells(self, query: str, max_results: int = 50) -> list[dict]:
        """
        Расширенный поиск заклинаний с ранжированием результатов.
        
        Args:
            query: Поисковый запрос
            max_results: Максимальное количество результатов
        
        Returns:
            Список словарей с информацией о найденных заклинаниях
            Каждый словарь содержит: name, path, score, match_type
        """
        if not query or not query.strip():
            return []
        
        query = query.strip().lower()
        results = []
        
        for spell_name, spell_path in self.spell_index.items():
            spell_name_lower = spell_name.lower()
            score = 0
            match_type = ""
            
            # Точное совпадение названия (наивысший приоритет)
            if spell_name_lower == query:
                score = 100
                match_type = "exact"
            
            # Начинается с запроса (высокий приоритет)
            elif spell_name_lower.startswith(query):
                score = 90
                match_type = "starts_with"
            
            # Содержит запрос как отдельное слово (средний приоритет)
            elif self._contains_as_word(spell_name_lower, query):
                score = 70
                match_type = "word_match"
            
            # Содержит запрос как подстроку (низкий приоритет)
            elif query in spell_name_lower:
                score = 50
                match_type = "substring"
            
            # Частичное совпадение слов (очень низкий приоритет)
            elif self._partial_word_match(spell_name_lower, query):
                score = 30
                match_type = "partial"
            
            if score > 0:
                results.append({
                    'name': spell_name,
                    'path': spell_path,
                    'score': score,
                    'match_type': match_type
                })
        
        # Сортируем по убыванию рейтинга, затем по алфавиту
        results.sort(key=lambda x: (-x['score'], x['name'].lower()))
        
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
        pattern = r'\b' + re.escape(word) + r'\b'
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
    
    def search_spells_advanced(self, query: str, include_description: bool = False, max_results: int = 50) -> list[dict]:
        """
        Продвинутый поиск заклинаний с возможностью поиска по описанию.
        
        Args:
            query: Поисковый запрос
            include_description: Включать ли поиск по описанию заклинаний
            max_results: Максимальное количество результатов
        
        Returns:
            Список словарей с подробной информацией о найденных заклинаниях
        """
        if not query or not query.strip():
            return []
        
        # Сначала ищем по названиям
        name_results = self.search_spells(query, max_results)
        
        if not include_description:
            return name_results
        
        # Если включен поиск по описанию, загружаем и ищем в описаниях
        description_results = []
        query_lower = query.lower()
        
        # Избегаем дублирования с результатами поиска по названию
        found_names = {result['name'] for result in name_results}
        
        for spell_name, spell_path in self.spell_index.items():
            if spell_name in found_names:
                continue
                
            spell_data = self._load_spell_data(Path(self.packs_directory.parent) / spell_path)
            if spell_data:
                description = spell_data.get('system', {}).get('description', {}).get('value', '')
                if query_lower in description.lower():
                    description_results.append({
                        'name': spell_name,
                        'path': spell_path,
                        'score': 25,  # Низкий рейтинг для поиска по описанию
                        'match_type': 'description'
                    })
        
        # Объединяем результаты
        all_results = name_results + description_results
        all_results.sort(key=lambda x: (-x['score'], x['name'].lower()))
        
        return all_results[:max_results]


# Глобальный экземпляр индексатора
_spell_indexer: Optional[SpellIndexer] = None


def initialize_spell_indexer(packs_directory: str = None) -> SpellIndexer:
    global _spell_indexer
    _spell_indexer = SpellIndexer(packs_directory)
    return _spell_indexer


def get_spell_indexer() -> Optional[SpellIndexer]:
    return _spell_indexer


def find_spell(spell_name: str) -> Optional[str]:
    """
    Удобная функция для поиска заклинания по названию.
    
    Args:
        spell_name: Название заклинания
    
    Returns:
        Путь к файлу заклинания или None, если не найдено
    """
    if _spell_indexer is None:
        print("Индексатор заклинаний не инициализирован!")
        return None
    
    return _spell_indexer.find_spell_case_insensitive(spell_name)


def search_spells(query: str, max_results: int = 50) -> list[dict]:
    """
    Удобная функция для поиска заклинаний по запросу.
    
    Args:
        query: Поисковый запрос
        max_results: Максимальное количество результатов
    
    Returns:
        Список словарей с информацией о найденных заклинаниях
    """
    if _spell_indexer is None:
        print("Индексатор заклинаний не инициализирован!")
        return []
    
    return _spell_indexer.search_spells(query, max_results)


def search_spells_advanced(query: str, include_description: bool = False, max_results: int = 50) -> list[dict]:
    """
    Удобная функция для продвинутого поиска заклинаний.
    
    Args:
        query: Поисковый запрос
        include_description: Включать ли поиск по описанию заклинаний
        max_results: Максимальное количество результатов
    
    Returns:
        Список словарей с подробной информацией о найденных заклинаниях
    """
    if _spell_indexer is None:
        print("Индексатор заклинаний не инициализирован!")
        return []
    
    return _spell_indexer.search_spells_advanced(query, include_description, max_results)

if __name__ == '__main__':
    s = SpellIndexer()
    print(s.spell_index)
