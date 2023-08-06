# naveeeen Package

This is a simple package, you can see the difference when using naveeeen and without.

> ***It's 4 e's.***

This saves your time when dealing with many files.

* What happen if you don't use naveeeen, see the difference

  pass your method name(without())), iterable, false to e()

  *syntax: naveeeen.e(func_name,list,False)*
* What happen if you use naveeeen, see the difference

  pass your method name, iterable, True to e()

  *syntax: naveeeen.e(func_name,list,True)*

  Always the third argument is True.
* See the difference in result of using 'both' - output will the time taken to run a normal program and time taken to run  a normal program with naveeeen.
  syntax: *naveeeen.e(func_name,list,'both')* or *naveeeen.e(func_name,list,whizz='both')*

Try running the below code to see the difference:

*import naveeeen*

*import os*

*import time*

*def main_fun(s=[]):*

 *with open(f'{s}.txt','w+') as f:*

 *time.sleep()*

 *if os.path.exists(f'{s}.txt'):*

 *os.remove(f'{s}.txt')*

 *print(s, end=',')*

*nums=[i for i in range(1000)] #try with 10000 100000*

*#if"____main____"==__name__:*

*print(naveeeen.e(main_fun,nums,whizz='both'))*
