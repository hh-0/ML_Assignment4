import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import logsumexp
# def logSumExp(ns):
#     max = np.max(ns)
#     ds = ns - max
#     sumOfExp = np.exp(ds).sum()
#     return max + np.log(sumOfExp)
X = np.array([1,2,3,4,5,6])
states = np.array([0,1])

B = np.array([[1/6, 1/6, 1/6, 1/6, 1/6, 1/6], [1/10, 1/10, 1/10, 1/10, 1/10, 5/10]])
A = np.array([[0.95, 0.05],[0.1, 0.9]])

rolls = []
die = []
current_state = 0
for i in range(100):
    face = np.random.choice(X, p=B[current_state])
    rolls.append(face)
    die.append(current_state)

    r = np.random.random()
    if r > A[current_state][current_state]:
        current_state ^= 1
    

rolls = np.array(rolls) - 1
die = np.array(die)

K = 2
T = rolls.shape[0]
Alpha = np.empty((K,T))

Alpha[:, 0] = np.log(0.5) + np.log(B[:,rolls[0]])
# Alpha[:, 0] = 0.5 * B[:,rolls[0]]

for t in range(1,T):
    for k in range(K):
        Alpha[k,t] = np.log(B[k, rolls[t]]) + logsumexp([Alpha[i,t-1] + np.log(A[i, k]) for i in range(K)])
        # Alpha[k,t] = B[k, rolls[t]] * np.sum([Alpha[i,t-1] * A[i, k] for i in range(K)])

normalized_alpha = Alpha[1,:]/np.sum(Alpha, axis=0)

# normalized_alpha = np.array([Alpha[:,i]/np.sum(Alpha[:,i]) for i in range(Alpha.shape[1])])
# n_alpha = Alpha[0,:]/np.sum(Alpha[0])
x = np.arange(0,100)

plt.plot(x, normalized_alpha)
plt.plot(x, die)
plt.show()