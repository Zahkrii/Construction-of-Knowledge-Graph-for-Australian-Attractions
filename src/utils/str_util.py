import re


def check_str(re_exp: str, str: str):
    """检查字符串str是否符合正则表达式re_exp

    Args:
        re_exp (str): 正则表达式
        str (str): 待检查的字符串

    Returns:
        bool: 结果
    """
    res = re.match(re_exp, str)
    if res:
        return True
    else:
        return False
