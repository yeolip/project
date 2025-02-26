import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import make_gaze as mg
from util_calc import *
import datetime as dt
import subprocess

idx = 0
pre_roi =0

def update_graph(num):
    data=df[df['time']==num]
    graph._offsets3d = (data.x, data.y, data.z)
    title.set_text('3D Test, time={}'.format(num))

def extract_resultRoi_from_data(inputPath):
    print("//////////", funcname(), "//////////")
    extGT = pd.read_csv(inputPath)

    # h_x = extData.loc[tindex, 'HSVL_MS_S_Head_Pos_Veh_X']
    # h_y = extData.loc[tindex, 'HSVL_MS_S_Head_Pos_Veh_Y']
    # h_z = extData.loc[tindex, 'HSVL_MS_S_Head_Pos_Veh_Z']
    # in_x = extData.loc[tindex, 'intersect_x_h']
    # in_y = extData.loc[tindex, 'intersect_y_h']
    # in_z = extData.loc[tindex, 'intersect_z_h']

    df_extGT = extGT[['f_frame_counter_left_camera', 'HSVL_MS_S_Head_Pos_Veh_X', 'HSVL_MS_S_Head_Pos_Veh_Y', 'HSVL_MS_S_Head_Pos_Veh_Z','intersect_x_h', 'intersect_y_h', 'intersect_z_h','roi_idx_h']]
    df_extGT = df_extGT.dropna()

    # print('df_extGT\n\n', df_extGT)
    return df_extGT

def render_fix_roi(pROI, nMax=-1):
    # fig = plt.figure(figsize=(10, 8))
    # ax3 = fig.add_subplot(111, projection='3d')
    #
    # plt.title('3D gaze target ROI')
    pROI = pROI.sort_values(['tID'], ascending=True)

    for i in pROI.index:  #[0:nMax]
        # print(pROI.tID[i])
        # print(pROI.tTargetName[i])
        # print(pROI.ttop_left[i][0],pROI.ttop_left[i][1],pROI.ttop_left[i][2])
        # print(pROI.ttop_right[i])
        # print(pROI.tbottom_left[i])
        # print(pROI.tbottom_right[i])
        x0 = pROI.ttop_left[i][0] * 1000
        y0 = pROI.ttop_left[i][1] * 1000
        z0 = pROI.ttop_left[i][2] * 1000
        # ax3.scatter(xs=x, ys=y, zs=z, label=i[1])
        x1 = pROI.ttop_right[i][0] * 1000
        y1 = pROI.ttop_right[i][1] * 1000
        z1 = pROI.ttop_right[i][2] * 1000
        # ax3.scatter(xs=x, ys=y, zs=z, label=i[1])
        x2 = pROI.tbottom_left[i][0] * 1000
        y2 = pROI.tbottom_left[i][1] * 1000
        z2 = pROI.tbottom_left[i][2] * 1000
        # ax3.scatter(xs=x, ys=y, zs=z, label=i[1])
        x3 = pROI.tbottom_right[i][0] * 1000
        y3 = pROI.tbottom_right[i][1] * 1000
        z3 = pROI.tbottom_right[i][2] * 1000
        # print([x0,x1,x3,x2])
        ax3.scatter(xs=np.array([x0, x1, x3, x2]), ys=np.array([y0, y1, y3, y2]), zs=np.array([z0, z1, z3, z2]))
        ax3.plot([x0, x1, x3, x2, x0], [y0, y1, y3, y2, y0], [z0, z1, z3, z2, z0],'-', alpha=0.7,
                 label=str("%.2d_" % pROI.tID[i]) + pROI.tTargetName[i])

        # X = np.array([[x0, x1], [x2, x3]])
        # Y = np.array([[y0, y1], [y2, y3]])
        # Z = np.array([[z0, z1], [z2, z3]])
        # ax3.plot_surface(X, Y ,Z ,edgecolor = 'black',rstride = 1,cstride = 1,alpha = 0.6)
        # ax3.plot3D([x0, x1, x3, x2, x0], [y0, y1, y3, y2, y0], [z0, z1, z3, z2, z0],  alpha=0.6,
        #            label=str("%.2d_" % pROI.tID[i]) + pROI.tTargetName[i])

    # ax3.plot_surface(X, Y, Z, edgecolor='black', rstride=1, cstride=1, alpha=0.3, color='blue')

    # ax3.set_zlim(-1500, 1500)
    ax3.set_title("3D gaze target ROI")
    ax3.set_xlabel('veh X', fontsize=16)
    ax3.set_ylabel('veh Y', fontsize=16)
    ax3.set_zlabel('veh Z', fontsize=16)
    ax3.legend(loc='center left', bbox_to_anchor=(-0.15, 0.5), fontsize='small')
    #camera view = up->down
    # ax3.view_init(+95, 0)

    #camera view = front->back
    ax3.view_init(-3, 0)
    ax3.azim = 180

    #camera view = back->front
    # ax3.view_init(-3, 0)

    ax3.dist = 8
    # plt.show()
    pass

