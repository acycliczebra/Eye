



__main__ = [args]{

    i = try {
        s = input
        as_int = Int s # may throw exception
    } except {

    } else {

    }

    l = '1 2 3 4 5 6'
    f = [x]{ # a complicated function that only takes an integer not an integer list
        x = x * 2
    }




    ~ # ??
    42 `Int` # casting?
    l ! [x] x % 2 == 0 # 2 4 6 # filter
    l @ [x] x * 2      # 2 4 6 8 10 12 # map
    # # comment
    $ # ??
    % # directive
    3 ^ 2 # power
    (set 1, 2, 3)^ True^ # not the set, false
    True & False # non short circuiting
    a * b # mul
    a +* b # outer product
    a .* b # inner product
    A* # transpose
    a - b # min
    foo -- # function placeholder
    a + b # plus
    a ++ b # concat
    [] # function decl if attached to previous token, subscript
    a | b # or non short circuiting
    \ # ??
    "abc" # string
    'a b c' #list
    0:*-1 # range operator
    ; # statement end?
    'a b c' << d # push
    d >> 'a b c' # push front
    'a b c' >> # pop back
    << 'a b c' # pop front
    foo ?, 3 # partial application

    true
    false
    * #wildcard
    ... #etc
    inf
    nan
}
