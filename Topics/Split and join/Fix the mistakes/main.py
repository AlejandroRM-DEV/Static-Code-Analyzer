text = input()
words = text.split()
for word in words:
    # finish the code here
    if word.lower().startswith("https://") or \
            word.lower().startswith("http://") or \
            word.lower().startswith("www."):
        print(word)