def print_current_time():
    tnow = dt.datetime.now()
    print('%s-%2s-%2s %2s:%2s:%2s' % (tnow.year, tnow.month, tnow.day, tnow.hour, tnow.minute, tnow.second))

def update_graph2(num):
    global idx, pre_roi
    print_current_time()
    t_x= extData.intersect_x_h[idx]
    t_y= extData.intersect_y_h[idx]
    t_z= extData.intersect_z_h[idx]
    s_x= extData.HSVL_MS_S_Head_Pos_Veh_X[idx]
    s_y= extData.HSVL_MS_S_Head_Pos_Veh_Y[idx]
    s_z= extData.HSVL_MS_S_Head_Pos_Veh_Z[idx]
    t_roi = extData.roi_idx_h[idx]

#    print(t_roi, "pre_roi", pre_roi)
    if (pre_roi != t_roi):
        for i in ret_ExtROI.index:
            if(t_roi == ret_ExtROI.tID[i]):
#                print(i)
                x0 = ret_ExtROI.ttop_left[i][0] * 1000
                y0 = ret_ExtROI.ttop_left[i][1] * 1000
                z0 = ret_ExtROI.ttop_left[i][2] * 1000
                x1 = ret_ExtROI.ttop_right[i][0] * 1000
                y1 = ret_ExtROI.ttop_right[i][1] * 1000
                z1 = ret_ExtROI.ttop_right[i][2] * 1000
                x2 = ret_ExtROI.tbottom_left[i][0] * 1000
                y2 = ret_ExtROI.tbottom_left[i][1] * 1000
                z2 = ret_ExtROI.tbottom_left[i][2] * 1000
                x3 = ret_ExtROI.tbottom_right[i][0] * 1000
                y3 = ret_ExtROI.tbottom_right[i][1] * 1000
                z3 = ret_ExtROI.tbottom_right[i][2] * 1000


                X = np.array([[x0, x1], [x2, x3]])
                Y = np.array([[y0, y1], [y2, y3]])
                Z = np.array([[z0, z1], [z2, z3]])
#                print(X,Y,Z)
                pre_roi = t_roi
#                print("update preroi", pre_roi)

                graph_roi[0].remove()
                graph_roi[0] = ax3.plot_surface(X, Y ,Z, edgecolor = 'black',rstride = 4,cstride = 4,alpha = 0.6)
                break
    # print(i)
#    print('idx',idx, "pos=", t_x, t_y,t_z, "//", s_x,s_y,s_z)
    graph_target.set_data(t_x,t_y)
    graph_target.set_3d_properties(t_z)
    graph_mideye.set_data(s_x,s_y)
    graph_mideye.set_3d_properties(s_z)
    graph_gaze.set_data(np.array([s_x, t_x]), np.array([s_y, t_y]))
    graph_gaze.set_3d_properties(np.array([s_z, t_z]))
    #  = ax3.plot(xs=(s_x, t_x), ys=(s_y, t_y), zs=(s_z, t_z))

    # title.set_text('3D gaze target ROI, num=')
    title.set_text('3D gaze target ROI, num={}'.format(int(idx)))
    idx+=1
    return title, graph_gaze, graph_target, graph_mideye, ax3 #, graph_roi
    # return ax3

