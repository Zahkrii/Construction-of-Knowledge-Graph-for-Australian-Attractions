from text2vec import Similarity, sentence_model
import warnings
from functools import wraps


def ignore_warnings(f):
    @wraps(f)
    def inner(*args, **kwargs):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("ignore")
            response = f(*args, **kwargs)
        return response
    return inner


@ignore_warnings
def getSim(sentences1: str, sentences2: str):
    """计算两字符串相似度

    Args:
        sentences1 (str): 字符串1
        sentences2 (str): 字符串2
    
    Returns:
        float: 相似度
    """
    sim_model = Similarity()
    score = sim_model.get_score(sentences1, sentences2)
    # print(f'{sentences1}与{sentences2}相似度：{score}')
    return score


@ignore_warnings
def getSimCustomModel(sentences1: str, sentences2: str):
    """计算两字符串相似度(自定义模型)

    Args:
        sentences1 (str): 字符串1
        sentences2 (str): 字符串2

    Returns:
        float: 相似度
    """
    sim_model = Similarity('shibing624/text2vec-base-chinese',
                           encoder_type=sentence_model.EncoderType.FIRST_LAST_AVG)
    score = sim_model.get_score(sentences1, sentences2)
    # print(f'{sentences1}与{sentences2}相似度：{score}')
    return score