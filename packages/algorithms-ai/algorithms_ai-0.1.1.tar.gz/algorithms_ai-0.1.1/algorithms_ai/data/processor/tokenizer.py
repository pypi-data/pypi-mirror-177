import re

from consts import TOKEN, PUNCTUATIONS, HTML_ESCAPE_DICT


class WordTokenizer:
    def __init__(self, regex=None, keep_words=()):
        # 规则切词，可以保留哪些词不用切分

        html_escape = list(HTML_ESCAPE_DICT.keys())
        # 同一个字符开头满足多个规则，以第一个规则作数
        if not regex:
            # 数字（整数和小数）| 英文单词 | 空白符 | 中文 | 希腊大写字母 | 希腊小写字母 | 标点 | 其他字符
            regex = f"\d+\.?\d+|[A-Za-z]+|\s+|[\u4e00-\u9fa5]|[\u0391-\u03a9]|[\u03b1-\u03c9]|[{PUNCTUATIONS}]|[^a-zA-Z0-9{PUNCTUATIONS}\s\u4e00-\u9fa5\u03b1-\u03c9\u0391-\u03a9]"
            regex = '|'.join(html_escape) + '|' + regex
        if keep_words:
            regex = '|'.join(keep_words) + '|' + regex
        self.find_re = re.compile(regex)

    def run(self, text):
        # 输入文本，输出切分后的文本以及坐标--start-end--- 最后一个字符的坐标，而不是索引
        res = []
        tmp_index = 0

        token_index = 0
        for i in self.find_re.finditer(text):
            if tmp_index < i.start():
                if text[tmp_index:i.start()].strip():
                    res.append(TOKEN(
                        index=token_index,
                        start_offset=tmp_index,
                        end_offset=i.start() - 1,
                        text=text[tmp_index:i.start()],
                        label='O'))
                    token_index+=1
            if i.group().strip():
                res.append(TOKEN(token_index,i.start(), i.end() - 1, i.group(), 'O'))
                token_index += 1
            tmp_index = i.end()

        if (tmp_index < len(text)) and (text[tmp_index:len(text) - 1].strip()):

            res.append(TOKEN(token_index,tmp_index, len(text) - 1, text[tmp_index:len(text) - 1], 'O'))
            token_index += 1
        return res  # [Token(start,end,text)]

    # def _cut_sentence_to_words_zh(self, sentence: str):
#         english = 'abcdefghijklmnopqrstuvwxyz0123456789αγβδεζηθικλμνξοπρστυφχψω'
#         output = []
#         buffer = ''
#         for s in sentence:
#             if s in english or s in english.upper():  # 英文或数字
#                 buffer += s
#             else:  # 中文
#                 if buffer:
#                     output.append(buffer)
#                 buffer = ''
#                 output.append(s)
#         if buffer:
#             output.append(buffer)
#         return output

    # def get_word_tokenizer(self, method='nltk_word_tokenizer'):
    #     if method == 'nltk_word_tokenizer':
    #         word_tokenizer = nltk.NLTKWordTokenizer().tokenize
    #     elif method == 'nltk_word_tokenizer_span':
    #         word_tokenizer = nltk.WordPunctTokenizer().tokenize
    #     elif method == 'm2':
    #         word_tokenizer = ''
    #         pass
    #         # from transformers import BasicTokenizer
    #         # BasicTokenizer(do_lower_case=False).tokenize()
    #     else:
    #         word_tokenizer = re.compile(r'[，,:：;；\s]').split
    #     return word_tokenizer


class SentenceTokenizer:
    def __init__(self, keep_suffix=()):
        from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
        punkt_param = PunktParameters()

        abbreviation = ['et al.', 'i.e.', 'e.g.', 'etc.', 'i.e', 'e.g', 'etc', ' et al']
        if keep_suffix:
            abbreviation.extend(list(keep_suffix))
        punkt_param.abbrev_types = set(abbreviation)
        self.sentence_tokenizer = PunktSentenceTokenizer(punkt_param, verbose=True).tokenize

    def run(self, text):
        tokens = self.sentence_tokenizer(text)
        end = 0
        token_index = 0
        all_token_span = []
        for each_token in tokens:
            all_token_span.append(TOKEN(
                token_index,
                text[end:].find(each_token) + end,
                text[end:].find(each_token) + end + len(each_token) - 1,  # 坐标而不是索引
                each_token,
                'O'
            ))
            token_index+=1
            end += len(each_token)
        return all_token_span  # sentence_token , start ,end


#     def _cut_paragraph_to_sentences_zh(self, para: str, drop_empty_line=True, strip=True, deduplicate=False):
#         """
#         Args:
#            para: 输入文本
#            drop_empty_line: 是否丢弃空行
#            strip:  是否对每一句话做一次strip
#            deduplicate: 是否对连续标点去重，帮助对连续标点结尾的句子分句
#
#         Returns:
#            sentences: list of str
#         """
#         if deduplicate:
#             para = re.sub(r"([。！？\!\?])\1+", r"\1", para)
#
#         para = re.sub('([。！？\?!])([^”’])', r"\1\n\2", para)  # 单字符断句符
#         para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
#         para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
#         para = re.sub('([。！？\?!][”’])([^，。！？\?])', r'\1\n\2', para)
#         # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
#         para = para.rstrip()  # 段尾如果有多余的\n就去掉它
#         # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
#         sentences = para.split("\n")
#         if strip:
#             sentences = [sent.strip() for sent in sentences]
#         if drop_empty_line:
#             sentences = [sent for sent in sentences if len(sent.strip()) > 0]
#         return sentences


if __name__ == '__main__':
    s4 = "CX (cisplatin 80 mg/m(2) IV Q3W; capecitabine 1000 mg/m(2) P.O. BID for 14 days Q3W) plus intravenous AMG 386 10 mg/kg QW (Arm A"
    t = SentenceTokenizer(keep_suffix=('s.v',))

    print(t.run(s4))

    s = "Oral acalabruti(nib) 100 mg 我i在发啊 <  twic\u00b7e daily  ; was & admi\nnister\ted with or &lt; 13.8kg/m without,α-1 12.😊 "
    w_t = WordTokenizer(regex=None, keep_words=('在发',))
    print(w_t.run(s))
