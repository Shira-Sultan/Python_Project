import ast

# שומר את מספר הבעיות לכל סוג בעיה
dict_problems = {
    "functions_length": 0,
    "file_length": 0,
    "find_unused_variables": 0,
    "find_missing_docstrings": 0
}

def get_functions_length(code):
    tree = ast.parse(code)  # מנתח את הקוד ל-AST
    func_length = {}  # מילון לשמירת מספר השורות של כל פונקציה

    for node in ast.walk(tree):  # עובר על כל הצמתים בעץ
        if isinstance(node, ast.FunctionDef):  # אם הצומת הוא פונקציה
            start_line = node.lineno  # שורת התחלה של הפונקציה
            end_line = node.end_lineno  # שורת סיום של הפונקציה
            length = end_line - start_line + 1  # סופר את השורות
            if length > 20:
                dict_problems["functions_length"] += 1  # עדכון המילון
            func_length[node.name] = length  # שומר את מספר השורות במילון
    return func_length


def get_file_length(code):
    tree = ast.parse(code)

    # סופר את השורות על סמך השורות של כל נוד בפעולה
    total_lines = 0
    for node in ast.walk(tree):
        if hasattr(node, 'lineno'):
            total_lines = max(total_lines, node.lineno)

    if total_lines > 200:
        dict_problems["file_length"] += 1
    return total_lines


def get_find_unused_variables(code):
    assigned_vars = set()
    used_vars = set()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                assigned_vars.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                used_vars.add(node.id)

    unused_vars = assigned_vars - used_vars
    dict_problems["find_unused_variables"] += len(unused_vars)
    return unused_vars


def get_find_missing_docstrings(code):
    tree = ast.parse(code)
    missing_docs = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            docstring = ast.get_docstring(node)
            if docstring is None:
                missing_docs.append((node.name, node.lineno, type(node).__name__))
                dict_problems["find_missing_docstrings"] += 1

    return missing_docs
