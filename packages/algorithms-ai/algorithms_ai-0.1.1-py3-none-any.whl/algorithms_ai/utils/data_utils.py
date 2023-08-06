import re
from collections import namedtuple

ENGLISH_PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
CHINESE_PUNCTUATION = '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
PUNCTUATIONS = ENGLISH_PUNCTUATION + CHINESE_PUNCTUATION

Token = namedtuple('Token', ['start_offset', 'end_offset', 'text'])
Label = namedtuple('Label', ['start_token', 'end_token', 'start_token_index', 'end_token_index', 'label'])
# label: 开始和结束的token以及这个token在整体tokens中的位置

class WordTokenizer:
    def __init__(self, regex=None, keep_words=()):
        # 规则切词，可以保留哪些词不用切分
        # zh_punctuation = '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
        # en_punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        # punctuations = ENGLISH_PUNCTUATION + CHINESE_PUNCTUATION

        html_escape = ['&quot;', '&amp;', '&lt;', '&gt;', '&nbsp;']
        # 同一个字符开头满足多个规则，以第一个规则作数，
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
        for i in self.find_re.finditer(text):
            if tmp_index < i.start():
                if text[tmp_index:i.start()].strip():
                    res.append(Token(tmp_index, i.start() - 1, text[tmp_index:i.start()]))
            if i.group().strip():
                res.append(Token(i.start(), i.end() - 1, i.group()))
            tmp_index = i.end()

        if tmp_index < len(text):
            if text[tmp_index:len(text) - 1].strip():
                res.append(Token(tmp_index, len(text) - 1, text[tmp_index:len(text) - 1]))
        return res  # [Token(start,end,text)]


class TokenProcessor:
    def __init__(self, lower=False, map_digit=False, token_map=None):
        self.html_escape_map = {'&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt;': '>', '&nbsp;': ' '}
        self.GRToLat_map = {
            'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta',
            'θ': 'theta', 'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron',
            'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi', 'χ': 'chi', 'ψ': 'psi',
            'ω': 'omega',
            'Α': 'Alpha', 'Β': 'Beta', 'Γ': 'Gamma', 'Δ': 'Delta', 'Ε': 'Epsilon', 'Ζ': 'Zeta', 'Η': 'Eta',
            'Θ': 'Theta', 'Ι': 'Iota', 'Κ': 'Kappa', 'Λ': 'Lambda', 'Μ': 'Mu', 'Ν': 'Nu', 'Ξ': 'Xi', 'Ο': 'Omicron',
            'Π': 'Pi', 'Ρ': 'Rho', 'Σ': 'Sigma', 'Τ': 'Tau', 'Υ': 'Upsilon', 'Φ': 'Phi', 'Χ': 'Chi', 'Ψ': 'Psi',
            'Ω': 'Omega'
        }
        self.token_map = token_map

        self.lower = lower
        self.map_digit = map_digit

    def run(self, token_text: str):
        if token_text in self.html_escape_map:
            return self.html_escape_map[token_text]
        # if token_text in self.GRToLat_map:
        #     return ' ' +self.GRToLat_map[token_text]+' '

        if self.map_digit:
            token_text = self.map_num_to_special_token(token_text)
        if self.token_map and isinstance(self.token_map, dict):
            if token_text in self.token_map:
                return self.token_map[token_text]

        if self.lower:
            token_text = token_text.lower()
        return token_text.strip()

    @staticmethod
    def map_num_to_special_token(token_text, special_token='num_token'):
        if token_text.isdigit():
            return special_token
        else:
            if token_text.count('.') == 1 and token_text[0:token_text.find('.')].isdigit() \
                    and token_text[token_text.find('.') + 1:].isdigit():
                return special_token
        return token_text


