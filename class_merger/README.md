# Why does this exist?

There came a scenario where I had a base class that designated a number of function prototypes. Different groups of these functions performed rather different tasks, but would coaelesce in the end to achieve a complete implementation of the base class. To save myself and others the mental strain of having to parse the implementation contained entirely within one derived class, I thought it best to split the class up, then unite everything together at the end through multiple inheritance (because unlike SOME languages Python can actually do that).

The trouble arose when some functions were implemented twice, and both implementations needed to be called in the final class. The concept of "additive" or "merged" inheritance as a way to accomplish this felt like a no-brainer to me: instead of overriding each method, just call every parent for that method in order, easy peezy.

# Why is this code bad?

It was not easy peezy. As you can see by inspection, the code to run down the MRO and call each parent is a mess. Its uncleanliness is most evidenced by the need to modify `__getattribute__` (in a pretty non-trivial way at that), a method override that only rears its ugly head in the most hacky of Python projects. The heavy reliance on exception catching is not a saving grace either. The package in its current form took several hours to put together, with each iteration increasing both my enjoyment of the project for its sheer devilishness and its inexcusable violations of every practical coding guideline thereof.

# Why is this code not not good?

Despite its obvious abhorrent nature to any moderately-seasoned Python programmer, this package does what it says on the tin, and quite well. The majority of edge cases can really only arise by engaging in this level of class hacking yourself. Most importantly, though, casual use of this package advocates for the general concept of "additive' or "merged" inheritance in a natural way. Container classes or similar patterns are usually the solution when presented with such a conundrum, but have two big flaws:

1. Sometimes containers can't be used, as in the case of deriving from a base class you have no access to but must be able to implement by the end
2. Containers miss the point of organizing methods this way in the first place: the derived class does not "contain" or "wrap" its component classes; it *is* its component classes put together.

I would be interested in exploring this strange flavor of OOP in the future, and perhaps have been beaten to the punch by some language I'm not familiar with. But for now, we must live with terrible code to do terrible things, until the presence of elegant code makes those same things elegant too.
