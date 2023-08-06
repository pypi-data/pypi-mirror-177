from collections import namedtuple

ENGLISH_PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
CHINESE_PUNCTUATION = '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
PUNCTUATIONS = ENGLISH_PUNCTUATION + CHINESE_PUNCTUATION


# 每个token在所有tokens中的位置index(从0开始)， 在整体文本中的位置（'start_offset', 'end_offset'），根据位置的文本‘text’，这个token的label，若有，默认'O'
TOKEN = namedtuple('Token', ['index', 'start_offset', 'end_offset', 'text', 'label'],defaults=(-1,-1,-1,'','O'))  # end_offset 是坐标，不是索引, 这边索引是token所在文本的坐标

NER_LABEL = namedtuple('NER_Label', ['start_token', 'end_token','label'],defaults=(None,None,'O'))

# 部分常用html字符
HTML_ESCAPE_DICT = {
    '&lt;': '<',
    '&gt;': '>',
    '&nbsp;': ' ',
    '&amp;': '&',
    '&quot;': '"',
    '&times;': '×',
    '&pide;': '÷'
}

GRToLat_DICT = {
            'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta',
            'θ': 'theta', 'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron',
            'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi', 'χ': 'chi', 'ψ': 'psi',
            'ω': 'omega',
            'Α': 'Alpha', 'Β': 'Beta', 'Γ': 'Gamma', 'Δ': 'Delta', 'Ε': 'Epsilon', 'Ζ': 'Zeta', 'Η': 'Eta',
            'Θ': 'Theta', 'Ι': 'Iota', 'Κ': 'Kappa', 'Λ': 'Lambda', 'Μ': 'Mu', 'Ν': 'Nu', 'Ξ': 'Xi', 'Ο': 'Omicron',
            'Π': 'Pi', 'Ρ': 'Rho', 'Σ': 'Sigma', 'Τ': 'Tau', 'Υ': 'Upsilon', 'Φ': 'Phi', 'Χ': 'Chi', 'Ψ': 'Psi',
            'Ω': 'Omega'
        }
