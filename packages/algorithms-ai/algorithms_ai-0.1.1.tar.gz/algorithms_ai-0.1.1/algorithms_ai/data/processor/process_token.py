# 处理token-word级别

from consts import HTML_ESCAPE_DICT, GRToLat_DICT, PUNCTUATIONS


class TokenProcessor:
    def __init__(self,
                 # 处理
                 lower=False,
                 use_stem=False,  # 词干提取
                 use_lemmatize=False,  # 词性还原

                 # 转换
                 mapping_html_escape=True,  # 映射html转义字符
                 mapping_greek=False,  # 映射希腊字母
                 mapping_digit=False,  # 把数字以及小数映射为【NUM】
                 mapping_special_token: dict = None,  # 自定义特殊字符的映射

                 #  去除
                 stopwords=(),  # 需要去除的token序列
                 remove_punctuations=False,  # token是标点的是否为‘’
                 ):
        self.lower = lower
        if use_lemmatize:
            self.lemmatizer = self.get_lemmatizer()
        else:
            self.lemmatizer = None
        if use_stem:
            self.stemmer = self.get_stemmer(method='poreter')
        else:
            self.stemmer = None

        # 把一个token映射为另一个
        self.token_mapping = dict()
        if mapping_html_escape:
            self.token_mapping.update(HTML_ESCAPE_DICT)
        if mapping_greek:
            for i, j in GRToLat_DICT:
                self.token_mapping[i] = ' ' + j + ' '
        if mapping_special_token:
            self.token_mapping.update(mapping_special_token)
        self.mapping_digit = mapping_digit

        # token满足某个条件则移除，即映射为‘’
        self.token_remove = []
        self.token_remove.extend(stopwords)
        if remove_punctuations:
            self.token_remove.extend(list(PUNCTUATIONS))

    def run(self, token_text: str):
        if self.lower:
            token_text = token_text.lower()

        if self.lemmatizer:
            token_text = self.lemmatizer(token_text)

        if self.stemmer:
            token_text = self.stemmer(token_text)

        if token_text in self.token_mapping:
            token_text = self.token_mapping[token_text]

        if self.mapping_digit:
            token_text = self.map_num_to_special_token(token_text)

        if token_text in self.token_remove:
            return ''

        return token_text.strip()

    @staticmethod
    def map_num_to_special_token(token_text, special_token='[NUM]'):
        # 把数字和小数映射为特殊token
        if token_text.isdigit() or (token_text.count('.') == 1 and token_text[0:token_text.find('.')].isdigit()
                                    and token_text[token_text.find('.') + 1:].isdigit()):
            return special_token
        else:
            return token_text

    @staticmethod
    def get_stemmer(method='poreter'):
        # 词干提取（例如：dysfunctional  -> dysfunct）
        if method == 'lancaster':
            from nltk.stem.lancaster import LancasterStemmer
            stemmer = LancasterStemmer()
        elif method == 'snowball':
            from nltk.stem import SnowballStemmer
            stemmer = SnowballStemmer('english')
        else:
            from nltk.stem.porter import PorterStemmer
            stemmer = PorterStemmer()
        return stemmer.stem  # usage: stemmer.stem('...')

    @staticmethod
    def get_lemmatizer():
        # 词性还原（例如：dysfunct -> dysfunctional）,复数变成单数
        from nltk.stem.wordnet import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()  # 词形还原
        return lemmatizer.lemmatize  # usage: lemmatizer.lemmatize('...')

    def pos_tag(self, token):
        """ 词性标注
        CC  并列连词          NNS 名词复数        UH 感叹词
        CD  基数词              NNP 专有名词        VB 动词原型
        DT  限定符            NNP 专有名词复数    VBD 动词过去式
        EX  存在词            PDT 前置限定词      VBG 动名词或现在分词
        FW  外来词            POS 所有格结尾      VBN 动词过去分词
        IN  介词或从属连词     PRP 人称代词        VBP 非第三人称单数的现在时
        JJ  形容词            PRP$ 所有格代词     VBZ 第三人称单数的现在时
        JJR 比较级的形容词     RB  副词            WDT 以wh开头的限定词
        JJS 最高级的形容词     RBR 副词比较级      WP 以wh开头的代词
        LS  列表项标记         RBS 副词最高级      WP$ 以wh开头的所有格代词
        MD  情态动词           RP  小品词          WRB 以wh开头的副词
        NN  名词单数           SYM 符号            TO  to
        """
        if not hasattr(self, 'pos_tag_word'):
            from nltk import pos_tag
            self.pos_tag_word = pos_tag
        return self.pos_tag_word([token])

    def get_synonym(self, word):
        # wordnet 语义同义词
        if not hasattr(self, 'syn_word'):
            from nltk.corpus import wordnet
            self.syn_word = wordnet.synsets
        return self.syn_word(word)

    @staticmethod
    def other_code():
        # def correct_text(self):
        #     from textblob import TextBlob
        #     str(TextBlob(x).correct())
        ########################
        #     def generate_ngram_token(self, n, token_list: list):
        #         # # n-gram dict , n=token_length ,n最小为1 ， n>=1
        #         return [" ".join(token_list[i:i + n]) for i in range(0, len(token_list) - n + 1)]
        ###########
        # # Taken from Gensim
        # def deaccent(text):
        #     """
        #     Remove accentuation from the given string.
        #     """
        #     norm = unicodedata.normalize("NFD", text)
        #     result = "".join(ch for ch in norm if unicodedata.category(ch) != 'Mn')
        #     return unicodedata.normalize("NFC", result)
        #################
        # def data_clean(x):
        # def normalize_text(self, text):
        #     # 规范化文本，主要是将字符或token变成另外的字符
        #     if self.remove_tag:
        # from bs4 import BeautifulSoup
        #         text = BeautifulSoup(text, "lxml").text
        #
        #     if self.is_lower:
        #         text = text.lower()
        #     return text
        #  if self.normalize_unicode:
        #             # 规范化 unicode 字符 ，比如\u2002
        #             # NFC表示字符应该是整体组成(比如可能的话就使用单一编码)，而NFD表示字符应该分解为多个组合字符表示
        #             from unicodedata import normalize as u_normalize
        #             text = u_normalize("NFKC", text)
        #         if self.remove_illegal_chars:
        #             # 移除非法字符,比如存储openxyl时
        # ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
        #             text = ILLEGAL_CHARACTERS_RE.sub(r'', text)
        #         if self.remove_invisible_chars:
        #             # 移除所有不可见字符，包括：'\t', '\n', '\r'
        #             text = ''.join(t for t in text if t.isprintable())
        #         if self.remove_multi_space:
        #             # 删除多个空格
        #             text = re.sub('\s{2,}', " ", text)
        #     x = x.lower()                                # 所有字母转为小写
        #     x = ' '.join([word for word in x.split(' ') if word not in stop_words])  # 删除停用词
        #     x = x.encode('ascii', 'ignore').decode()     # 删除 unicode 字符（乱码,例如：pel韈ula）
        #     x = re.sub("@\S+", " ", x)                   # 删除提及(例如：@zhangsan)
        #     x = re.sub("https*\S+", " ", x)              # 删除URL链接
        #     x = re.sub("#\S+", " ", x)                   # 删除标签（例如：#Amazing）
        #     x = re.sub("\'\w+", '', x)                   # 删除记号和下一个字符（例如：he's）
        #     x = re.sub(r'[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！\[\\\]^_`{|}~]+', ' ', x)   # 删除特殊字符
        #     x = re.sub(r'\w*\d+\w*', '', x)              # 删除数字
        #     x = re.sub('\s{2,}', " ", x)                 # 删除2个及以上的空格
        #     x = x.strip()                                # 删除两端无用空格
        #     x = str(TextBlob(x).correct())               # 拼写校对  ->  速度慢
        #     x = " ".join([st.stem(word) for word in x.split()])            # 词干提取（例如：dysfunctional  -> dysfunct）
        #     x = " ".join([Word(word).lemmatize() for word in x.split()])   # 词性还原（例如：dysfunct -> dysfunctional）
        #     #  x = re.sub(u'[\u4e00-\u9fa5]', ' ', x)  # 删除英文中的中文字符
        #     x = x.split()     # 分词

        # import unicodedata
        # def strip_accents(s):
        #     return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
        pass


if __name__ == '__main__':
    token_processor = TokenProcessor(
        lower=False,
        use_stem=False,  # 词干提取
        use_lemmatize=False,  # 词性还原

        # 转换
        mapping_html_escape=True,  # 映射html转义字符
        mapping_greek=False,  # 映射希腊字母
        mapping_digit=False,  # 把数字以及小数映射为【NUM】
        mapping_special_token={'.': '1'},  # 自定义特殊字符的映射

        #  去除
        stopwords=(),  # 需要去除的token序列
        remove_punctuations=False,  # token是标点的是否为‘’
    )
    import nltk

    # nltk.download('omw-1.4')
    print(token_processor.run('names'))
