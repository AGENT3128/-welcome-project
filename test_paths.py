import unittest
from api_paths import BuildTree


class TestParsePaths(unittest.TestCase):

    def test_1(self):
        # Обычный случай
        paths1 = [("GET", "/api/v1/cluster/metrics"),
                 ("POST", "/api/v1/cluster/{cluster}/plugins")]
        paths2 = [("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")]
        
        tree = BuildTree()
        tree.add_path(paths1)
        output = tree.add_path(paths2)
        
        expected_output = {'cluster': {'metrics': 'GET', 'plugins': 'POST'}}
        self.assertEqual(output, expected_output)
    def test_2(self):
        # Проверка на отсутствие дубликатов
        paths1 = [("GET", "/api/v1/cluster/metrics"),
                 ("POST", "/api/v1/cluster/{cluster}/plugins")
                 ]
        paths2 = [("GET", "/api/v1/cluster/metrics"),
                 ("POST", "/api/v1/cluster/{cluster}/plugins"),
                 ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
                 ("GET", "/api/v1/cluster/metrics")]
        tree = BuildTree()
        tree.add_path(paths1)
        output = tree.add_path(paths2)
        expected_output = {'cluster': {'metrics': 'GET', 'plugins': 'POST'}}
        self.assertEqual(output, expected_output)

    def test_3(self):
        # Обработка пустого списка
        paths = []
        expected_output = {}
        self.assertEqual(BuildTree().add_path(paths), expected_output)
    
    def test_4(self):
        # Проверка на разные методы
        paths = [("GET", "/api/v1/cluster/freenodes/list"),
                ("GET", "/api/v1/cluster/nodes"),
                ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
                ("GET", "/api/v1/cluster/{cluster}/plugins")]
    
        with self.assertRaises(Exception):
            BuildTree().add_path(paths)
    
    def test_5(self):
        # Проверка на разные верхушки дерева
        paths = [("GET", "/api/v1/cluster2/metrics"),
                 ("POST", "/api/v1/cluster/{cluster}/plugins"),
                 ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
                 ("POST", "/api/v1/cluster/{cluster}/plugins")]
        with self.assertRaises(Exception):
            BuildTree().add_path(paths)
            
if __name__ == '__main__':
    unittest.main()