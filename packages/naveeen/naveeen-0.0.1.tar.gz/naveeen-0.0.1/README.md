# naveeen Package

This is a simple package, you can see the difference when using naveeen/threeeading and without.

> ***It's 3 e's.***

This saves your time mainly dealing with files.


1. [ ] What happen if you don't use naveeen/threeeading, seee the difference

    pass your method name(without())), iterable, false to e()

    *syntax: naveeen.e(func_name,list,False)*

1. [ ] What happen if you use naveeen/threeeading, seee the difference

    pass your method name, iterable, True to e()

    *syntax: naveeen.e(func_name,list,True)*

    Always the third argument is True.

* [ ] See the difference in result of using 'both' - output will the time taken to run a normal program and time taken to run  a normal program with naveeen/threeeading.
  syntax: *naveeen.e(func_name,list,'both')* or *naveeen.e(func_name,list,whizz='both')*

Try running the below code to see the difference:


*import naveeen*

*import os*

*import time*

*def main_fun(s=[]):*

 *with open(f'{s}.txt','w+') as f:*

 *time.sleep()*

 *if os.path.exists(f'{s}.txt'):*

 *os.remove(f'{s}.txt')*

 *print(s, end=',')*

*nums=[i for i in range(100000)]*

*#if"____main____"==__name__:*

*print(naveeen.e(main_fun,nums,whizz='both'))*
