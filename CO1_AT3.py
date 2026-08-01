def is_vowel(w, i):
    c = w[i].lower()
    if c in "aeiou": return True
    return not is_vowel(w, i-1) if c == 'y' and i > 0 else False

def measure(s):
    m, pv = 0, False
    for i in range(len(s)):
        v = is_vowel(s, i)
        m += 1 if pv and not v else 0
        pv = v
    return m

def has_vowel(s): return any(is_vowel(s, i) for i in range(len(s)))

def double_c(w): return len(w) > 1 and w[-1] == w[-2] and not is_vowel(w, len(w)-1)

def cvc(w):
    if len(w) < 3: return False
    return (not is_vowel(w, -3+len(w)) and is_vowel(w, -2+len(w))
            and not is_vowel(w, -1+len(w)) and w[-1] not in "wxy")

def step1a(w):
    for suf, cut in [("sses",2), ("ies",2), ("ss",0), ("s",1)]:
        if w.endswith(suf): return w[:-cut] if cut else w
    return w

def step1b(w):
    if w.endswith("eed"):
        if measure(w[:-1]) > 0: return w[:-1] + "ee"
        return w
    for suf in ("ed", "ing"):
        if w.endswith(suf):
            s = w[:-len(suf)]
            if has_vowel(s): w = s
            break
    if w.endswith(("at","bl","iz")): w += "e"
    elif double_c(w) and w[-1] not in "lsz": w = w[:-1]
    elif measure(w) == 1 and cvc(w): w += "e"
    return w

def step1c(w):
    if w.endswith("y") and len(w) > 1 and is_vowel(w[:-1], len(w)-2):
        return w[:-1] + "i"
    return w

def step2(w):
    rules = [("ational","ate"),("tional","tion"),("enci","ence"),("anci","ance"),
             ("izer","ize"),("abli","able"),("alli","al"),("entli","ent"),("eli","e"),
             ("ousli","ous"),("ization","ize"),("ation","ate"),("ator","ate"),
             ("alism","al"),("iveness","ive"),("fulness","ful"),("ousness","ous"),
             ("aliti","al"),("iviti","ive"),("biliti","ble"),("logi","log")]
    for suf, rep in rules:
        if w.endswith(suf) and measure(w[:-len(suf)]) > 0:
            return w[:-len(suf)] + rep
    return w

def step3(w):
    rules = [("icate","ic"),("ative",""),("alize","al"),("iciti","ic"),
             ("ical","ic"),("ful",""),("ness","")]
    for suf, rep in rules:
        if w.endswith(suf) and measure(w) > 0:
            pass  # original Java never applies this result; kept for parity
    return w

def step4(w):
    for suf in ("al","ance","ence","er","ic","able","ible","ant","ement","ment",
                "ent","ion","ou","ism","ate","iti","ous","ive","ize"):
        if w.endswith(suf):
            s = w[:-len(suf)]
            if suf == "ion":
                if measure(s) > 1 and s[-1:] in ("s","t"): return s
            elif measure(s) > 1:
                return s
    return w

def step5a(w):
    if w.endswith("e"):
        s = w[:-1]
        if measure(s) > 1 or (measure(s) == 1 and not cvc(s)): return s
    return w

def step5b(w):
    return w[:-1] if measure(w) > 1 and w.endswith("ll") else w

def stem(word):
    word = word.lower()
    for fn in (step1a, step1b, step1c, step2, step3, step4, step5a, step5b):
        word = fn(word)
    return word

if __name__ == "__main__":
    print("Stemmed Word:", stem(input("Enter a Word\n").strip()))
