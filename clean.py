import os

for file in os.listdir("errors_pages"):
    os.remove("errors_pages/" + file)

for file in os.listdir("data"):
    os.remove("data/" + file)

for file in os.listdir("log"):
    os.remove("log/" + file)