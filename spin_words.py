def spin_words(sentence):
    words = sentence.split()
    spun_words = []
    for word in words:
        if len(word) >= 5:
            spun_words.append(word[::-1])
        else:
            spun_words.append(word)
    return " ".join(spun_words)

# Example Test Cases
print(f"'Hey fellow warriors' --> '{spin_words('Hey fellow warriors')}' (Expected: 'Hey wollef sroirraw')")
print(f"'This is a test' --> '{spin_words('This is a test')}' (Expected: 'This is a test')")
print(f"'This is another test' --> '{spin_words('This is another test')}' (Expected: 'This is rehtona test')")
