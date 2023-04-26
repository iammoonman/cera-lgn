import requests
import random
import json

response = requests.get(
    f"https://www.planesculptors.net/set/splinters-of-novanda?json",
    headers={
        "User-Agent": "Python 3.9.13 CERA",
    },
)

data: dict = response.json()
cards: dict[str, dict] = data["cards"]
set = "c_son"
rarity = "M"

w = []
u = []
r = []
b = []
g = []
n = []
for k, c in cards.items():
    if c["colors"] == "B" and c["rarity"] == rarity:
        b.append([c["cardNumber"], set])
    if c["colors"] == "G" and c["rarity"] == rarity:
        g.append([c["cardNumber"], set])
    if c["colors"] is None and c["rarity"] == rarity:
        n.append([c["cardNumber"], set])
    if c["colors"] == "W" and c["rarity"] == rarity:
        w.append([c["cardNumber"], set])
    if c["colors"] == "U" and c["rarity"] == rarity:
        u.append([c["cardNumber"], set])
    if c["colors"] == "R" and c["rarity"] == rarity:
        r.append([c["cardNumber"], set])
random.shuffle(b)
random.shuffle(g)
random.shuffle(n)
random.shuffle(r)
random.shuffle(w)
random.shuffle(u)
l = []
print("Side A")
for aa, bb, cc in zip(w, u, r):
    l.append(aa)
    l.append(bb)
    l.append(cc)
print(json.dumps(l))
print("Side B")
l = []
for dd, ee in zip(b, g):
    l.append(dd)
    l.append(ee)
for i, f in enumerate(n):
    l.insert(i * 3, f)
print(json.dumps(l))