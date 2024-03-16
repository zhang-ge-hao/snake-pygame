import random
import copy

class TreeNode:
    def __init__(self, number):
        self.number = number
        self.operator = None
        self.parent = None
        self.left_offspring = None
        self.right_offspring = None

def factorize(n):
    factors = []
    factor = 2
    while n > 1:
        if n % factor == 0:
            factors.append(factor)
            n = n // factor
        else:
            factor += 1
    return factors

def construct_equation(node: TreeNode):
    rank_map = {"+": 0, "-": 0, "*": 1, "/": 1}
    if node.left_offspring is None:
        return str(node.number)
    left_equation = construct_equation(node.left_offspring)
    right_equation = construct_equation(node.right_offspring)
    if node.left_offspring.operator is not None and rank_map[node.left_offspring.operator] < rank_map[node.operator]:
        left_equation = "(%s)" % left_equation
    if node.right_offspring.operator is not None and rank_map[node.right_offspring.operator] <= rank_map[node.operator]:
        right_equation = "(%s)" % right_equation
    return "%s %s %s" % (left_equation, node.operator, right_equation)

def quiz_generate(integer_digits, length, operators=None):
    if operators is None:
        operators = ["+", "-", "*", "/"]
    operators_without_div = copy.deepcopy(operators)
    operators_without_div.remove("/")
    max_number = 10**integer_digits

    # build a tree with `length` leaf-nodes randomly
    tree = [TreeNode(random.randrange(0, max_number))] # add root initially
    for _ in range(1, length):
        candidates = [node for node in tree if node.left_offspring is None]
        sub_tree_root = random.choice(candidates)
        
        calculate_result = sub_tree_root.number

        if calculate_result == 0:
            operator = random.choice(operators_without_div)
        else:
            operator = random.choice(operators)
        if operator == "+":
            left_number = random.randint(0, calculate_result)
            right_number = calculate_result - left_number
        elif operator == "-":
            left_number = random.randrange(calculate_result, max_number)
            right_number = left_number - calculate_result
        elif operator == "*":
            factors = factorize(calculate_result)
            left_number = 1
            if len(factors) > 0:
                k = random.randrange(0, len(factors))
                for factor in random.sample(factors, k=k):
                    left_number *= factor
            if calculate_result != 0 and random.randint(0, 1) == 1:
                left_number = calculate_result // left_number
            right_number = calculate_result // left_number
        elif operator == "/":
            right_number = random.randint(1, (max_number - 1) // calculate_result)
            left_number = right_number * calculate_result

        sub_tree_root.operator = operator
        left_node = TreeNode(left_number)
        right_node = TreeNode(right_number)
        left_node.parent = sub_tree_root
        right_node.parent = sub_tree_root
        sub_tree_root.left_offspring = left_node
        sub_tree_root.right_offspring = right_node
        tree.append(left_node)
        tree.append(right_node)

    return construct_equation(tree[0]), tree[0].number


if __name__ == "__main__":
    while True:
        quiz, answer = quiz_generate(3, 4)
        print("%s = %s = %s" % (quiz, answer, eval(quiz)))
        assert answer == eval(quiz)
