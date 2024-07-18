import matplotlib.pyplot as plt
import re

def read_placement(file_path):
    modules = []
    with open(file_path, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            idx = int(re.search(r'\d+', line).group())
            relative_position = tuple(map(float, re.findall(r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', file.readline())))
            is_filler = bool(int(re.search(r'\d+', file.readline()).group()))
            width = float(re.search(r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', file.readline()).group())
            height = float(re.search(r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', file.readline()).group())
            related_nets_line = file.readline().strip()
            related_nets = list(map(int, re.findall(r'\d+', related_nets_line))) if related_nets_line else []
            modules.append({
                'idx': idx,
                'relative_position': relative_position,
                'is_filler': is_filler,
                'width': width,
                'height': height,
                'related_nets': related_nets
            })
            file.readline()  # Read the empty line
    return modules

def plot_placement(modules):
    fig, ax = plt.subplots(figsize=(10, 10))

    # 绘制外围边界
    outer_boundary = plt.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(outer_boundary)

    rectangles = []
    for module in modules:
        x, y = module['relative_position']
        width = module['width']
        height = module['height']
        color = 'green' if module['is_filler'] else 'red'
        line_width = 0 if module['is_filler'] else 1
        rect = plt.Rectangle((x, y), width, height, linewidth=line_width, edgecolor=color, facecolor=color, alpha=0.4)
        rectangles.append((rect, module))
        ax.add_patch(rect)

    # 设置绘图范围
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)

    plt.gca().set_aspect('equal', adjustable='box')

    def on_move(event):
        for rect, module in rectangles:
            rect.set_edgecolor('green' if module['is_filler'] else 'red')
            rect.set_linewidth(0 if module['is_filler'] else 1)

        for rect, module in rectangles:
            contains, _ = rect.contains(event)
            if contains:
                for r, m in rectangles:
                    if set(m['related_nets']).intersection(set(module['related_nets'])):
                        r.set_edgecolor('black')
                        r.set_linewidth(3)
                break
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', on_move)

    plt.show()

if __name__ == '__main__':
    file_path = 'C:/Users/zhangzhijie/CLionProjects/untitled1/output/placement.txt'
    modules = read_placement(file_path)
    plot_placement(modules)
