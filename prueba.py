import matplotlib.pyplot as plt
import numpy.random as rnd

fig = plt.figure()
plt.subplot(231)
plt.imshow(rnd.random((100, 100)))
plt.subplot(232)
plt.imshow(rnd.random((100, 100)))
plt.subplot(233)
plt.imshow(rnd.random((100, 100)))
plt.subplot(234)
plt.imshow(rnd.random((100, 100)))
plt.subplot(235)
plt.imshow(rnd.random((100, 100)))
plt.subplot_tool()
plt.show()