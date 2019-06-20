from PIL import Image, ImageFilter
import tensorflow as tf

def imageprepare(filepath): 
    im = Image.open(filepath) #读取的图片所在路径，注意是28*28像素
    im = im.convert('L')
    tv = list(im.getdata()) 
    # tva = [(255-x)*1.0/255.0 for x in tv] 
    return tv

def weight_variable(shape):
    initial = tf.truncated_normal(shape,stddev = 0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1,shape = shape)
    return tf.Variable(initial)

def conv2d(x,W):
    return tf.nn.conv2d(x, W, strides = [1,1,1,1], padding = 'SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

def run_predict(filepath):
    result = imageprepare(filepath)
    x = tf.placeholder(tf.float32, [None, 784])

    y_ = tf.placeholder(tf.float32, [None, 10])

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

    saver = tf.train.Saver()

    sess.run(tf.global_variables_initializer())
    saver.restore(sess, "models/softmax_model.ckpt") #使用模型，参数和之前的代码保持一致

    prediction=tf.argmax(y,1)
    predint=prediction.eval(feed_dict={x: [result]}, session=sess)

    return predint[0]