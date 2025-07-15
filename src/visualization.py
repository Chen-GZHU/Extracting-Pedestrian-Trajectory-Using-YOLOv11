import pandas as pd
import matplotlib.pyplot as plt

# 读取TXT文件
data = []
with open(r"output_tracks.txt", 'r') as file:
    for line in file:
        # 按空格拆分每行数据
        values = line.split()

        # 提取所需的字段
        frame = values[0]
        category = 'A' if values[1] == '1' else 'B'  # 类别A或B
        unique_id = values[2]
        x = float(values[3])
        y = float(values[4])
        w = float(values[5])
        h = float(values[6])

        # 计算物体的中心坐标 (cx, cy)
        cx = x + w / 2
        cy = y + h / 2

        # 保存结果
        data.append([frame, category, unique_id, cx, cy])

# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=['Frame', 'Category', 'ID', 'CX', 'CY'])
# 保存为CSV文件
df.to_csv('J1.csv', index=False)
print("Data has been successfully converted to CSV format.")

# 读取CSV文件
Df = pd.read_csv("J1.csv")
plt.rcParams['font.family'] = 'Times New Roman'
# 设置画布
plt.figure(figsize=(10, 6))
# 绘制每个人的轨迹
for unique_id in Df['ID'].unique():
    # 获取该行人的所有轨迹数据
    person_data = Df[Df['ID'] == unique_id]

    # 根据类别决定颜色
    color = 'cyan' if person_data['Category'].iloc[0] == 'A' else 'magenta'

    # 绘制该行人的轨迹
    plt.plot(person_data['CX'], person_data['CY'], color=color,
             label=f'ID: {unique_id}' if person_data['Category'].iloc[0] == 'A' else "")
# 添加标签和标题
plt.xlabel('X Coordinate', fontsize=25)
plt.ylabel('Y Coordinate', fontsize=25)

# 显示图像
plt.show()