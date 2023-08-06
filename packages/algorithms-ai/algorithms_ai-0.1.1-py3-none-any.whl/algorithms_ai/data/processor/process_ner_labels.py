# 处理实体识别的label
# 输入原文，和标签或预测的实体，输出规范化后的实体
# 原始的label需要包含：start_offset，end_offset，label,以及原文

from loguru import logger

from consts import PUNCTUATIONS, TOKEN, NER_LABEL
from process_text import TextProcessor


class NER_Processor:
    def __init__(self, word_tokenizer=None, token_processor=None, labels_format=None):
        self.text_processor = TextProcessor(word_tokenizer=word_tokenizer, token_processor=token_processor)
        if not labels_format:
            self.labels_format = FormatLabels().run
        else:
            self.labels_format = labels_format

    @staticmethod
    def map_label(tokens, raw_label: dict):
        # 给定tokens，以及原始label对应的token
        try:
            assert ('start_offset' in raw_label) and ('end_offset' in raw_label) and ('label' in raw_label) and (
                        0<=raw_label['start_offset'] <= raw_label['end_offset']<=tokens[-1].end_offset)

            start_token_index = 0
            start_token = TOKEN(-1, -1, -1, '', 'O')
            for i in range(len(tokens) - 2):
                if tokens[i].start_offset <= raw_label['start_offset'] <= tokens[i].end_offset:
                    start_token = tokens[i]
                    start_token_index = start_token.index
                    break
                elif tokens[i].end_offset < raw_label['start_offset'] < tokens[i + 1].start_offset:
                    start_token = tokens[i + 1]
                    start_token_index = start_token.index
                    break
            if start_token.index==-1:  # 未找到,则最后一个token为label
                return NER_LABEL(tokens[-1], tokens[-1], raw_label['label'])
            else:
                end_token = TOKEN(-1, -1, -1, '', 'O')
                for i in range(start_token_index, len(tokens) - 2):
                    if tokens[i].start_offset <= raw_label['end_offset'] <= tokens[i].end_offset:
                        end_token = tokens[i]
                        break
                    elif tokens[i].end_offset < raw_label['end_offset'] < tokens[i + 1].start_offset:
                        end_token = tokens[i]
                        break

                if end_token.start_offset == -1:
                    end_token = tokens[-1]
                return NER_LABEL(start_token, end_token, raw_label['label'])
        except Exception as e: #
            logger.info(f'error label:{raw_label}')
            return


    def process_raw_data(self, input_text, labels):
        # 输入原始文本和labels，处理成规范化后的文本和labels，label需要start_offset,end_offset，label，
        refined_input_text, tokens, mapping_tokens = self.text_processor.process_input_text(input_text)

        mapping_labels = []
        try:
            for each_label in labels:
                each_label = self.map_label(tokens, each_label)  # 把label变成几个token的集合，并表明label在tokens中位置
                if each_label:
                    mapping_labels.append(NER_LABEL(
                            mapping_tokens[each_label.start_token.index],
                            mapping_tokens[each_label.end_token.index],
                            each_label.label
                        ))  # 映射到处理后token中的label

            refined_labels = self.labels_format(mapping_labels, mapping_tokens)
            refined_labels = [
                {
                    'start_offset': i.start_token.start_offset,
                    'end_offset': i.end_token.end_offset,
                    'text': refined_input_text[i.start_token.start_offset:i.end_token.end_offset + 1],
                    'label': i.label
                }
                for i in refined_labels
            ]
            return refined_labels
        except Exception as e:
            logger.info(f'error labels:{labels}')
            logger.info(e)


    def get_raw_labels(self, input_text, refined_labels):
        # 已知输入的原始文本，规范化后的文本，和得到的标签，映射回原始文本中的标签
        refined_input_text, tokens, map_tokens = self.text_processor.process_input_text(input_text)

        map_labels = [self.map_label(map_tokens, r_l) for r_l in refined_labels]
        map_labels = [NER_LABEL(tokens[m_l.start_token.index],
                            tokens[m_l.end_token.index],
                            m_l.label) for m_l in map_labels]

        raw_labels = self.labels_format(map_labels, tokens)
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

    #     @staticmethod
    #     def check_labels(labels):
    #         # 检查label之间是否相互包含
    #         sub_labels = sorted(labels, key=lambda x: x['start_offset'])
    #         last_end = -1
    #         for i in sub_labels:
    #             if i['start_offset'] >i['end_offset']:
    #                 return False
    #             if i['start_offset'] <= last_end:
    #                 return False
    #
    #             last_end = i['end_offset']
    #         return True