class NERProcessor:
    def __init__(self, regex=None, keep_token=(),
                 token_map=None, lower=False, map_digit=False,
                 left_token_keep=None, right_token_keep=('%',), left_token_remove=None, right_token_remove=None):
        """
        regex: 切词的规则
        keep_token : 保持哪些文本单独作为token
        token_map : 需要对哪些token进行变换
        lower: 处理完的text是否小写
        map_digit: 把数字映射为特定的token：【NUM】
        left_token_keep：label中左边token的保留
        right_token_keep：label中右边token的保留
        left_token_remove: label中左边token的去除
        right_token_remove: label中右边token的去除
        """
        self.word_tokenizer = WordTokenizer(regex=regex, keep_words=keep_token).run
        self.token_processor = TokenProcessor(lower=lower,
                                              map_digit=map_digit,
                                              token_map=token_map).run
        self.format_labels = FormatLabels(left_token_keep=left_token_keep,
                                          right_token_keep=right_token_keep,
                                          left_token_remove=left_token_remove,
                                          right_token_remove=right_token_remove).run

    def simple_process_input_text(self,input_text):
        # 规范化处理原始文本，得到处理后的文本，文本的tokens和处理后文本的tokens
        tokens = self.word_tokenizer(input_text)
        refined_input_text = ''
        last_end = -1

        for token in tokens:
            token_text = self.token_processor(token.text) if self.token_processor(token.text) else ' '
            if token.start_offset == last_end + 1:
                refined_input_text += token_text
            else:
                refined_input_text += ' ' + token_text
            last_end = token.end_offset

        return refined_input_text


    def process_input_text(self, input_text):
        # 规范化处理原始文本，得到处理后的文本，文本的tokens和处理后文本的tokens
        tokens = self.word_tokenizer(input_text)
        refined_input_text = ''
        last_end = -1
        map_tokens = []
        for token in tokens:
            token_text = self.token_processor(token.text) if self.token_processor(token.text) else ' '
            if token.start_offset == last_end + 1:
                map_tokens.append(
                    Token(len(refined_input_text), len(refined_input_text) + len(token_text) - 1, token_text))
                refined_input_text += token_text
            else:
                map_tokens.append(
                    Token(len(refined_input_text) + 1, len(refined_input_text) + len(token_text), token_text))
                refined_input_text += ' ' + token_text
            last_end = token.end_offset

        return refined_input_text, tokens, map_tokens

    def simple_process_text(self,input_text):
        refined_input_text = ''
        last_end = -1
        for token in self.word_tokenizer(input_text):
            token_text = self.token_processor(token.text) if self.token_processor(token.text) else ' '
            if token.start_offset == last_end + 1:
                refined_input_text += token_text
            else:
                refined_input_text += ' ' + token_text
            last_end = token.end_offset

        return refined_input_text


    def process_raw_data(self, input_text, labels):
        # 输入原始文本和labels，处理成规范化后的文本和labels，label需要start_offset,end_offset，label，
        refined_input_text, tokens, map_tokens = self.process_input_text(input_text)

        map_labels = [self.map_label(tokens, _) for _ in labels]
        map_labels = [Label(map_tokens[m_l.start_token_index],
                            map_tokens[m_l.end_token_index],
                            m_l.start_token_index,
                            m_l.end_token_index,
                            m_l.label) for m_l in map_labels]

        refined_labels = self.format_labels(map_labels, map_tokens)
        refined_labels = [
            {
                'start_offset': i.start_token.start_offset,
                'end_offset': i.end_token.end_offset,
                'text': refined_input_text[i.start_token.start_offset:i.end_token.end_offset + 1],
                'label': i.label

            }
            for i in refined_labels
        ]
        return refined_input_text, refined_labels

    @staticmethod
    def map_label(tokens, raw_label):
        # 给定tokens，以及原始label对应的token
        start = raw_label['start_offset']
        end = raw_label['end_offset']
        # print(raw_label)
        label_name = raw_label['label']
        assert start <= end
        start_token, start_token_index = Token(-1, -1, ''), -1
        if tokens[-1].start_offset <= start <= tokens[-1].end_offset:
            start_token, start_token_index = tokens[-1], len(tokens) - 1
            end_token, end_token_index = tokens[-1], len(tokens) - 1
        else:
            for i in range(len(tokens) - 1):
                if tokens[i].start_offset <= start <= tokens[i].end_offset:
                    start_token, start_token_index = tokens[i], i
                    break
                elif tokens[i].end_offset < start < tokens[i + 1].start_offset:
                    start_token, start_token_index = tokens[i + 1], i + 1
                    break

            end_token, end_token_index = Token(-1, -1, ''), -1
            for i in range(start_token_index, len(tokens) - 1):
                if tokens[i].start_offset <= end <= tokens[i].end_offset:
                    end_token, end_token_index = tokens[i], i
                    break
                elif tokens[i].end_offset < end < tokens[i + 1].start_offset:
                    end_token, end_token_index = tokens[i], i
                    break
            if end_token.start_offset == -1:
                end_token, end_token_index = tokens[-1], len(tokens) - 1

        return Label(start_token, end_token, start_token_index, end_token_index, label_name)

    def get_raw_labels(self, input_text, refined_labels):
        # 已知输入的原始文本，规范化后的文本，和得到的标签，映射回原始文本中的标签
        refined_input_text, tokens, map_tokens = self.process_input_text(input_text)

        map_labels = [self.map_label(map_tokens, r_l) for r_l in refined_labels]
        map_labels = [Label(tokens[m_l.start_token_index],
                            tokens[m_l.end_token_index],
                            m_l.start_token_index,
                            m_l.end_token_index,
                            m_l.label) for m_l in map_labels]

        raw_labels = self.format_labels(map_labels, tokens)
        raw_labels = [
            {
                'start_offset': i.start_token.start_offset,
                'end_offset': i.end_token.end_offset,
                'text': input_text[i.start_token.start_offset:i.end_token.end_offset + 1],
                'label': i.label
            }
            for i in raw_labels
        ]
        return raw_labels

    @staticmethod
    def check_labels(labels):
        # 检查label之间是否相互包含
        sub_labels = sorted(labels, key=lambda x: x['start_offset'])
        last_end = -1
        for i in sub_labels:
            if i['start_offset'] >i['end_offset']:
                return False
            if i['start_offset'] <= last_end:
                return False

            last_end = i['end_offset']
        return True


