class TreeNode:
    def __init__(self, value=None, children=None, is_max=True, index=None):
        self.value = value  # Значение листа
        self.children = children if children else []  # Дочерние узлы
        self.is_max = is_max  # True для MAX, False для MIN
        self.index = index  # Индекс узла для удобного вывода

# Функция для отображения дерева
def display_tree(root, depth=0, indent=""):
    if root is None:
        print(f"{indent}Пустой узел")
        return
    # Проверка, является ли текущий узел листом
    if root.value is not None:
        print(f"{indent}Лист {root.index}: оценка = {root.value}")
    else:
        # Определение типа узла (MAX или MIN)
        player_type = "MAX" if root.is_max else "MIN"
        print(f"{indent}Узел {player_type} {root.index}:")
    # Рекурсивное отображение дочерних узлов
    for child in root.children:
        display_tree(child, depth + 1, indent + "    ")


# Реализация минимаксного алгоритма
def minimax(node, depth, is_max_turn, display=True): # Если display=False, то вывод отключен
    # Устанавливаем отступ для вывода, чтобы показать текущую глубину узла в дереве
    indent = "    " * depth
    # Если у узла нет дочерних узлов, значит, он является листом
    if not node.children:
        if display:
            print(f"{indent}Лист {node.index} -> {node.value}")
        return node.value  # Возвращаем значение листа как итоговую оценку для этого узла
    # Если текущий узел - это узел MAX
    if is_max_turn:
        # Инициализируем максимальное значение как отрицательную бесконечность, поскольку будем искать максимальную оценку среди дочерних узлов
        max_eval = float('-inf')
        if display:
            print(f"{indent}Узел MAX {node.index}:")
        # Обходим всех дочерних узлов, чтобы найти наилучшее значение для узла MAX
        for child in node.children:
            # Рекурсивно вызываем minimax для дочернего узла, переключая ход на MIN
            eval = minimax(child, depth + 1, False, display)
            # Обновляем максимальное значение, если текущая оценка выше
            max_eval = max(max_eval, eval)
        if display:
            print(f"{indent}Оценка узла MAX {node.index} -> {max_eval}")
        # Возвращаем максимальное найденное значение, так как это узел MAX
        return max_eval
    # Если текущий узел - это узел MIN
    else:
        # Инициализируем минимальное значение как положительную бесконечность, поскольку будем искать минимальную оценку среди дочерних узлов
        min_eval = float('inf')
        if display:
            print(f"{indent}Узел MIN {node.index}:")
        # Обходим всех дочерних узлов, чтобы найти наименьшее значение для узла MIN
        for child in node.children:
            # Рекурсивно вызываем minimax для дочернего узла, переключая ход на MAX
            eval = minimax(child, depth + 1, True, display)
            # Обновляем минимальное значение, если текущая оценка ниже
            min_eval = min(min_eval, eval)
        if display:
            print(f"{indent}Оценка узла MIN {node.index} -> {min_eval}")
        # Возвращаем минимальное найденное значение, так как это узел MIN
        return min_eval

