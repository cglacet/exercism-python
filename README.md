# exercism-python
My answers for the exercism.io python track. You can find my profile over here [exercism.io/cglacet](https://exercism.io/profiles/cglacet)

**2019 update** I'm sadly not back yet on Exercism.io, but I'm currently writting a few words about python here: ["One step closer to using Python properly
"](https://github.com/cglacet/Blog/tree/master/python#one-step-closer-to-using-python-properly). There are some overlaps with the content you can find here and it's still under construction, but I'll go in much more details on every subject I'll talk about.

## You should try Exercism.io
[Exercism.io](https://exercism.io) is an online learning platform with __feedback__. The feedback comes from experimented _mentors_ in the specific language that you choose. The main drawback when learning online is the lack of feedback, you can develop bad habits without even having a chance to be notified about it. I think exercism.io is a good idea to try solving that missing bit in online learning.

The process is simple:
__(i)__ you pick and download an exercise (_eg._, [kindergarten-garden](kindergarten-garden)),
__(ii)__ you solve and upload it,
__(iii)__ a mentor gives you feedback and you both work on improving the solution.

Mentoring is oriented tower language specific questions, but you also can get advises on complexity (algorithmic) issues.
<details>
<summary>
Here is an example of exchange I had with a mentor on handling optional parameters in python:
</summary>


> __Mentor__
>
>  Lines 12-14 could as easily be self.students = sorted(students or Garden.DEFAULT_CHILDREN_NAMES)
>
In my first iteration, [Lines 10-14](https://github.com/cglacet/exercism-python/blob/master/kindergarten-garden/kindergarten_garden_origin.py#L10-L14) looked like:

```python
def __init__(self, diagram, students=None):
    if students is not None:
        self.students = sorted(students)
    else:
        self.students = Garden.DEFAULT_CHILDREN_NAMES
```
>
> __Me__
>
> Isn't that considered a hack, is there a link to the specification of what this code does? I may be a bit old school but in my head, by default I'll always assume OR operator returns a boolean. I looked for it and [I'm not the only one being confused](https://stackoverflow.com/questions/4477850/python-and-or-operators-return-value). On the other hand I kind of like having that done in a single line (as this is an operation that is used a lot).
>
> I searched for a cleaner (to my non-python expert eyes), what do you feel about this:
>
>```python
>sorted(students if students is not None else Garden.DEFAULT_CHILDREN_NAMES)
>```
>
>Or even a bit more hacky version (I don't like too much relying on the fact that `None == False` either):
>```python
>sorted(students if students else Garden.DEFAULT_CHILDREN_NAMES)
>```
>I have to admit that I could use this solution and get over it, just because I would be lazzy to type `is not None` over and over.
>
> __Mentor__
>
> There's no hack, Python's and has always returned either the first operand that is False or the last operand that is True, and Python's `or` has always returned either the first operand that is True or the last operand that is False. The only "problem" here is that should someone explictly pass in an argument for students that is False equivalent (empty string, empty list, 0, empty dict, False, etc), you'll still get the fallback operation instead of either no result without error (empty string, empty list, empty dict) or an obscure error further down your code (0, 0.0, False). In Python None is considered False ... so are a lot of things, use it to your advantage, it's not a design flaw. If you really want to be pedantic, then use the ternary syntax, but be nicer to yourself and do Garden.DEFAULT_CHILREN_NAMES if students is None else students ... not None can hurt people.
>
> __Me__
>
> Ok. This problem you are talking about seems like a very big one to me. If you are used to test for `None` using shortcuts like this you have a pretty big risk of using it on a boolean variable at some point. I really feel like this is something that we should never do just because it can become an automatism. But maybe the bad habit is just to have some "boolean variable" set to None in the first place?
>
> __Mentor__
>
>  I think you're overestimating the problem of a default of `None` and a truth test. First because it's very -- even exceedlingy -- rare that you'll have a well-reasoned bit of code that has a parameter that logically should accept any potential false-y but not None argument passed in and treat it substantially differently than None, and second because in professional practice over millions of lines of code I've seen it bite somebody exactly once. And I couldn't and wouldn't describe what broke as well-reasoned.
>
> __Me__
>
> I'll try to trust you on this one, but I can't promise my paranoia won't catch up ...

This mentor was really thorough and we talk about 3-4 things in such details. To be honest not all mentors will take that much time for you, but a typical exchange will probably teach you at least one thing about the langage.

</details>

## Some selected exercises

**Solutions**
There is a solution attached to every problem, for some exercises I also provide a detailed explanation on my solution.
Exercise for which there are explanations have their names in **bold**, (for example **zipper**).


**Color codes**
first time in python ![#56BDFF](https://placehold.it/10/56BDFF/000000?text=+) | _easy_ ![#ABFF89](https://placehold.it/10/ABFF89/000000?text=+) | _not so easy_ ![#E8C14E](https://placehold.it/10/E8C14E/000000?text=+) | medium ![#FF7C63](https://placehold.it/10/FF7C63/000000?text=+) | hard ![#000000](https://placehold.it/10/000000/000000?text=+)

Exercises from the main track are:
 - ![#56BDFF](https://placehold.it/10/56BDFF/000000?text=+) [leap](leap) ([_.py solution_](leap/leap.py)) booleans and modulo
 - ![#ABFF89](https://placehold.it/10/ABFF89/000000?text=+) [Bob](bob) ([_.py solution_](bob/bob.py)) "switch-cases"
 - ![#ABFF89](https://placehold.it/10/ABFF89/000000?text=+) [allergies](allergies) ([_.py solution_](allergies/allergies.py)) range and enumerate
 - ![#ABFF89](https://placehold.it/10/ABFF89/000000?text=+) [sum of multiples](sum-of-multiples) ([_.py solution_](sum-of-multiples/sum_of_multiples.py)) range and sum
 - ![#E8C14E](https://placehold.it/10/E8C14E/000000?text=+) [kindergarten garden](kindergarten-garden) ([_.py solution_](kindergarten-garden/kindergarten_garden.py)) zip and default dictionaries
 - ![#E8C14E](https://placehold.it/10/E8C14E/000000?text=+) [grade school](grade-school) ([_.py solution_](grade-school/grade_school.py)) lazzy evealuation and sorting
 - ![#E8C14E](https://placehold.it/10/E8C14E/000000?text=+) [**saddle points**](saddle-points#saddle-points) ([_.py solution_](saddle-points/saddle_points.py)) object oriented programming and generators
 - ![#E8C14E](https://placehold.it/10/E8C14E/000000?text=+) [binary search](binary-search) ([_.py solution_](binary-search/binary_search.py)) algorithmic problem
 - ![#ABFF89](https://placehold.it/10/ABFF89/000000?text=+) [list operators](list-ops) ([_.py solution_](list-ops/list_ops.py))"Easier to ask for forgiveness than permission" (EFAP)
 - ![#FF7C63](https://placehold.it/10/FF7C63/000000?text=+) [**book store**](book-store#book-store) ([_.py solution_](book-store/book_store.py)) algorithmic problem (a little bit challenging. Try to achieve _O(n)_)
 - ![#ABFF89](https://placehold.it/10/ABFF89/000000?text=+) [24h clock](clock) ([_.py solution_](clock/clock.py)) Euclidian division (and modulo)
 - ![#56BDFF](https://placehold.it/10/56BDFF/000000?text=+) [two fer](two-fer) ([_.py solution_](two-fer/two_fer.py)) Not too sure why this exercise is here TBH.
 - ![#E8C14E](https://placehold.it/10/E8C14E/000000?text=+) [markdown](markdown) ([_.py solution_](markdown/markdown.py)) code review and regex.
 - ![#FF7C63](https://placehold.it/10/FF7C63/000000?text=+) [rest API](rest-api) ([_.py solution_](rest-api/rest_api.py)) I'm not too sure what this is about, you can have a look at my solution and tell me what you think.

Extra exercises that I think are interesting:
 - ![#E8C14E](https://placehold.it/10/E8C14E/000000?text=+) [bank account](bank-account) ([_.py solution_](bank-account/bank_account.py)): concurrency, decorators and errors
 - ![#FF7C63](https://placehold.it/10/FF7C63/000000?text=+) [**flatten array**](flatten-array#flatten-array) ([_.py solution_](flatten-array/flatten_array.py)): Python stack discussion (iterative array flattening)
 - ![#E8C14E](https://placehold.it/10/E8C14E/000000?text=+) [binary search tree](binary-search-tree) ([_.py solution_](binary-search-tree/binary_search_tree.py)): basically a simpler version of the array flattening problem (same techniques involved)
 - ![#FF7C63](https://placehold.it/10/FF7C63/000000?text=+) [rectangles](rectangles) ([_.py solution_](rectangles/rectangles.py)): interesting algorithmic problem (if you have a simpler solution I'm interested)
 - ![#FF7C63](https://placehold.it/10/FF7C63/000000?text=+) [POV](pov) ([_.py solution_](pov/pov.py)): Rotating a tree around a given node (POV is a warming up exercise for [zipper](zipper)).
 - ![#000000](https://placehold.it/10/000000/000000?text=+) [**zipper**](zipper#zipper) ([_.py solution_](zipper/clean_zipper.py)): A programming concept I had never heard of, this is interesting to understand (tackle immutability and performances)
 - ![#000000](https://placehold.it/10/E8C14E/000000?text=+) [**nth prime**](nth-prime#computing-the-nth-prime) ([_.py solution_](nth-prime/nth_prime.py)): Memoization and algorithmic optimization