if __name__ == '__main__':
    print("\n\n\n make_gaze test/////////////////////")
    if(0):
        sys.stdout = open('DebugLog.txt', 'w')

    fps = 54  # frame per sec
    frn = 3224  # frame number of the animation
    mpl.rcParams['path.simplify_threshold'] = 1.0
    mpl.rcParams['agg.path.chunksize'] = 10000

    fig = plt.figure(figsize=(10, 8))
    ax3 = fig.add_subplot(111, projection='3d')
    title = ax3.set_title("3D gaze target ROI")

    inputPath_ROI = "./refer/roi_config.json"
    obj = mg.make_gaze_and_roi()
    ret_roi = obj.load_jsonfile_ROI(inputPath_ROI)
    ret_ExtROI = obj.extract_availData_from_3D_target_ROI(ret_roi)
    render_fix_roi(ret_ExtROI)

    extData = extract_resultRoi_from_data('./out/basegaze_output000.csv')
    print('\n\n\n')

    extData = extData.astype({'intersect_x_h': int,
                              'intersect_y_h': int,
                              'intersect_z_h': int})
    graph_target, = ax3.plot(extData.intersect_x_h[0:2], extData.intersect_y_h[0:2], extData.intersect_z_h[0:2], marker='x', color='b')
    graph_mideye, = ax3.plot(extData.HSVL_MS_S_Head_Pos_Veh_X[0:2], extData.HSVL_MS_S_Head_Pos_Veh_Y[0:2], extData.HSVL_MS_S_Head_Pos_Veh_Z[0:2], marker='D', color='black')
    graph_gaze, = ax3.plot([extData.HSVL_MS_S_Head_Pos_Veh_X[0],extData.intersect_x_h[0]], [extData.HSVL_MS_S_Head_Pos_Veh_Y[0],extData.intersect_y_h[0]],
                             [extData.HSVL_MS_S_Head_Pos_Veh_Z[0],extData.intersect_z_h[0]], linewidth=3, color='springgreen')
    # graph_gaze, = ax3.plot([extData.HSVL_MS_S_Head_Pos_Veh_X,extData.intersect_x_h], [extData.HSVL_MS_S_Head_Pos_Veh_Y,extData.intersect_y_h],
    #                          [extData.HSVL_MS_S_Head_Pos_Veh_Z,extData.intersect_z_h])
    X = np.array([[0, 1], [0, 1]])
    graph_roi = [ax3.plot_surface(X, X, X, edgecolor='black', rstride=4, cstride=4, alpha=0.6)]


    ani = FuncAnimation(fig, update_graph2, frn, blit=False, interval=1000/fps)
    # fargs = (extData)
    # plt.show()
    # print(1/0)
    
    fn = '3d_gaze_roi_result_15'
    ani.save(fn + '.mp4', writer='ffmpeg', fps=fps)
    # ani.save(fn + '.gif', writer='imagemagick', fps=fps)
    # cmd = 'magick convert %s.gif -fuzz 5%% -layers Optimize %s_r.gif' % (fn, fn)
    # print(cmd)
    # subprocess.check_output(cmd)
    plt.show()

    # fig, ax = plt.subplots()
    # ax.set_xlim(0, 2 * np.pi)
    # ax.set_ylim(-1.2, 1.2)
    #
    # x, y = [], []
    # line, = plt.plot([], [], 'bo')
    #
    # # ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128))
    # ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128))
    #
    # plt.show()
    # Attaching 3D axis to the figure
    # fig = plt.figure()
    # ax = Axes3D(fig)
    #
    # # Fifty lines of random 3-D lines
    # data = [Gen_RandLine(25, 3) for index in range(50)]
    #
    # # Creating fifty line objects.
    # # NOTE: Can't pass empty arrays into 3d version of plot()
    # lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]
    #
    # # Setting the axes properties
    # ax.set_xlim3d([0.0, 1.0])
    # ax.set_xlabel('X')
    #
    # ax.set_ylim3d([0.0, 1.0])
    # ax.set_ylabel('Y')
    #
    # ax.set_zlim3d([0.0, 1.0])
    # ax.set_zlabel('Z')
    #
    # ax.set_title('3D Test')
    #
    # # Creating the Animation object
    # line_ani = FuncAnimation(fig, update_lines, 25, fargs=(data, lines),
    #                                    interval=50, blit=False)
    #
