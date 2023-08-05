# Like partial, but you can determine the order of *args

```python
pip install flexible-partial
```

```python
from flexible_partial import FlexiblePartial
import regex
from random import choice
from string import ascii_lowercase

text = """Hi, my friend, how are you?"""

allfus = [
    FlexiblePartial(
        regex.sub,
        True,  # this_args_first = True (choice(list(ascii_lowercase)) will be the first arg when the function is called)
        choice(list(ascii_lowercase)),
        flags=regex.IGNORECASE,
    )
    for x in range(10)
]

for alsw in allfus:
    print(f"Executing: {alsw}")
    text = alsw("P", text)
    print(text)

# Executing: regex.regex.sub('z', flags=regex.I)
# Hi, my friend, how are you?
# Executing: regex.regex.sub('o', flags=regex.I)
# Hi, my friend, hPw are yPu?
# Executing: regex.regex.sub('u', flags=regex.I)
# Hi, my friend, hPw are yPP?
# Executing: regex.regex.sub('y', flags=regex.I)
# Hi, mP friend, hPw are PPP?
# Executing: regex.regex.sub('z', flags=regex.I)
# Hi, mP friend, hPw are PPP?
# Executing: regex.regex.sub('b', flags=regex.I)
# Hi, mP friend, hPw are PPP?
# Executing: regex.regex.sub('k', flags=regex.I)
# Hi, mP friend, hPw are PPP?
# Executing: regex.regex.sub('w', flags=regex.I)
# Hi, mP friend, hPP are PPP?
# Executing: regex.regex.sub('k', flags=regex.I)
# Hi, mP friend, hPP are PPP?
# Executing: regex.regex.sub('a', flags=regex.I)
# Hi, mP friend, hPP Pre PPP?

text = """Hi, my friend, how are you?"""

allfus = [
    FlexiblePartial(
        regex.sub,
        False,  # this_args_first = False (text will be the last arg when the function is called)
        text,
        flags=regex.IGNORECASE,
    )
    for x in range(10)
]

for alsw in allfus:
    print(f"Executing: {alsw}")
    text = alsw(choice(list(ascii_lowercase)), choice(list(ascii_lowercase)))
    print(text)


# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, me friend, how are eou?
# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, mv friend, how are vou?
# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, my friend, hos are you?
# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, my frienh, how are you?
# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, my friend, how are you?
# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, my mriend, how are you?
# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, my friend, how are you?
# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, mv friend, how are vou?
# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, my friend, how are you?
# Executing: regex.regex.sub('Hi, my friend, how are you?', flags=regex.I)
# Hi, my friend, how rre you?
```
