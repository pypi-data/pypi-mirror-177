# Journal Prompts
A corpus of journal prompts with a finder facade

### Usage
```python
from journal_prompts import find_random_question

find_random_question()
```
Each function call returns a single random question.

### Results
```
What's the funniest brand name you've ever seen?
Have you ever broken a safety rule? What was it?
What's the most ridiculous warning sign you've ever seen?
Have you ever tried to lick your elbow?
...
Do you believe in UFOs, and have you seen one?
```

### Corpus Size
```python
from journal_prompts import corpus_size
assert corpus_size() == 3642
```
