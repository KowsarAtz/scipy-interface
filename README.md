# scipy-interface

Of course you need scipy package and its dependencies installed on your system or on your virtualenv for this! :)

How to use it? Easy! Just follow the below example:

1. You will define your problem target function with MIN or MAX keywords as well as your problem constraints all in a file with the proper format like the following example:
```
MAX 1000*x_1+1900*x_2+2700*x_3+3400*x_4
0.18*x_1+0.28*x_2+0.4*x_3+0.5*x_4-0.2125*x_5<=0
x_5<=300
-0.8*x_1+0.2*x_2+0.2*x_3+0.2*x_4<=0
0.1*x_1-0.9*x_2+0.1*x_3+0.1*x_4<=0
0.25*x_1+0.25*x_2-0.75*x_3-0.75*x_4<=0
50*x_1+70*x_2+130*x_3+160*x_4+2*x_5<=15000
x_1>=0
x_2>=0
x_3>=0
x_4>=0
x_5>=0
```
2. Then you run the "main.py" script with your input-file path as argument for calculating and viewing the results:
```
$python main.py ./in.txt

{'max_value': 343965.2,
 'success_status': True,
 'variable_values': {'x_1': 35.8,
                     'x_2': 98.5,
                     'x_3': 44.8,
                     'x_4': 0.0,
                     'x_5': 244.5}}
```

## Considerations:
1. Instead of x_1/3 write this: x_1 * (1/3)
2. ...