
## Else Values ##

1. As an assignment statement
keeps previous Values

```
decl x 42
x = if (False) { 43 }

assert(x == 42)

x = if (True) { 43 }

assert(x == 43)
```

2. As an expression
return None
```
decl x if (False) 42
assert(x == None)

assert((if (False) 42) == None)
```

3. As an expression statement
Returns previous value

```
def foo []{
    42
    if (False) {
        10
    }
}

def bar []{
    12
    if (True) {
        43
    }
}

assert(foo() == 42)
assert(foo() == 43)
```

4. As a yield statement
continue

```
numbers = [1, 2, 3]
odds = for i in (numbers) if (i % 2 == 1) i

assert(odds == [1, 3])

```