class FormatLabels:
    def __init__(self, left_token_keep=None, right_token_keep=('%',), left_token_remove=None,
                 right_token_remove=None):
        """
        根据tokens和labels-token来对label进行规范化
        """
        punctions = list(PUNCTUATIONS)

        self.left_remove = punctions + [' ']
        if left_token_remove:
            for i in left_token_remove:
                self.left_remove.append(i)

        self.right_remove = punctions + [' ']
        if right_token_remove:
            for i in right_token_remove:
                self.right_remove.append(i)

        if right_token_keep:
            for i in right_token_keep:
                if i in self.right_remove:
                    self.right_remove.remove(i)

        if left_token_keep:
            for i in left_token_keep:
                if i in self.left_remove:
                    self.left_remove.remove(i)

    def run(self, labels, tokens):
        labels = [self.format_each_label(i, tokens) for i in labels]
        all_labels = [i.label for i in labels]
        refined_labels = []
        for a_l in all_labels:
            sub_labels = [i for i in labels if i.label == a_l]
            sub_labels = sorted(sub_labels, key=lambda x: x.start_token_index)
            for i in self.merge_nested_labels(sub_labels):
                if i not in refined_labels:
                    refined_labels.append(i)

        return refined_labels

    def format_each_label(self, label, tokens):
        # 对于label增删左右边界
        while label.start_token.text in self.left_remove:
            label = Label(tokens[label.start_token_index + 1], label.end_token, label.start_token_index + 1,
                          label.end_token_index, label.label)
            if label.start_token_index > label.end_token_index:
                break

        while label.end_token.text in self.right_remove:
            label = Label(label.start_token, tokens[label.end_token_index - 1], label.start_token_index,
                          label.end_token_index - 1, label.label)
            if label.start_token_index > label.end_token_index:
                break

        all_texts = [i.text for i in tokens[label.start_token_index:label.end_token_index + 1]]

        done_bound = False

        while not done_bound:
            c = 0
            for left_bound,right_bound in [('(',')'),('[',']')]:

                if all_texts.count(left_bound) - all_texts.count(right_bound) >= 1:
                    if label.end_token_index + 1 <= len(tokens) - 1 and tokens[label.end_token_index + 1].text == right_bound:
                        label = Label(label.start_token, tokens[label.end_token_index + 1], label.start_token_index,
                                      label.end_token_index + 1, label.label)
                        break

                if all_texts.count(right_bound) - all_texts.count(left_bound) >= 1:
                    if label.start_token_index >= 1 and tokens[label.start_token_index - 1].text == left_bound:
                        label = Label(tokens[label.start_token_index - 1], label.end_token,
                                      label.start_token_index - 1,
                                      label.end_token_index, label.label)
                        break

                c+=1

            if c==2:
                done_bound = True

            # if all_texts.count('(') - all_texts.count(')') >= 1:
            #     if label.end_token_index + 1 <= len(tokens) - 1 and tokens[label.end_token_index + 1].text == ')':
            #         label = Label(label.start_token, tokens[label.end_token_index + 1], label.start_token_index,
            #                       label.end_token_index + 1, label.label)
            #
            # if all_texts.count('[') - all_texts.count(']') >= 1:
            #     if label.end_token_index + 1 <= len(tokens) - 1 and tokens[label.end_token_index + 1].text == ']':
            #         label = Label(label.start_token, tokens[label.end_token_index + 1], label.start_token_index,
            #                       label.end_token_index + 1, label.label)
            #
            # if all_texts.count(')') - all_texts.count('(') >= 1:
            #     if label.start_token_index >= 1 and tokens[label.start_token_index - 1].text == '(':
            #         label = Label(tokens[label.start_token_index - 1], label.end_token, label.start_token_index - 1,
            #                       label.end_token_index, label.label)
            #
            # if all_texts.count(']') - all_texts.count('[') >= 1:
            #     if label.start_token_index >= 1 and tokens[label.start_token_index - 1].text == '[':
            #         label = Label(tokens[label.start_token_index - 1], label.end_token, label.start_token_index - 1,
            #                       label.end_token_index, label.label)


        return label

    @staticmethod
    def merge_nested_labels(labels):
        # 同一种实体的嵌套合并，输入的labels有序
        refined_labels = []

        last_label = labels[0]
        label = last_label.label
        for e in labels[1:]:
            if e.start_token_index > last_label.end_token_index:
                refined_labels.append(last_label)
                last_label = e
            elif e.start_token_index <= last_label.end_token_index:
                last_label = Label(
                    last_label.start_token,
                    e.end_token,
                    last_label.start_token_index,
                    e.end_token_index,
                    label
                )
        refined_labels.append(last_label)
        return refined_labels