# Реализация алгоритма с альфа-бета отсечениями
def alpha_beta_pruning(node, depth, alpha, beta, is_max_turn, direction, display=True):
    indent = "    " * depth  # Отступ
    if not node.children:  # Проверка, является ли узел листом
        if display:
            print(f"{indent}Лист {node.index} -> {node.value}")  # Вывод значения листа
        return node.value  # Возвращаем значение листа как итоговую оценку для этого узла
    # Если это ход MAX
    if is_max_turn:
        max_eval = float('-inf')  # Инициализация максимальной оценки как отрицательной бесконечности
        # Определение порядка анализа дочерних узлов: слева-направо или справа-налево
        child_nodes = node.children if direction == 'left' else node.children[::-1]
        if display:
            print(f"{indent}Узел MAX {node.index}:")
        for child in child_nodes:
            # Рекурсивный вызов для дочерних узлов с передачей переключенного флага is_max_turn
            eval = alpha_beta_pruning(child, depth + 1, alpha, beta, False, direction, display)
            max_eval = max(max_eval, eval)  # Обновление максимальной оценки для узла MAX
            alpha = max(alpha, eval)  # Обновление альфа-границы для узла MAX
            if beta <= alpha:  # Проверка условия отсечения
                if display:
                    print(f"{indent}Отсечены ветви на узле {node.index}")
                break  # Прерывание цикла при выполнении условия отсечения
        if display:
            print(f"{indent}Оценка узла MAX {node.index} -> {max_eval}")
        return max_eval  # Возврат наибольшей оценки для узла MAX
    else:  # Если это ход MIN
        min_eval = float('inf')  # Инициализация минимальной оценки как положительной бесконечности
        # Определение порядка анализа дочерних узлов: слева-направо или справа-налево
        child_nodes = node.children if direction == 'left' else node.children[::-1]
        if display:
            print(f"{indent}Узел MIN {node.index}:")  # Сообщение о начале анализа узла MIN
        for child in child_nodes:
            # Рекурсивный вызов для дочерних узлов с передачей переключенного флага is_max_turn
            eval = alpha_beta_pruning(child, depth + 1, alpha, beta, True, direction, display)
            min_eval = min(min_eval, eval)  # Обновление минимальной оценки для узла MIN
            beta = min(beta, eval)  # Обновление бета-границы для узла MIN
            if beta <= alpha:  # Проверка условия отсечения
                if display:
                    print(f"{indent}Отсечена ветвь на узле {node.index}")
                break  # Прерывание цикла при выполнении условия отсечения
        if display:
            print(f"{indent}Оценка узла MIN {node.index} -> {min_eval}")
        return min_eval  # Возврат наименьшей оценки для узла MIN


# Функция для создания дерева
def create_game_tree():
    # Уровень 5: листья
    leaves = [
        TreeNode(value=4), TreeNode(value=5), TreeNode(value=6), TreeNode(value=5),
        TreeNode(value=6), TreeNode(value=3), TreeNode(value=1), TreeNode(value=7),
        TreeNode(value=8), TreeNode(value=9), TreeNode(value=8), TreeNode(value=8),
        TreeNode(value=9), TreeNode(value=9), TreeNode(value=9), TreeNode(value=3),
        TreeNode(value=2), TreeNode(value=8), TreeNode(value=6), TreeNode(value=8),
        TreeNode(value=7), TreeNode(value=9), TreeNode(value=8), TreeNode(value=9),
        TreeNode(value=3), TreeNode(value=4), TreeNode(value=5), TreeNode(value=4),
        TreeNode(value=2), TreeNode(value=3), TreeNode(value=2), TreeNode(value=6),
        TreeNode(value=8), TreeNode(value=8), TreeNode(value=8), TreeNode(value=9)
    ]

    # Уровень 4: узлы, соединяющие листья
    level4 = [
        TreeNode(children=leaves[0:2], is_max=False, index="L41"),
        TreeNode(children=leaves[2:4], is_max=False, index="L42"),
        TreeNode(children=leaves[4:7], is_max=False, index="L43"),
        TreeNode(children=leaves[7:9], is_max=False, index="L44"),
        TreeNode(children=leaves[9:12], is_max=False, index="L45"),
        TreeNode(children=leaves[12:15], is_max=False, index="L46"),
        TreeNode(children=leaves[15:17], is_max=False, index="L47"),
        TreeNode(children=leaves[17:19], is_max=False, index="L48"),
        TreeNode(children=leaves[19:21], is_max=False, index="L49"),
        TreeNode(children=leaves[21:24], is_max=False, index="L410"),
        TreeNode(children=leaves[24:26], is_max=False, index="L411"),
        TreeNode(children=leaves[26:28], is_max=False, index="L412"),
        TreeNode(children=leaves[28:31], is_max=False, index="L413"),
        TreeNode(children=leaves[31:33], is_max=False, index="L414"),
        TreeNode(children=leaves[33:36], is_max=False, index="L415")
    ]

    # Уровень 3: узлы, соединяющие уровень 4
    level3 = [
        TreeNode(children=level4[0:3], is_max=True, index="M31"),
        TreeNode(children=level4[3:6], is_max=True, index="M32"),
        TreeNode(children=level4[6:8], is_max=True, index="M33"),
        TreeNode(children=level4[8:11], is_max=True, index="M34"),
        TreeNode(children=level4[11:13], is_max=True, index="M35"),
        TreeNode(children=level4[13:15], is_max=True, index="M36")
    ]

    # Уровень 2: узлы, соединяющие уровень 3
    level2 = [
        TreeNode(children=level3[0:2], is_max=False, index="L21"),
        TreeNode(children=level3[2:4], is_max=False, index="L22"),
        TreeNode(children=level3[4:6], is_max=False, index="L23")
    ]

    # Уровень 1: корневой узел
    root = TreeNode(children=level2, is_max=True, index="M1")

    return root


