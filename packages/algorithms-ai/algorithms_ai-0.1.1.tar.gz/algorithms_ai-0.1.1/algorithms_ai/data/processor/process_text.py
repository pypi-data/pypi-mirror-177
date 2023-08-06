from consts import TOKEN
from process_token import TokenProcessor
from tokenizer import WordTokenizer


class TextProcessor:
    def __init__(self, word_tokenizer=None, token_processor=None):
        if not word_tokenizer:
            self.word_tokenizer = WordTokenizer(regex=None, keep_words=()).run
        else:
            self.word_tokenizer = word_tokenizer

        if not token_processor:
            self.token_processor = TokenProcessor(
                lower=False,
                use_stem=False,  # 词干提取
                use_lemmatize=False,  # 词性还原
                mapping_html_escape=True,  # 映射html转义字符
                mapping_greek=False,  # 映射希腊字母
                mapping_digit=False,  # 把数字以及小数映射为【NUM】
                mapping_special_token=dict(),  # 自定义特殊字符的映射
                stopwords=(),  # 需要去除的token序列
                remove_punctuations=False).run
        else:
            self.token_processor = token_processor

    def simple_process_input_text(self, input_text):
        # 规范化处理原始文本，得到处理后的文本，文本的tokens和处理后文本的tokens
        tokens = self.word_tokenizer(input_text)
        refined_input_text = ''
        last_end = -1

        for token in tokens:
            token_text = self.token_processor(token.text) if self.token_processor(token.text) else ' '
            if token.start_offset == last_end + 1:
                refined_input_text += token_text
            else:
                refined_input_text += (' ' + token_text)
            last_end = token.end_offset

        return refined_input_text.strip()

    def process_input_text(self, input_text):
        # 规范化处理原始文本，得到处理后的文本，文本的tokens和处理后文本的tokens
        tokens = self.word_tokenizer(input_text)
        refined_input_text = ''
        last_end = -1
        mapping_tokens = []
        token_index = 0
        for token in tokens:
            token_text = self.token_processor(token.text) if self.token_processor(token.text) else ' '
            if token.start_offset == last_end + 1:
                mapping_tokens.append(
                    TOKEN(token_index,len(refined_input_text), len(refined_input_text) + len(token_text) - 1, token_text, 'O'))
                token_index+=1
                refined_input_text += token_text
            else:
                mapping_tokens.append(
                    TOKEN(token_index,len(refined_input_text) + 1, len(refined_input_text) + len(token_text), token_text, 'O'))
                token_index+=1
                refined_input_text += (' ' + token_text)
            last_end = token.end_offset
        assert len(tokens)==len(mapping_tokens)
        return refined_input_text.strip(), tokens, mapping_tokens


if __name__ == '__main__':
    s = ' CX (cisplatin 80 mg/m(2) IV Q3W; capecitabined df d\u2002d      1000 mg/m(2) \t P.O. BID for 14 days Q3W) plus intravenous AM '
    text_processor = TextProcessor()
    print(text_processor.simple_process_input_text(s))
    print(text_processor.process_input_text(s))