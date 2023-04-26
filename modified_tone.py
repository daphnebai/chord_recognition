def switch_tone():
    major_count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    minor_count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    combined_count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #  做变调的大调小调的列表
    major_switch_list = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    minor_switch_list = ["Cm", "Dbm", "Dm", "Ebm", "Em", "Fm", "F#m", "Gm", "Abm", "Am", "Bbm", "Bm"]

    f = open("in.txt", "r", encoding="UTF-8")

    new = open("in2.txt", "w", encoding="UTF-8")

    total_chord = 0  # 和弦总数记数
    for line in f:  # 分成每一行
        line = line.strip()  # 去除开头和结尾的空格与换行符
        words = line.split(" ")  # 分成每一个单词
        for w in words:
            for i in range(0, 12):  # 统计各个和弦个数
                if major_switch_list[i] == w:
                    major_count_list[i] += 1
                    # break
                if minor_switch_list[i] == w:
                    minor_count_list[i] += 1
                    # break
    for i in range(0, 12):
        combined_count_list[i] = major_count_list[i] + minor_count_list[i]
        total_chord = total_chord + combined_count_list[i]
    f.close()

    # 简化指法
    count_F_Fup = combined_count_list[5] + combined_count_list[6]
    min = count_F_Fup
    step = 0
    for stepss in range(12):
        index = (5-stepss) % 12
        count_temp = combined_count_list[index] + combined_count_list[(index + 1) % 12]
        if min > count_temp:
            step = stepss
    new.write("变调夹请夹"+f"{step}"+"品\n")
    # new.write(f"{step}\n")
    f = open("in.txt", "r", encoding="UTF-8")

    for l in f:  # 分成每一行
        line_feed = 0  # 统计字符，控制换行
        l = l.strip()  # 去除开头和结尾的空格与换行符
        ws = l.split(" ")  # 分成每一个单词
        for w in ws:
            for i in range(0, 12):
                j = (i + step) % 12
                if w == major_switch_list[i]:
                    w = major_switch_list[j]
                    break
                if w == minor_switch_list[i]:
                    w = minor_switch_list[j]
                    break
            new.write(w)
            new.write(" ")

    new.flush()
    f.close()
    return step
