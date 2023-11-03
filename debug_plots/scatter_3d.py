import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import numpy as np

def plot_3d_scatter(freemocap_data, qualisys_data):
    def plot_frame(f):
        ax.clear()
        ax.scatter(qualisys_data[f, :, 0], qualisys_data[f, :, 1], qualisys_data[f, :, 2], c='blue', label='Qualisys')
        ax.scatter(freemocap_data[f, :, 0], freemocap_data[f, :, 1], freemocap_data[f, :, 2], c='red', label='FreeMoCap')
        ax.set_xlim([-limit_x, limit_x])
        ax.set_ylim([-limit_y, limit_y])
        ax.set_zlim([-limit_z, limit_z])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        ax.set_title(f"Frame {f}")
        fig.canvas.draw_idle()

    mean_x = (np.nanmean(qualisys_data[:, :, 0]) + np.nanmean(freemocap_data[:, :, 0])) / 2
    mean_y = (np.nanmean(qualisys_data[:, :, 1]) + np.nanmean(freemocap_data[:, :, 1])) / 2
    mean_z = (np.nanmean(qualisys_data[:, :, 2]) + np.nanmean(freemocap_data[:, :, 2])) / 2

    ax_range = 1000
    limit_x = mean_x + ax_range
    limit_y = mean_y + ax_range
    limit_z = mean_z + ax_range

    fig = plt.figure(figsize=[10, 8])
    ax = fig.add_subplot(111, projection='3d')
    slider_ax = plt.axes([0.25, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    frame_slider = Slider(slider_ax, 'Frame', 0, len(qualisys_data) - 1, valinit=0, valstep=1)

    def update(val):
        frame = int(frame_slider.val)
        plot_frame(frame)

    frame_slider.on_changed(update)
    plot_frame(0)
    plt.show()
