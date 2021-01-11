Rabbit Hole - Cumulative Cyclomatic Complexity for Ghidra
=========================================================

This script calculates the sum of the cyclomatic complexities of functions reachable from any function. Calculated results are appended to function names as `_cc%d`.

Presenting results
------------------

Recently I've been becoming a believer in storing meta information in names so it is immediately visible when browsing any code representation (partially inspired by [this talk](https://www.youtube.com/watch?v=HyTkqcfSv4w)).

That being said representing this information as comments may be desirable. If you want this feature, please use the [issue tracker](https://github.com/v-p-b/rabbithole/issues/1)!

Results are also presented to the user as a simple table, that can be sorted, filtered and exported. 
