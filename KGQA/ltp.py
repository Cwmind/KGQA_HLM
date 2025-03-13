# -*- coding: utf-8 -*-
import pyltp
import os

# LTP 模型目录的路径
LTP_DATA_DIR = 'D:/installed/ltp-models/3.4.0/ltp_data_v3.4.0'

def cut_words(words):
    """
    对输入的文本进行分词。
    :param words: 输入的文本
    :return: 分词后的列表
    """
    try:
        # 分词模型路径
        seg_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
        # 初始化 Segmentor 并加载模型
        segmentor = pyltp.Segmentor(model_path=seg_model_path)  # 传递 model_path 参数
        # 分词
        words = segmentor.segment(words)
        # 将分词结果转换为列表
        array = list(words)
        segmentor.release()  # 释放模型
        return array
    except Exception as e:
        print(f"Error in cut_words: {e}")
        return []

def words_mark(array):
    """
    对分词后的列表进行词性标注。
    :param array: 分词后的列表
    :return: 词性标注后的列表
    """
    try:
        # 词性标注模型路径
        pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
        # 初始化 Postagger 并加载模型
        postagger = pyltp.Postagger(pos_model_path)  # 传递 model_path 参数
        # 词性标注
        postags = postagger.postag(array)
        # 将词性标注结果转换为列表
        pos_array = list(postags)
        postagger.release()  # 释放模型
        return pos_array
    except Exception as e:
        print(f"Error in words_mark: {e}")
        return []

def get_target_array(words):
    """
    获取目标词性的词语。
    :param words: 输入的文本
    :return: 目标词性的词语列表
    """
    # 目标词性列表
    target_pos = ['nh', 'n']
    target_array = []
    # 分词
    seg_array = cut_words(words)
    # 词性标注
    pos_array = words_mark(seg_array)
    # 筛选目标词性的词语
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])
    # 添加分词结果中的第二个词（假设需要）
    if len(seg_array) > 1:
        target_array.append(seg_array[1])
    return target_array