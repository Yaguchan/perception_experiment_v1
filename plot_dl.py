import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.linear_model import LinearRegression

def mid_log(x, y):
    return np.exp((np.log(x)+np.log(y))/2)

def delta_position(x, y):
    return [mid_log(x, y)], abs(x-y)


def main():
    
    # ms -> s
    M = 1000
    
    # x_data = np.array([100, 200, 400, 800, 1600])
    x_data = [0 for _ in range(10)]
    y_data = [0 for _ in range(10)]
    
    # 2（最大ミス・最小ミス除き）
    x_data[0], y_data[0] = delta_position(100, 66.75076331614126)
    x_data[1], y_data[1] = delta_position(133.24831594073302, 100)
    x_data[2], y_data[2] = delta_position(200, 166.09047193128922)
    x_data[3], y_data[3] = delta_position(235.1097756043987, 200)
    x_data[4], y_data[4] = delta_position(400, 368.07443717319535)
    x_data[5], y_data[5] = delta_position(465.18836007687634, 400)
    x_data[6], y_data[6] = delta_position(800, 749)
    x_data[7], y_data[7] = delta_position(879.3078845988229, 800)
    x_data[8], y_data[8] = delta_position(1600, 1460.72315104155)
    x_data[9], y_data[9] = delta_position(1724.10843270523, 1600)
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    print('------------------------------------')
    print('x_data            y_data')
    for x, y in zip(x_data, y_data):
        print(x[0], y)
    print('------------------------------------')
    
    # fitting
    def lod(x, A, B):
        return np.exp(A * np.log(x) + B)
        # return 10 ** (A * np.log10(x) + B)
    model = LinearRegression()
    model.fit(np.log(x_data[4:]), np.log(y_data[4:]))
    A_fit = model.coef_
    B_fit = model.intercept_
    C_fit = np.average(y_data[:4])
    print('fitting')
    print('A', A_fit[0])
    print('B', B_fit)
    print('C', C_fit)
    print('------------------------------------')
    
    # plot
    # point
    for i in range(len(x_data)): 
        plt.plot(x_data[i]/M, y_data[i]/M, '.', markersize=10, color='b') 
    
    # const
    plt.plot([0, 310/M], [C_fit/M, C_fit/M], 'r')
    
    # line
    x_range = np.linspace(310, 2000, 1000)
    x_s_range = x_range / M
    y_s_range = lod(x_range, A_fit, B_fit) / M
    plt.plot(x_s_range, y_s_range, 'r', label='Fitted Curve')
    
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)  
    plt.xlim(50/M, 2000/M)
    plt.xlabel('物理時間 t [s]', fontsize=30)
    plt.ylabel('弁別閾 Δt [s]', fontsize=30)
    plt.tick_params(labelsize=25)
    plt.show()

if __name__ == '__main__':
    main()