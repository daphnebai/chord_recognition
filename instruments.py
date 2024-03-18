import numpy as np 
from pydub import AudioSegment
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from mlxtend.plotting import plot_confusion_matrix
import soundfile as sf
import librosa
import os
import pickle
import tensorflow as tf
from tensorflow import keras
from tqdm import tqdm, trange

if __name__ == "__main__":
    
    #music_path = "/kaggle/input/chmusic-add/Musics"
    music_path = "D:\ChMusic-main\ChMusic-main\ChMusic\Musics"
    target_clip_length = 5 
    print("Let's start now")
    print(music_path)

    filter = [".wav"]
    music_list = []

    for maindir, subdir, file_name_list in os.walk(music_path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext in filter:
                music_list.append(apath)

    traindata = []
    testdata = []

    for i in music_list:   
        music = AudioSegment.from_wav(i)
        samplerate = music.frame_rate
        clip_number = int(music.duration_seconds // target_clip_length)

        for k in range(clip_number):
            music[k * target_clip_length * 1000:(k + 1) * target_clip_length * 1000].export("./tem_clip.wav", format="wav")
            x, sr = librosa.load("./tem_clip.wav")
            mfcc_tem = librosa.feature.mfcc(y=x, sr=sr, n_mfcc=20)

            if os.path.basename(i)[-5] == '5':
                strlist = i.split(os.path.sep)
                testdata.append([mfcc_tem, strlist[-1][:strlist[-1].find(".")]])
            else:
                strlist = i.split(os.path.sep)
                traindata.append([mfcc_tem, strlist[-1][:strlist[-1].find(".")]])

    train_X = []
    train_Y = []
    test_X = []
    test_Y = []
    ground = []

    for i in traindata:
        train_X.append(i[0])
        train_Y.append(int(i[1]) - 1)

    for i in testdata:
        test_X.append(i[0])
        test_Y.append(int(i[1]) - 1)
        ground.append(int(i[1]))

    train_X = np.array(train_X)
    train_X = np.expand_dims(train_X, axis=3)
    train_Y = np.array(train_Y)
    test_X = np.array(test_X)
    test_X = np.expand_dims(test_X, axis=3)
    test_Y = np.array(test_Y)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(64, kernel_size=3, activation=tf.nn.relu, padding="same", input_shape=(20, 216, 1)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        tf.keras.layers.Conv2D(128, kernel_size=3, activation=tf.nn.relu, padding="same"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        tf.keras.layers.Conv2D(256, kernel_size=3, activation=tf.nn.relu, padding="same"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation=tf.nn.relu),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(15, activation=tf.nn.softmax)
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(train_X, train_Y, epochs=15, batch_size=32)
    loss, accuracy = model.evaluate(test_X, test_Y, batch_size=1)
    predict = model.predict(test_X)

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

    for i in range(len(predict)):
        predicted_label = np.argmax(predict[i]) + 1
        true_label = ground[i]
        predicted_instrument = label_mapping.get(predicted_label, '未知乐器')
        true_instrument = label_mapping.get(true_label, '未知乐器')
        print(f"Sample {i + 1}: Predicted Label: {predicted_label} ({predicted_instrument}), True Label: {true_label} ({true_instrument})")
    print(accuracy)
    tf.keras.models.save_model(model, 'myModel_CNN.h5', overwrite=True, include_optimizer=True)


    # 计算混淆矩阵
    predictions = model.predict(test_X)
    predicted_labels = np.argmax(predictions, axis=1) + 1  # 加1是因为你的标签从1开始
    conf_matrix = confusion_matrix(test_Y + 1, predicted_labels)

    # 显示混淆矩阵
    classes = [i + 1 for i in range(15)]  # 你的标签类别
    disp = ConfusionMatrixDisplay(conf_matrix, display_labels=classes)
    disp.plot(cmap=plt.cm.Blues, values_format=".0f")
    plt.title('Confusion Matrix')
    plt.show()