class FormatLabels:
    def __init__(self,
                 left_token_keep=None,
                 right_token_keep=('%',),
                 left_token_remove=None,
                 right_token_remove=None,
                 left_token_add=None,
                 right_token_add=None
                 ):
        """
        默认对边界('(',')'),('[',']')进行处理，
        根据tokens和labels-token来对label进行规范化
        left_token_remove: label中左边token的去除 , 默认去除所有标点+空格
        right_token_remove: label中右边token的去除，, 默认去除所有标点+空格

        保留的强度大于去除的强度
        left_token_keep：label中左边token的保留,
        right_token_keep：label中右边token的保留

        # 最后在左右两边添加token
        left_token_add =None,
        right_token_add = None

        """

        self.left_remove = list(PUNCTUATIONS) + [' ']
        if left_token_remove:
            for i in left_token_remove:
                self.left_remove.append(i)

        self.right_remove = list(PUNCTUATIONS) + [' ']
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

        self.left_add = []
        if left_token_add:
            self.left_add.extend(left_token_add)

        self.right_add = []
        if right_token_add:
            self.right_add.extend(right_token_add)

    def run(self, labels, tokens):
        labels = [self.format_each_label(i, tokens) for i in labels]
        labels = [i for i in labels if i]

        all_labels = [i.label for i in labels]
        refined_labels = []
        for a_l in all_labels:
            # 不同label多个实体的合并
            sub_labels = [i for i in labels if i.label == a_l]
            sub_labels = sorted(sub_labels, key=lambda x: x.start_token.index)
            for i in self.merge_nested_labels(sub_labels):
                if i not in refined_labels:
                    refined_labels.append(i)

        return refined_labels

    def format_each_label(self, label, tokens):
        # ->NER_LABEL
        # 对于label增删左右边界
        while label.start_token.text in self.left_remove:
            label = NER_LABEL(tokens[label.start_token.index + 1], label.end_token, label.label)
            if label.start_token.index > label.end_token.index:  # 全都删完
                return

        while label.end_token.text in self.right_remove:
            label = NER_LABEL(label.start_token, tokens[label.end_token.index - 1], label.label)
            if label.start_token.index > label.end_token.index: # 全都删完
                return

        all_texts = [i.text for i in tokens[label.start_token.index:label.end_token.index + 1]]

        done_bound = False
        while not done_bound:
            c = 0
            # 补充左右括号
            for left_bound, right_bound in [('(', ')'), ('[', ']')]:
                if all_texts.count(left_bound) - all_texts.count(right_bound) >= 1:
                    if label.end_token.index  <= len(tokens) - 2 and tokens[label.end_token.index + 1].text == right_bound:
                        label = NER_LABEL(label.start_token, tokens[label.end_token.index + 1], label.label)
                        break

                if all_texts.count(right_bound) - all_texts.count(left_bound) >= 1:
                    if label.start_token.index >= 1 and tokens[label.start_token.index - 1].text == left_bound:
                        label = NER_LABEL(tokens[label.start_token.index - 1], label.end_token, label.label)
                        break
                c += 1

            if c == 2:
                done_bound = True

        while (label.start_token.index >= 1) and (tokens[label.start_token.index - 1] in self.left_add):
            label = NER_LABEL(tokens[label.start_token.index - 1], label.end_token, label.label)

        while (label.end_token.index + 1 <= len(tokens)) and (tokens[label.end_token.index + 1] in self.right_add):
            label = NER_LABEL(label.start_token, tokens[label.end_token.index + 1], label.label)

        return label

    @staticmethod
    def merge_nested_labels(labels):
        # NER_LABEL
        # 同一种实体的嵌套合并，输入的labels有序 ,交叉的合并，相邻的合并
        refined_labels = []

        last_label = labels[0]
        label = last_label.label
        for current_label in labels[1:]:
            if current_label.start_token.index > last_label.end_token.index+1:
                refined_labels.append(last_label)
                last_label = current_label
            else:
                last_label = NER_LABEL(
                    last_label.start_token,
                    current_label.end_token,
                    label
                )
        refined_labels.append(last_label)
        return refined_labels

    def get_labels_from_pred_tokens(self, token_predicts):
        # 模型输出各个token的判断结果，将这些结果合并起来,BIO ， I和B有相似地位
        all_labels = []
        append_label = all_labels.append
        label = []
        init_label = label.clear
        append_token = label.append

        last_tag = 'O'
        last_label = 'O'
        for token_index, current_pred in enumerate(token_predicts):
            current_tag = current_pred.split('-')[0]
            current_label = current_pred.split('-')[-1]

            if last_tag == 'O':
                if current_tag in ('B', 'I'):
                    append_token(TOKEN(token_index, -1, -1, '', current_label))
            elif last_tag == 'B':
                if current_tag == 'O':
                    append_label(NER_LABEL(label[0], label[-1], last_label))
                    init_label()
                elif current_tag == 'B':
                    append_label(NER_LABEL(label[0], label[-1], last_label))
                    init_label()
                    append_token(TOKEN(token_index, -1, -1, '', current_label))
                else:  # I
                    if last_label == current_label:
                        append_token(TOKEN(token_index, -1, -1, '', current_label))
                    else:
                        append_label(NER_LABEL(label[0], label[-1], last_label))
                        init_label()
                        append_token(TOKEN(token_index, -1, -1, '', current_label))
            else:  # I
                if current_tag == 'O':
                    append_label(NER_LABEL(label[0], label[-1], last_label))
                    init_label()
                elif current_tag == 'B':  # 另一个实体
                    append_label(NER_LABEL(label[0], label[-1], last_label))
                    init_label()
                    append_token(TOKEN(token_index, -1, -1, '', current_label))
                else:  # 'I'
                    if last_label == current_label:
                        append_token(TOKEN(token_index, -1, -1, '', current_label))
                    else:
                        append_label(NER_LABEL(label[0], label[-1], last_label))
                        init_label()
                        append_token(TOKEN(token_index, -1, -1, '', current_label))
            last_tag = current_tag
            last_label = current_label
        if label:
            append_label(NER_LABEL(label[0], label[-1], last_label))
        return all_labels

    def get_labels_from_pred_tokens_strict(self, token_predicts):
        # 模型输出各个token的判断结果，将这些结果合并起来,BIO ,严格BIO
        all_labels = []
        append_label = all_labels.append
        label = []
        init_label = label.clear
        append_token = label.append

        last_tag = 'O'
        last_label = 'O'
        for token_index, current_pred in enumerate(token_predicts):
            current_tag = current_pred.split('-')[0]
            current_label = current_pred.split('-')[-1]

            if last_tag == 'O':
                if current_tag == 'B':
                    append_token(TOKEN(token_index, -1, -1, '', current_label))
            elif last_tag == 'B':
                if current_tag == 'O':
                    append_label(NER_LABEL(label[0], label[-1], last_label))
                    init_label()
                elif current_tag == 'B':
                    append_label(NER_LABEL(label[0], label[-1], last_label))
                    init_label()
                    append_token(TOKEN(token_index, -1, -1, '', current_label))
                else:  # I
                    if last_label == current_label:
                        append_token(TOKEN(token_index, -1, -1, '', current_label))
            else:  # I
                if current_tag == 'O':
                    if label:
                        append_label(NER_LABEL(label[0], label[-1], last_label))
                        init_label()
                elif current_tag == 'B':  # 另一个实体
                    if label:
                        append_label(NER_LABEL(label[0], label[-1], last_label))
                    init_label()
                    append_token(TOKEN(token_index, -1, -1, '', current_label))
                else:  # 'I'
                    if last_label == current_label:
                        if label:
                            append_token(TOKEN(token_index, -1, -1, '', current_label))
            last_tag = current_tag
            last_label = current_label
        if label:
            append_label(NER_LABEL(label[0], label[-1], last_label))

        return all_labels