# Интерфейс программы
def interface(tree):

    print("Выберите алгоритм:\n1. Минимакс\n2. Альфа-бета отсечения")
    algo_choice = input("Ваш выбор: ")

    if algo_choice == '1':
        print("Кто начинает первым?\n1. MAX\n2. MIN")
        first_player = input("Ваш выбор: ")
        is_max_first = True if first_player == '1' else False
        print("\nИсходное дерево:")
        display_tree(tree)
        print("\nЗапуск минимакс алгоритма...\n")
        result = minimax(tree, 0, is_max_first)
        print(f"\nОкончательный результат минимакс: {result}")
    elif algo_choice == '2':
        print("Выберите порядок анализа:\n1. Слева-направо\n2. Справа-налево")
        order_choice = input("Ваш выбор: ")
        direction = 'left' if order_choice == '1' else 'right'
        print("Кто начинает первым?\n1. MAX\n2. MIN")
        first_player = input("Ваш выбор: ")
        is_max_first = True if first_player == '1' else False
        print("\nИсходное дерево:")
        display_tree(tree)
        print("\nЗапуск алгоритма альфа-бета отсечений...\n")
        result = alpha_beta_pruning(tree, 0, float('-inf'), float('inf'), is_max_first, direction)
        print(f"\nОкончательный результат альфа-бета: {result}")

    # Введение функции для изменения оценок листьев
    modify_leaves(tree)


# Функция для изменения оценок листьев
def modify_leaves(tree):
    print("\nХотите изменить значения листьев? (да/нет)")
    response = input("Ваш выбор: ").strip().lower()

    if response == 'да':
        new_values = []  # Список для хранения новых значений листьев
        print("Введите 36 новых значений листьев (только числа от 0 до 9):")

        # Цикл для ввода 36 значений с проверкой
        for i in range(1, 37):
            while True:
                try:
                    value = int(input(f"{i}. "))
                    # Проверка, чтобы значение было от 0 до 9
                    if 0 <= value <= 9:
                        new_values.append(value)
                        break
                    else:
                        print("Ошибка: введите число от 0 до 9.")
                except ValueError:
                    print("Ошибка: введите только число от 0 до 9.")

        # Функция для нахождения всех листьев в дереве
        def get_leaves(node):
            leaves = []
            if node.children:
                for child in node.children:
                    leaves.extend(get_leaves(child))
            else:
                leaves.append(node)
            return leaves

        # Получаем все листья дерева
        leaf_nodes = get_leaves(tree)

        # Проверка, чтобы количество листьев соответствовало количеству введенных значений
        if len(leaf_nodes) != len(new_values):
            print("Ошибка: количество листьев не соответствует количеству введенных значений.")
            return

        # Присваиваем новые значения листьям
        for node, new_value in zip(leaf_nodes, new_values):
            node.value = new_value

        print("Значения листьев обновлены!")
        print("\nИзменённое дерево:")
        display_tree(tree)
        interface(tree)

    else:
        print("Значения листьев остались без изменений.")


# Запуск программы
if __name__ == "__main__":
    tree = create_game_tree()
    interface(tree)
