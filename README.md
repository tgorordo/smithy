# Smithy
*A simple smith set solver for ranked-choice ballots.* 

The Smith set is the minimal set of candidates which can beat all others pairwise - if there is a single winner
in the set they are guaranteed the standard Condorcet i.e. Majority winner (they beat all others pairwise).


## TODO

- add cli options & flexibility
  - relevant column selection flags
  - eligible voter filter flags (row selection)
  - output control flags (whether to show input ballots or the voter ids on them, whether to pretty print output, etc.)
- `cgi` [interface on pages.uoregon.edu](https://service.uoregon.edu/TDClient/2030/Portal/KB/Article/43069/Advanced-use-of-pages-uoregon-edu).
- instructions/writeup and README
- polish/finalize packaging and usage (might be some refactoring of where the cli goes)