if __name__ == '__main__':
    # s = 'With median follow-up of 21 months, 24-month relapse-free survival (RFS) was 67% (95% CI 62% to 73%) in the 326 patients.'
    # NerFormat().run(s,[])
    s2 = "Oral acalabruti(nib) 100 mg 我i在发啊 <  twic\u00b7e daily  ; was & admi\nnister\ted with or &lt; 13.8kg/m without,α-1 12.😊 "
    labels = [{'start_offset': 14, 'end_offset': 18, 'text': 'i(nib', 'label': 'a'},  # end_offset错误
              # {'start_offset': 16, 'end_offset': 20, 'text': 'nib)', 'label': 'a'},  # 正确
              {'start_offset': 38, 'end_offset': 44, 'text': 'wice dail', 'label': 'c'},  # 边界不对
              {'start_offset': 46, 'end_offset': 54, 'text': 'ly  ; ', 'label': 'c'},
              {'start_offset': 79, 'end_offset': 89, 'text': '&lt; 13.8', 'label': 'd'}]
    s = [{'start_offset': 5, 'end_offset': 18, 'text': 'acalabruti(nib', 'label': 'a'},
         {'start_offset': 38, 'end_offset': 54, 'text': 'twice daily ; was', 'label': 'c'},
         {'start_offset': 78, 'end_offset': 87, 'text': 'or < 13.8', 'label': 'd'}]

    # s2 = "sd fatigue (62 [55.4%]) and gynecomastia (41 [36.6%])sdf "
    # s = {'id': '18612151',
    #      'arms_ner': [{'start_offset': 173,
    #                    'end_offset': 216,
    #                    'text': '(paclitaxel plus carboplatin) with cetuximab',
    #                    'label': 'arm_option'}],
    #      'input_text': 'Two hundred twenty-nine chemotherapy-naive patients with advanced-stage NSCLC were enrolled onto a phase II selection trial evaluating sequential or concurrent chemotherapy (paclitaxel plus carboplatin) with cetuximab.'}
    # labels = [{"start_offset": 3, "end_offset": 125-77+3, "text": "fatigue (62 [55.4%]) and gynecomastia (41 [36.6%]", "label": "result"}]
    print(NER_Processor().process_raw_data(s2, labels))
    print(NER_Processor().text_processor.simple_process_input_text(s2))
    print(s2[78:87])
    print(NER_Processor().get_raw_labels(s2, s))
    k = 'Oral acalabruti(nib) 100 mg 我i在发啊 < twic·e daily ; was & admi nister ed with or < 13.8kg/m without,α-1 12.😊'
    print(k[78:87])
