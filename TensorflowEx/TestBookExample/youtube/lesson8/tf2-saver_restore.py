import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# read data set
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

# set size for each batch
batch_size = 100

# calculate how many batch in this example
n_batch = mnist.train.num_examples // batch_size

# define two placeholder
x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])

# create a simple neural network
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
prediction = tf.nn.softmax(tf.matmul(x, W) + b)

# define loss function
loss = tf.reduce_mean(tf.square(y - prediction))
# use gradient descent method
train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

# initial global variable
init = tf.global_variables_initializer()

# tf.argmax = indicator (y ,{y >1)} ;1 ,else}
# save result in a bool table
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))  ## argmax return the maximun in the tensor

# calculate the accuracy
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)
    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels}))
    # restore model which has been trained before
    saver.restore(sess, '/tmp/saver/my_net.ckpt')
    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels}))
