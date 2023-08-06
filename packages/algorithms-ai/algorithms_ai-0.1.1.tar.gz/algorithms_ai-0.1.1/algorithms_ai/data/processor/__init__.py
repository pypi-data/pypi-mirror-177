# # 数据预处理、
# # stem
# # 标点
# # 替换不重要的词
# # 低频词用UNK
#
# #词根化-删除词缀（后缀、前缀、中缀），例如，running 变成run
#
# # 词形还原-捕获单词的原本词形。例如，better变成good[4]
# # 用NUM替换数字之类的
# # 减少vocabulary大小
#
# #3 clean_token=[]
# for token in word_punct_token:
#     token = token.lower()
#     # 删除任何非字母的值
#     new_token = re.sub(r'[^a-zA-Z]+', '', token)
#     # 删除空值和单个字符值
#     if new_token != "" and len(new_token) >= 2:
#         vowels=len([v for v in new_token if v in "aeiou"])
#         if vowels != 0: # 删除只包含辅音的行
#             clean_token.append(new_token)
#
# # 获取停用词列表
# stop_words = stopwords.words('english')
# # 在列表中添加新的停用词
# stop_words.extend(["could","though","would","also","many",'much'])
#
#
# # 词干化和词形还原都有助于减少词汇的维数，方法是将单词还原为词根形式（词形还原）或删除所有后缀、词缀、前缀等（词干化）。
# #
# # 词干分析有助于减少词汇的维数，但大多数情况下，词干分析会变得毫无意义，因为词干分析只会切掉词尾，而不会将单词还原为基本形式。例如，houses在删除后会变成hous，完全失去意义。因此，词形还原对于文本分析更为可取。
# #
# # 以下脚本用于获取名词、形容词和动词的词形还原形式。
#
#
# # 替换为单个字符以简化
# df = df.replace(['NN', 'NNS', 'NNP', 'NNPS'], 'n')
# df = df.replace(['JJ', 'JJR', 'JJS'], 'a')
# df = df.replace(['VBG', 'VBP', 'VB', 'VBD', 'VBN', 'VBZ'], 'v')
#
# '''
# 定义一个函数，当tagset是名词时，词形还原；当标识集是形容词时，取词形还原的形容词
# '''
# df_lemmatized = df.copy()
# df_lemmatized['Tempt Lemmatized Word'] = df_lemmatized['Lemmatized Noun'] + ' | ' + df_lemmatized[
#     'Lemmatized Adjective'] + ' | ' + df_lemmatized['Lemmatized Verb']
#
# df_lemmatized.head(5)
# lemma_word = df_lemmatized['Tempt Lemmatized Word']
# tag = df_lemmatized['Tag']
# i = 0
# new_word = []
# while i < len(tag):
#     words = lemma_word[i].split('|')
#     if tag[i] == 'n':
#         word = words[0]
#     elif tag[i] == 'a':
#         word = words[1]
#     elif tag[i] == 'v':
#         word = words[2]
#     new_word.append(word)
#     i += 1
#
# df_lemmatized['Lemmatized Word'] = new_word
#
# 将形容词、名词和动词分开进行词形还原是为了提高lemmatizer的准确性。
#
# import re
# from collections import namedtuple
#
# Token = namedtuple('Token', ['type', 'value'])
#
#
# def lexer(text):
#     IDENTIFIER = r'(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z_0-9]*)'
#     ASSIGNMENT = r'(?P<ASSIGNMENT>=)'
#     NUMBER = r'(?P<NUMBER>\d+)'
#     MULTIPLIER_OPERATOR = r'(?P<MULTIPLIER_OPERATOR>[*/])'
#     ADDING_OPERATOR = r'(?P<ADDING_OPERATOR>[+-])'
#     WHITESPACE = r'(?P<WHITESPACE>\s+)'
#     EOF = r'(?P<EOF>\Z)'
#     ERROR = r'(?P<ERROR>.)'  # catch everything else, which is an error
#
#     tokenizer = re.compile(
#         '|'.join([IDENTIFIER, ASSIGNMENT, NUMBER, MULTIPLIER_OPERATOR, ADDING_OPERATOR, WHITESPACE, EOF, ERROR]))
#     seen_error = False
#     for m in tokenizer.finditer(text):
#         if m.lastgroup != 'WHITESPACE':  # ignore whitespace
#             if m.lastgroup == 'ERROR':
#                 if not seen_error:
#                     yield Token(m.lastgroup, m.group())
#                     seen_error = True  # scan until we find a non-error input
#             else:
#                 yield Token(m.lastgroup, m.group())
#                 seen_error = False
#         else:
#             seen_error = False
#
#
# for token in lexer('foo = x12 * y / z - 3'):
#     print(token)
#
