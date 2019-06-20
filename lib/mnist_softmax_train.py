from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import os

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None


def Train(_):
  # Get train data
  mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

  # Create model
  x = tf.placeholder(tf.float32, [None, 784])
  W = tf.Variable(tf.zeros([784, 10]))
  b = tf.Variable(tf.zeros([10]))
  y = tf.matmul(x, W) + b

  y_ = tf.placeholder(tf.float32, [None, 10])

  cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
  train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()
  print("[*] Training mnist softmax")
  # Train
  for _ in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    if (_ + 1) % 100 == 0:
      print((_ + 1), "Trained")

  # Test trained model
  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  print("Total Accuracy: ", sess.run(accuracy, feed_dict={x: mnist.test.images,
                                      y_: mnist.test.labels}))
  saver = tf.train.Saver()
  dirname, filename = os.path.split(os.path.abspath(sys.argv[0])) 
  save_path = os.path.join(dirname, '../models/softmax_model.ckpt')
  saver.save(sess, save_path)

if __name__ == '__main__':
  # Run Training
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=Train, argv=[sys.argv[0]] + unparsed)