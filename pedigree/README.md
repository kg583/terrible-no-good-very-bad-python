# Why does this exist?

The original problem and first attempt at a solution can be found in the README of `class_merger`. TL;DR: I want to be able to customize multiple inheritance, wherein parent class methods and attributes are combined in some way that isn't just picking the first one found in the MRO. My first attempt involved hacking `__getattribute__`, which has some nice runtime advantages but is also extremely unstable and just generally bad. So, I have since turned to metaclasses with surprisingly good results; so good I've given this one a proper name: `pedigree`, after the fact it combines a class's entire ancestry.

# Why is this code bad?

Metaclasses are dangerous. They can overwrite every fundamental assumption you have about the code you write, as I can almost guarantee that you have never seen any metaclass besides `type` (and if you have, you're some Django nerd). And, even though most dunder shenanigans have left the building, potentially unstable under-the-hood fiddling remains (which you could argue is neccesary for the project anyway). Unit testing is hard for this sort of thing, but hopefully `examples.py` provides enough demonstrations and checks.

# Why is this code not not good?

Even less abhorrent than its mixin-based predecessor, this packages also does exactly what it says on the tin, and this time actually seamlessly through the power of metaclasses. And just as with the mixin, use of this package advocates for the general concept of "additive" or "merged" inheritance in a natural way. Container classes or similar patterns are usually the solution when presented with such a conundrum, but have major flaws as previously discussed.

I would prefer you use this code over the mixin at this point, and that probably means the documentation here should be more completely ported over rather than just telling you to go read about obsolete code instead. Then again, its unlikely this content will *ever* see the light of day in a practical context, so if you've found your way over here you probably don't even care.
