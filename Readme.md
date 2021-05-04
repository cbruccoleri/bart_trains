# BART Task

Your task is to write a program in Python 3 that queries the API and prints out the number of
minutes until the upcoming departing from the El Cerrito Plaza station in the southern direction.

So, your program output should look like this:
> python departures.py
[1, 11, 21]

## Requirements

The program must meet the following requirements:

- it must run correctly with no modifications in any Python 3 environment;

- it must output the answer on a single line as an array of numbers (not strings);

- it must handle the case where the BART API returns a value that is not a number (hint: this is the case if the number of minutes is 0);
- it must handle the case when the trains aren't running at all (BART opens 5 AM PDT and closes at 9 PM PDT) - in this case it should print out an empty array, but not error out;

- it must fail gracefully if the API service is unavailable.

- the code should be readable.
