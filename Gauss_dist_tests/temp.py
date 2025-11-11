
arr = [False, False]
# arr = False

if arr:
    print("if(arr) = True")
else:
    print("if(arr) = False")


dir = "aaa/"

print(f"abc/{dir}efg")

arrb = [1, 2, 3, 4]
# arrb = False

if arrb:
    print("if(arrb) = True")
else:
    print("if(arrb) = False")

# print(f"arrb.all: {arrb.all()}")
print(f"isinstance(arrb) = {isinstance(arrb, list)}")

mu = 0

print(f"type(mu) = {type(mu)}")

if isinstance(mu, bool):
    print(f"type(mu) = bool")
else:
    print(f"type(mu) = int")

print(arrb**2)
