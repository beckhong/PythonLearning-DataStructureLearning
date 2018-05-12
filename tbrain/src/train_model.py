from tbrain.reference_package.import_tfbrain_data import read_tbrain_data
from tbrain.module.lstm_model import LSTMRNN
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import copy

BATCH_START = 0  # 定義batch開始處
TIME_STEPS = 10  # 每一層有幾個ＲＮＮ - 定義10個工作天一層
BATCH_SIZE = 35  # 定義每次batch提出的量的大小
INPUT_SIZE = 1  # 放入參數個數
OUTPUT_SIZE = 1  # 輸出參數個數
CELL_SIZE = 10  # 多少個hidden units
LEARNING_RATE = 0.006  # 學習率
TRAIN_LOOP = 96  # 迭代次數
SAVING_DIR_FILE_NAME = '/Users/jimweng/PythonLearning-DataStructureLearning/tbrain/src/save_model/test.model.ckpt'

Df = read_tbrain_data('../data/taetfp.csv')  # 50 51 52
# 使用code 50的data
trainDf = Df[(Df.code == 50)]

# declaration global variable
final_pred_array = []
final_average = 0
final_std = 0


# normalization
def normalization(data):
    global final_average, final_std
    data_average = np.average(data)
    data_std = np.std(data)
    z_data = (data - data_average) / data_std

    final_average = data_average
    final_std = data_std

    return z_data


def get_batch():
    global BATCH_START, TIME_STEPS
    start_pt = BATCH_START
    end_pt = BATCH_START + TIME_STEPS * BATCH_SIZE
    xs = np.array(copy.copy(trainDf.date[start_pt:end_pt]).reshape(BATCH_SIZE, TIME_STEPS))
    res = np.array(copy.copy(trainDf.open[1 + start_pt:1 + end_pt]).reshape(BATCH_SIZE, TIME_STEPS))
    res = normalization(res)
    seq = np.array(copy.copy(trainDf.close[start_pt:end_pt]).reshape(BATCH_SIZE, TIME_STEPS))
    seq = normalization(seq)

    BATCH_START += TIME_STEPS
    return [seq[:, :, np.newaxis], res[:, :, np.newaxis], xs]


if __name__ == '__main__':
    model = LSTMRNN(TIME_STEPS, INPUT_SIZE, OUTPUT_SIZE, CELL_SIZE, BATCH_SIZE, LEARNING_RATE)
    sess = tf.Session()
    merged = tf.summary.merge_all()
    # writer = tf.summary.FileWriter("logs", sess.graph)

    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    sess.run(init)

    plt.ion()
    plt.show()

    # 根據data量做調整，目前code 50有data 13XX
    # 能做迭代次數為 13XX/ (batch_size*step_size)
    for i in range(TRAIN_LOOP):
        seq, res, xs = get_batch()
        if i == 0:
            feed_dict = {
                model.xs: seq,
                model.ys: res,
                # create initial state
            }
        else:
            feed_dict = {
                model.xs: seq,
                model.ys: res,
                model.cell_init_state: state  # use last state as the initial state for this run
            }

        _, cost, state, pred = sess.run(
            [model.train_op, model.cost, model.cell_final_state, model.pred],
            feed_dict=feed_dict)

        print('the %d_th cost: %.3f' % (i, round(cost, 4)))
        result = sess.run(merged, feed_dict)

        # plotting
        plt.plot(xs[0, :], res[0].flatten(), 'r', xs[0, :], pred.flatten()[:TIME_STEPS], 'b--')
        # plt.ylim((-1.2, 1.2))
        plt.draw()
        plt.pause(.3)
    saver.save(sess, SAVING_DIR_FILE_NAME, global_step=96)
    print(xs[-1:])
    final_pred_array = pred
    final_res_array = res

# 打印出平均數以及標準差
print("the final_close average is %.3f" % final_average)
print("the final_close std is %.3f" % final_std)

print("the final pred_array is ", final_pred_array.flatten()[-TIME_STEPS * 2:])
print("the final pred result is ", final_res_array.flatten()[-TIME_STEPS * 2:])
