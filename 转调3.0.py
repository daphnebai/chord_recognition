def rewrite(step):
    """
    转调并输出文件
    :param step: 移动的步长 ，即半音音程的整数倍d
    :return: void
    """
    new.write(f"若使用变调夹，移动{step}个品格\n")
    if step > 5:
        new.write("移动品格数大于5，建议更换指法而非使用变调夹\n")

    f = open("F://py//雏燕//转调//文件名.txt", "r", encoding="UTF-8")

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
            new.write("\t")

            # 换行
            if line_feed == 15:
                line_feed = 0
                new.write("\n")
            else:
                line_feed += 1
    new.flush()
    f.close()


# 统计大调、小调、大调加小调的和弦个数的列表，下标由0开始分别是
# C,Db,D,Eb,E,F,F#,G,Ab,A,Bb,B；
# Cm,Dbm,Dm,Ebm,E m,Fm,F#m,Gm,Abm,Am,Bbm,Bm
major_count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
minor_count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
combined_count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#  做变调的大调小调的列表
major_switch_list = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
minor_switch_list = ["Cm", "Dbm", "Dm", "Ebm", "Em", "Fm", "F#m", "Gm", "Abm", "Am", "Bbm", "Bm"]

f = open("F://py//雏燕//转调//文件名.txt", "r", encoding="UTF-8")

new = open("F://py//雏燕//转调//变调结果3.0.txt", "w", encoding="UTF-8")

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
# print(f"F：{major_count_list[5] + minor_count_list[5]}，F#：{major_count_list[6] + minor_count_list[6]}",total_chord)

new.write("本输出的和弦指法均为C大调下的和弦指法\n")
# 将大调小调分开的，找出出现次数最多的
if max(major_count_list) > max(minor_count_list):
    max_distinct = max(major_count_list)
    i_max_distinct = major_count_list.index(max_distinct)
    new.write(f"（区分大小调）通过歌曲和弦定调：{major_switch_list[i_max_distinct]}调\n")
else:
    max_distinct = max(minor_count_list)
    i_max_distinct = minor_count_list.index(max_distinct)
    new.write(f"（区分大小调）通过歌曲和弦定调：{minor_switch_list[i_max_distinct]}调\n")

# 将大调小调放一起的，找出出现次数最多的
max_combined = max(combined_count_list)
i_max_combined = combined_count_list.index(max_combined)
new.write(f"（不区分大小调）通过歌曲和弦定调：{major_switch_list[i_max_distinct]}调\n")

# 转到原调
rewrite(i_max_combined)

# 升调
rewrite(1)

# 降调
rewrite(13)

# 简化指法
count_F_Fup = combined_count_list[5] + combined_count_list[6]
min = count_F_Fup
min_step = 0
for step in range(12):
    index = (step + 5) % 12
    count_temp = combined_count_list[index] + combined_count_list[(index + 1)%12]
    if min > count_temp:
        min_step = step
rewrite(min_step)
