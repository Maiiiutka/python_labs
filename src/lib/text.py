import re
from typing import Dict, List, Tuple

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True):
    if not text:
        return ""
    
    result = text
    
    if yo2e:
        result = result.replace('ё', 'е').replace('Ё', 'Е')
    
    if casefold:
        result = result.casefold()
    
    control_chars = {'\\t', '\\r', '\\n'}
    for char in control_chars:
        result = result.replace(char, ' ')
    
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result


def tokenize(text: str):
    if not text:
        return []
    pattern = r'\w+(?:-\w+)*'
    tokens = re.findall(pattern, text)
    
    return tokens


def count_freq(tokens: List[str]):
    freq_dict = {}
    
    for token in tokens:
        if not token or not any(c.isalpha() for c in token):
            continue
            
        freq_dict[token] = freq_dict.get(token, 0) + 1
    
    return freq_dict


#def top_n(freq: Dict[str, int], n: int = 5) -> List[Tuple[str, int]]:
    if not freq:
        return []
    
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    
    return sorted_items[:n]

def top_n(data, n: int = 5):
    freq = {}
    
    if isinstance(data, list):
        freq = count_freq(data)
    elif isinstance(data, dict):
        freq = data
    else:
        return []
    
    if not freq:
        return []
    
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    
    return sorted_items[:n]

#x = int(input())

#if x == 1:
#    s = input()
#    a = normalize(s)
#    print(a)
#elif x == 2:
#    s = input()
#    a = tokenize(s)
#    print(a)
#elif x == 3:
#    s = input()
#    a = count_freq(s)
#    print(a)
#elif x == 4:
#    s = input()
#    n = int(input())
#    s_clean = s.strip('[]\"\'')
#    items = [item.strip(' \"\'') for item in s_clean.split(',') if item.strip()]
#    a = top_n(items, n)
#    print(a)