if __name__ == '__main__':
    # s = 'With median follow-up of 21 months, 24-month relapse-free survival (RFS) was 67% (95% CI 62% to 73%) in the 326 patients.'
    # NerFormat().run(s,[])
    s2 = "Oral acalabruti(nib) 100 mg 我i在发啊 <  twic\u00b7e daily  ; was & admi\nnister\ted with or &lt; 13.8kg/m without,α-1 12.😊 "
    labels = [{'start_offset': 14, 'end_offset': 18, 'text': 'i(nib', 'label': 'a'},  # end_offset错误
              # {'start_offset': 16, 'end_offset': 20, 'text': 'nib)', 'label': 'a'},  # 正确
              {'start_offset': 38, 'end_offset': 47, 'text': 'wice dail', 'label': 'c'},  # 边界不对
              {'start_offset': 46, 'end_offset': 54, 'text': 'ly  ; ', 'label': 'c'},
              {'start_offset': 79, 'end_offset': 89, 'text': '&lt; 13.8', 'label': 'd'}]
    s = [{'start_offset': 5, 'end_offset': 18, 'text': 'acalabruti(nib', 'label': 'a'},
         {'start_offset': 38, 'end_offset': 54, 'text': 'twice daily ; was', 'label': 'c'},
         {'start_offset': 78, 'end_offset': 87, 'text': 'or < [NUM]', 'label': 'd'}]

    s2 = "sd fatigue (62 [55.4%]) and gynecomastia (41 [36.6%])sdf "
    # s = {'id': '18612151',
    #      'arms_ner': [{'start_offset': 173,
    #                    'end_offset': 216,
    #                    'text': '(paclitaxel plus carboplatin) with cetuximab',
    #                    'label': 'arm_option'}],
    #      'input_text': 'Two hundred twenty-nine chemotherapy-naive patients with advanced-stage NSCLC were enrolled onto a phase II selection trial evaluating sequential or concurrent chemotherapy (paclitaxel plus carboplatin) with cetuximab.'}
    labels = [{"start_offset": 3, "end_offset": 125-77+3, "text": "fatigue (62 [55.4%]) and gynecomastia (41 [36.6%]", "label": "result"}]
    # print(NERProcessor().process_raw_data(s['input_text'], s['arms_ner']))
    # print(NERProcessor().get_raw_labels(s2, s))
    ner_processor = NERProcessor(keep_token=('\u00b7',''),
                                 token_map={'\u00b7': '.'},
                                 right_token_keep=('%',),
                                 right_token_remove=('daily',))
    sample_processor = NERProcessor(
        regex=None,
        keep_token=(),
        token_map={},
        lower=False, map_digit=False,
        left_token_keep=('.', '·'), right_token_keep=('%',),
        left_token_remove=None, right_token_remove=None
    )

    # print(ner_processor.process_input_text(s2))
    print(sample_processor.process_raw_data(s2, labels))

    # 输入： 原始文本 ， labels ----》原始tokens-----》处理后的tokens
    # 输出： 处理后的文本， 处理后的labels
    # 需要： 通过处理后的文本的得到原始文本的索引
