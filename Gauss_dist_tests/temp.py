import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt

# arr = [False, False]
# # arr = False
#
# if arr:
#     print("if(arr) = True")
# else:
#     print("if(arr) = False")
#
#
# dir = "aaa/"
#
# print(f"abc/{dir}efg")
#
# arrb = [1, 2, 3, 4]
# # arrb = False
#
# if arrb:
#     print("if(arrb) = True")
# else:
#     print("if(arrb) = False")
#
# # print(f"arrb.all: {arrb.all()}")
# print(f"isinstance(arrb) = {isinstance(arrb, list)}")
#
# mu = 0
#
# print(f"type(mu) = {type(mu)}")
#
# if isinstance(mu, bool):
#     print(f"type(mu) = bool")
# else:
#     print(f"type(mu) = int")
#
# print(arrb**2)


n_qubits = 4
dim = 2 ** n_qubits

x = np.arange(dim, dtype=float)
y = [4.69423103e-04, 2.70134344e-03, 1.21065814e-02, 4.22561211e-02,
 1.14864046e-01, 2.43167188e-01, 4.00914914e-01, 5.14784940e-01,
 5.14784940e-01, 4.00914914e-01, 2.43167188e-01, 1.14864046e-01,
 4.22561211e-02, 1.21065814e-02, 2.70134344e-03, 4.69423103e-04]
# y = [0.17678442 0.17678439 0.17678432 0.1767842  0.17678404 0.17678382
#  0.17678356 0.17678325 0.1767829  0.17678249 0.17678204 0.17678155
#  0.176781   0.17678041 0.17677977 0.17677908 0.17677834 0.17677756
#  0.17677673 0.17677585 0.17677493 0.17677396 0.17677294 0.17677187
#  0.17677075 0.17676959 0.17676838 0.17676713 0.17676582 0.17676447
#  # 0.17676307 0.17676162]

plt.figure(figsize=(8, 4))
plt.plot(x, y, marker='o')
plt.title("Dyskretny rozkład Gaussa")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 4))
plt.bar(x, y, width=0.8)
plt.title("Dyskretny rozkład Gaussa – wersja słupkowa")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

xs = np.linspace(x.min(), x.max(), 500)
spline = make_interp_spline(x, y, k=3)
ys = spline(xs)

plt.figure(figsize=(8, 4))
plt.plot(xs, ys)
plt.scatter(x, y, color="black", s=20)
plt.title("Dyskretny rozkład Gaussa – wygładzony wykres")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.show()




























