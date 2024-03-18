import numpy as np
import librosa
import tensorflow as tf
from tensorflow import keras
from collections import Counter

# 加载已保存的模型
model = tf.keras.models.load_model('myModel_CNN.h5')

def predict_instrument_from_song(song_path, target_clip_length=5):
    # 加载歌曲并提取特征
    y, sr = librosa.load(song_path)
    duration = librosa.get_duration(y=y, sr=sr)
    clip_number = int(duration // target_clip_length)
    features = []

    for k in range(clip_number):
        clip_start = k * target_clip_length
        clip_end = (k + 1) * target_clip_length
        clip = y[clip_start * sr:clip_end * sr]
        mfcc = librosa.feature.mfcc(y=clip, sr=sr, n_mfcc=20)
        features.append(mfcc)

    features = np.array(features)
    features = np.expand_dims(features, axis=3)

    # 使用模型进行预测
    predictions = model.predict(features)

    # 将预测的标签映射为乐器名称
    label_mapping = {
        1: '二胡',
        2: '琵琶',
        3: '三弦',
        4: '笛子',
        5: '唢呐',
        6: '锥琴',
        7: '中阮',
        8: '柳琴',
        9: '古筝',
        10: '扬琴',
        11: '笙',
        12: '古琴',
        13: '箜篌',
        14: '葫芦丝',
        15: '埙'
    }

    # 获取唯一的预测值
    unique_predictions = np.unique(np.argmax(predictions, axis=1) + 1)

    # 将预测的乐器名称输出为列表
    predicted_instruments = [label_mapping.get(label, '未知乐器') for label in unique_predictions]

    # 获取预测的标签列表
    predicted_labels = np.argmax(predictions, axis=1) + 1

    # 统计每个预测值的出现次数
    label_counts = Counter(predicted_labels)

    # 获取出现次数最多的预测值
    most_common_label = label_counts.most_common(1)[0][0]

    # 输出最常见预测值对应的乐器名称
    predicted_instrument_most = label_mapping.get(most_common_label, '未知乐器')

    return predicted_instruments, predicted_instrument_most

# 示例用法
song_path = 'D:\ChMusic-main\ChMusic-main\ChMusic\Test\hulusi.ogg'  # 替换为实际歌曲路径
predicted_instruments = predict_instrument_from_song(song_path)
print('预测的乐器:', predicted_instruments[0])
print('最可能的乐器:', predicted_instruments[1])
