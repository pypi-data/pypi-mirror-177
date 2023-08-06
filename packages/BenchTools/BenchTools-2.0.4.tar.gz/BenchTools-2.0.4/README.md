# benchtools
A small project written in C, with a modular port to python. Performs benchmarks using functions.

[GitHub-BenchTools](https://github.com/PothpothBR/benchtools)

[GitHub-Issues](https://github.com/PothpothBR/benchtools/issues)

# Use example:
```python
from benchtools import addToBench, benchRound, clearRound
from typing import Any
```

create functions to bench
all functions using this template

```python
def myfuncName() -> None:
    "Your code here"
``` 

no args, no return.
if your execution recive args. encapsule it an parse the args properly.

```python
def myfuncNameWithArgs(arg1, arg2, arg3) -> Any:
    "Your code here"
```

example to encapsule
```python
myfuncNameWithArgsCorrect = lambda : myfuncNameWithArgs('arg1', 'arg2', 'arg3')
```

after it, you set the functions to bench table, make it calling addToBench
```python
addToBench(myfuncName, "beatifull alias", 4)
```

the first argument is your callable
the second is an alias for view
the third is an number of executions to get an average time, if 0 the function not is executed!

```python
addToBench(myfuncNameWithArgsCorrect, "second beatifull alias", 1)
addToBench(myfuncNameWithArgsCorrect, "another beatifull alias", 0) # this not execute!
```

after it, you like to benchmark, make it calling benchRound
```python
benchRound()
```

if you like to save the results, set True
```python
benchRound(True)
```

the file is benchmark.log.csv (comma separated, indexed)

in the end, to reset the benchmark system call clearRound

```python
clearRound()
```

after it, is free to set new bench function