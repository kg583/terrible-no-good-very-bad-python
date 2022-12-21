# Why does this exist?

The itch to make abhorrent things from Guido's little rascal of a language is a strong one. The initial subject of this particular excursion was the `@` operator, and no I don't mean decorator syntax. I mean the binary version, the unceremoniously unloved matrix multiplication operator, a.k.a. `__matmul__`.

Now, one asks: what *else* do you use `@` for? That's right: email addresses. Thus began the journey to make `@` send an email... somehow. Unfortunately, all the ways one might try to develop a framework such that `__matmul__` does what you want are a bit convoluted for `@` to even make sense in the end (i.e. appear *outside* a string literal).

So, this project developed a new goal: violate the inner cogs of Python's grammar so viciously as to allow one to type the headers and contents of an email akin to how it would appear in an actual email service. With a bit of finagling and context managing, I am quite happy with the result. Anyone who can deduce why its called `bushel` gets a cookie.

# Why is this code bad?

It shouldn't take long for the careful reader to realize that the source code for `bushel` involves walking the AST of a file *after* an error is thrown for how absolutely disgusting the AST is. I tried my best to make the custom parse as lax as possible, but many concessions had to be made. Thus, if you want to ensure that anything works at all, follow the format of `examples.py`. As much as it might be convenient over constructing a whole host of email-adjacent objects in somewhat unwieldy ways, `bushel` is not any form of airtight improvement.

# Why is this code not not good?

Though we have stripped Python of its actual meaning and replaced it with MIME headers, there is some good to be gleaned here. I might draw the interested reader to the module's use of context managers, the primary enabler of all our tomfoolery. Context managers, those buggers that hide behind your favorite `with` statements, are pretty powerful, and the `contextlib` built-in contains even more recipes and utilities.

The implementation of `bushel` is also decently robust, with rudimentary syntax checking and moderately okay file handling. You *can* use this to send the occasional email, and I've done well to make it not the worst idea, but nonetheless I have no idea why you would want to.