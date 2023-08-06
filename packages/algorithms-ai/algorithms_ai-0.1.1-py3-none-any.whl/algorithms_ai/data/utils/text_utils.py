import time

from loguru import logger

ENGLISH_PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
CHINESE_PUNCTUATION = '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
GRToLat = {
    'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta',
    'θ': 'theta', 'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron',
    'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega',

    'Α': 'Alpha', 'Β': 'Beta', 'Γ': 'Gamma', 'Δ': 'Delta', 'Ε': 'Epsilon', 'Ζ': 'Zeta', 'Η': 'Eta',
    'Θ': 'Theta', 'Ι': 'Iota', 'Κ': 'Kappa', 'Λ': 'Lambda', 'Μ': 'Mu', 'Ν': 'Nu', 'Ξ': 'Xi', 'Ο': 'Omicron',
    'Π': 'Pi', 'Ρ': 'Rho', 'Σ': 'Sigma', 'Τ': 'Tau', 'Υ': 'Upsilon', 'Φ': 'Phi', 'Χ': 'Chi', 'Ψ': 'Psi', 'Ω': 'Omega'
}


def is_char_chinese(char):
    # 中文常用字符
    if '\u4e00' <= char <= '\u9fff':
        return True
    else:
        return False


def is_chinese(chars):
    # 中文常用
    for c in chars:
        if is_char_chinese(c):
            return True
    return False


def is_char_english(char):
    if is_char_english_lowercase(char) or is_char_english_uppercase(char):
        return True
    else:
        return False


def is_char_english_lowercase(char):
    # 英文小写常用字符
    if '\u0061' <= char <= '\u007a':
        return True
    else:
        return False


def is_char_english_uppercase(char):
    # 英文大写常用字符
    if '\u0041' <= char <= '\u005a':
        return True
    else:
        return False


def is_number(char):
    if '\u0030' <= char <= '\u0039':
        return True
    else:
        return False


def is_punctuation_chinese(char):
    if char in CHINESE_PUNCTUATION:
        return True
    else:
        return False


def is_punctuation_english(char):
    # 英文标点
    if char in ENGLISH_PUNCTUATION:
        return True
    else:
        return False


def is_punctuation(char):
    if is_punctuation_english(char) or is_punctuation_chinese(char):
        return True
    else:
        return False


def is_greek_uppercase(char):
    # 大写希腊字母
    if '\u0391' <= char <= '\u03a9':
        return True
    else:
        return False


def is_greek_lowercase(char):
    # 小写希腊字母
    if '\u03b1' <= char <= '\u03c9':
        return True
    else:
        return False


def get_left_right_char(raw_text: str, index_text: str, end_index: int):
    # 获取一个字符在文本中的左右字符,end_index指text中最后一个字符的后一个位置（索引时）,起始的左右设置为''
    assert raw_text[end_index - len(index_text):end_index] == index_text
    start_index = end_index - len(index_text)
    if start_index <= 0:
        left = ''
    else:
        left = raw_text[start_index - 1]

    if end_index >= len(raw_text):
        right = ''
    else:
        right = raw_text[end_index]
    return left, right


def format_english_char(char):
    """全角转半角"""
    inside_code = ord(char)
    if inside_code == 12288:  # 全角空格直接转换
        inside_code = 32
    elif 65374 >= inside_code >= 65281:  # 全角字符（除空格）根据关系转化
        inside_code -= 65248
    return chr(inside_code)


def is_cover(a, b):
    # 判断坐标a是否包含坐标b, (1,9)包含（2,8）
    if a[0] <= b[0] and a[-1] >= b[-1]:  # a包含b
        return True
    else:
        return False


def is_subtext_match(raw_text, sub_text, end_index):
    # 判断sub_text在text中是否是tokens_list, 英文短语,数字，end_index是索引的index，是sub_text的索引
    # assert raw_text[end_index-len(sub_text):end_index] == sub_text

    # 判断non-非
    left_part = raw_text[:end_index - len(sub_text)].replace('-', '').rstrip()
    if left_part.endswith('non') or left_part.endswith('非') or left_part.endswith('none') or left_part.endswith('not'):
        return False

    left, right = get_left_right_char(raw_text=raw_text, index_text=sub_text, end_index=end_index)
    if is_char_english(left) and is_char_english(sub_text[0]):  # 'ab'
        return False
    if is_number(left) and is_number(sub_text[0]):  # 12
        return False
    if is_char_english(left) and is_number(sub_text[0]):  # a1
        return False
    if is_number(left) and is_char_english(sub_text[0]):  # 1a
        return False

    if is_char_english(right) and is_char_english(sub_text[-1]):  # 'ba'
        return False
    if is_number(right) and is_number(sub_text[-1]):  # '12'
        return False
    if is_char_english(right) and is_number(sub_text[-1]):  # 'a1'
        return False
    if is_number(right) and is_char_english(sub_text[-1]):  # '1a'
        return False

    return True


def time_spend(func):
    def func_in(*args, **kwargs):
        logger.info(f'start function:{func.__name__}')
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f'end function:{func.__name__}')
        logger.info(f'function：{func.__name__} ,spend time：{round(end_time - start_time, 4)} s')
        return res  # test函数的返回值

    return func_in


def get_run_time(func, *args, **kwargs):
    start_time = time.time()
    res = func(*args, **kwargs)
    end_time = time.time()
    logger.info(f'function：{func.__name__} ,spend time：{round(end_time - start_time, 4)} s')
    return res

import re
decimal_and_integer_re = re.compile("\d+\.?\d+")

def find_decimal_and_integer(text):
    # 找到文本中的小数和整数
    res = decimal_and_integer_re.finditer(text)
    decimals = []
    integers = []
    for i in res:
        if '.' in i.group():
            decimals.append((i.group(),i.start()))
        else:
            integers.append((i.group(),i.start()))
    return decimals, integers

def replace_decimal_and_integer(text):
    # 把文本中的小数变成 【decimical】，整数变成【integer】
    res = decimal_and_integer_re.finditer(text)
    decimals = set()
    integers = set()
    for i in res:
        if '.' in i.group():
            decimals.add(i.group())
        else:
            integers.add(i.group())
    for i in decimals:
        text = text.replace(i, ' [decimal] ')

    for i in integers:
        text = text.replace(i, ' [integer] ')

    return text

if __name__ == '__main__':
    a = 'adsf asdf3.2323sdfsdf3.2323 asdf asdf32'
    replace_decimal_and_integer(a)

