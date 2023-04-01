from pprint import pprint

class BuildTree:
    
    def __init__(self):
        self.paths = {}
    def add_path(self, paths):
        
        for verb, path in paths:
            # Исключаем версию api
            path = path.replace("/api/v1", "")
            parts = path.split("/")
            # дробим путь на части и исключаем пустые части и части с параметрами {}
            parts = [part for part in parts if "{" not in part and "}" not in part and part != ""]
            current = self.paths
            # создаем вершину дерева/поддерево без последней части, которая содержит метод
            for part in parts[:-1]: 
                current = current.setdefault(part, {}) # добавляем ключ если его нет 
            last_part = parts[-1]
            
            # проверяем или последняя часть пути существует в словаре, то проверяем метод иначе добавляем эту часть с методом
            if last_part in current:
                if current[last_part] != verb: # проверка разных методов у одного ключа
                    raise Exception(f"Конфликт пути: /api/v1{path}, существующий метод: {current[last_part]}, новый метод: {verb}")
            else:
                current[last_part] = verb
        # Проверка на одинаковую верхушку дерева
        top_level_nodes = set()
        for path in self.paths:
            top_level_nodes.add(path.split("/")[0])
        if len(top_level_nodes) > 1:
            raise Exception(f"Разные верхушки дерева: {top_level_nodes}")
        return self.paths
    
if __name__ == "__main__":
    example1 = [("GET", "/api/v1/cluster/metrics"),
              ("POST", "/api/v1/cluster/{cluster}/plugins"),
              ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")]
    example2 = [("GET", "/api/v1/cluster/freenodes/list"),
                ("GET", "/api/v1/cluster/nodes"),
                ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
                ("POST", "/api/v1/cluster/{cluster}/plugins")]
    # Создаем экземпляр класса
    tree = BuildTree()
    # Добавляем данные из первого набора
    output1 = tree.add_path(example1)
    print("Result 1: ")
    pprint(output1)
    # Добавляем данные из второго набора
    output2 = tree.add_path(example2)
    # Итоговый результат
    print("Result 2: ")
    pprint(output2)