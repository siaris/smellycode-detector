import os
import re

def detect_switch_case_smell(content, min_cases=5):
    smells = []
    switch_blocks = re.finditer(r'switch\s*\(.*?\)\s*{[^}]+}', content, re.DOTALL)

    for block in switch_blocks:
        code_block = block.group()
        cases = re.findall(r'\bcase\b\s+\d+', code_block)
        if len(cases) >= min_cases:
            smells.append(("Long switch-case", len(cases), code_block[:200]))
    return smells

def detect_long_methods(content, threshold=30):
    long_methods = []
    pattern = re.finditer(r'(function|def)\s+\w+\s*\([^)]*\)\s*{?', content)

    for match in pattern:
        start = match.start()
        method_code = content[start:]
        lines = method_code.splitlines()
        count = 0

        for line in lines:
            count += 1
            if re.match(r'^\s*}', line) or count > threshold:
                break

        if count >= threshold:
            long_methods.append(("Long method", count, match.group()))
    return long_methods

def detect_deep_nesting(content, threshold=4):
    lines = content.splitlines()
    deep_lines = []

    for i, line in enumerate(lines):
        indent = len(line) - len(line.lstrip())
        if indent // 4 >= threshold:
            deep_lines.append(("Deep nesting", i + 1, line.strip()))
    return deep_lines

def detect_long_if_else(content, threshold=4):
    long_chains = []
    chains = re.findall(r'(if\s*\(.*?\)\s*{(?:\s*else\s*if\s*\(.*?\)\s*{)*\s*})', content, re.DOTALL)

    for chain in chains:
        count = len(re.findall(r'else\s*if', chain))
        if count >= threshold:
            long_chains.append(("Long if-else chain", count, chain[:200]))
    return long_chains

def detect_magic_numbers(content):
    matches = re.findall(r'[^a-zA-Z0-9](\d{2,})[^a-zA-Z0-9]', content)
    return [("Magic number", m) for m in set(matches)]

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    results = []
    results.extend(detect_switch_case_smell(content))
    results.extend(detect_long_methods(content))
    results.extend(detect_deep_nesting(content))
    results.extend(detect_long_if_else(content))
    results.extend(detect_magic_numbers(content))

    if results:
        print(f"\n📄 {filepath}")
        for item in results:
            print(f"  - {item[0]}: {item[1]}\n    → {str(item[2])[:100]}...")

def traverse_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.js', '.ts', '.jsx', '.py')):
                analyze_file(os.path.join(root, file))

if __name__ == '__main__':
    folder_to_scan = './src'
    traverse_folder(folder_to_scan)
