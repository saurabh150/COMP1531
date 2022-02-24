# Software Engineering Principles

## Reflection On Iteration 2
* What was good?
	* Data structure had an API-like interface with many helper functions which reduced need for repetitive code.
	* Design- similar coding style throughout code/
	* Abstracted certain functions like creating an error handler.
	* Most tests had setup for an entire file by using global variables so reduced repetitive setup for every test.
* What was bad?
	* Some code was very fragile and didn't work completely with frontend due to not converting the type passed in from frontend.
	* Bad pylint score for many files.
	* Some repetitive code- redundant checks due to unclear return values in helper functions.
	* Tests had different setup depending on who wrote it.
	* Tests couldn't run together in root tests folder due to using global variables. (They could run individually).

Needless to say, our code had many design smells which we sought to improve in this iteration.

## Key Issues

### rigidity, immobility, opacity, needless repetition
**Issue:** Many of our functions were long and although they made use of helper functions, they had many unecessary error checks due to unclear helper function return values. This was because our very extensive suite of helper functions had some functions which overlapped in functionality. Some of them also raised errors rather than returning boolean (e.g. is_active_token would throw an AccessError rather than return false if the tokenw as inactive). This meant our code was very opaque and only clear to the people who wrote the helper functions themselves.

An example of needless checks and repetition is:
![Repetition in changing name](/imagesForMd/RepeatingMembers.png)
As you can see here there is quite a lot of repetition for changing names. What we did instead was create a function called change_name which would do the above in a much more efficient way. This allowed our functions to have more of a *single responsibility* implementation improve *maintainability* and *understandability*. It became less rigid and less opaque.

Instead, we get:
![Clean refactored change name](/imagesForMd/CleanMembers.png)


Another example of how we refactored our code was going through every function in our helper file and cleaning it up so that there were no redundant checks. This made our code much cleaner and shorter overall.

Trash version:
![Trash Version Repetitive Helper](/imagesForMd/RepetitiveHelper.png)

By cleaning it up, we improved the style as well as made it less rigid and repetitive. This way our code was easier to read and use.

Improved version:
![Cleaner Helper](/imagesForMd/CleanHelper.png)

As you can see, instead of looping through users in every function, we refactored the code so that they used other functions which had similar functionality. Not only this, we improved the style so that it was less messy by writing docstrings.

These are just two examples of how we refactored our code to make it more maintainable. We trawled through all our files to implement this.

### fragility, immobility, needless complexity, coupling
**Issue:** Our server functions would receive data from frontend as strings. This made integration between our backend and frontend hard since we assumed we were given ints or other values. To solve this problem of fragility, we converted all the types in our server.py before passing them into our functions.

Our code also reduced complexity and immobility by creating many helper functions as mentioned. This improved our testability and made the data structure less fragile.

### Design Patterns and Principles
We kept in mind a few of the software principles from the lectures such as DRY (Don't repeat yourself) and KISS (Keep it simple, stupid). This allowed us to go through our code near the end of our iteration (after all the functionality was working with the frontend) and then refactor all our code to fit those principles. We recognise that this was probably not the most efficient way to implement these principles and that they should have been implemented from the very beginning, but since we had already started a certain way, many members were working on the code at once and it was very hard to change how we were coding halway. By going over our code at the end, we cleaned it up so that in the future if we had to maintain it, it would be a lot easier.

# Testing
* Fixed tests from iteration 2 so that they can all be run from the tests root directory with pytest.
* Implemented pytest fixtures to setup tests in each file. This made the code much less repetitive and stopped it from breaking when running all the tests together. We are still using global variables as there are too many variables to be able to pass in to our test functions cleanly with fixtures, but the fixtures clear and setup all variables being used so there are no issues when running all the tests at once.

### Coverage
We worked very hard after we had completed the functions to check that our coverage was 100% for all our functions.
By running the command:
```
pytest --cov-report term-missing --cov=myproj tests/
```
We were able to see which lines of our code were missing coverage. We then went through every file and revised all our tests so that we could get perfect coverage scores.

```
File 												  Stmts	  Miss  Cover
functions/admin.py                                       24      0   100%
functions/auth.py                                        71      0   100%
functions/channel.py                                    119      0   100%
functions/exceptions.py                                   8      0   100%
functions/message_profile.py                            108      0   100%
functions/search.py                                      12      0   100%
functions/standup.py                                     51      0   100%
functions/user_profile.py                                58      0   100%
functions/user_profiles_uploadphoto.py                   21      0   100%
```
However, some things could not be tested in our pytests so we tested them manually against the frontend. For example, it was very difficult to test reset passcode request and check that it would send an email to the user. To test this functionality we simply ran tests using dummy emails and checked them. It was also hard to test that upload photo saved files from the server into a certain directory without actually running the server. To test this we just ran rigorous tests using the frontend.

### Pylint and Code Style
After we had finished all our functions, we ran pylint to make sure that our code had good python style. We then corrected all the errors to make our code more readable and reusable.

 ![Perfect Pylint Score](/imagesForMd/PylintScore.png)

Instead of basic comments before every function, we used docstrings to describe the function in a very clear and concise way. We followed the style of "Do this... Return that", so that it would be very easy to read and understand.

```py
def standup_start(token, channel_id, length):
    """Start standup in a channel. Return time standup finishes."""

def verify_token_in_channel(token, channel_id):
    """Check whether a token is active and in the channel. Return boolean or raise error if inactive."""
```
