import numpy as np
import matplotlib.pyplot as plt

num_vectors = 1000
num_clusters = 4
num_steps = 100

x_values = []
y_values = []
vector_value = []

for i in range(num_vectors):
    if np.random.random() > 0.5:
        x_values.append(np.random.normal(0.4, 0.7))
        y_values.append(np.random.normal(0.2, 0.8))
    else:
        x_values.append(np.random.normal(0.6, 0.4))
        y_values.append(np.random.normal(0.8, 0.5))

plt.plot(x_values, y_values, 'o', label='Input Data')
plt.legend()
plt.show()
