### Let Expressions and Assignment Operator  
cook is used as a let expression, and the "=" operator is used as an assignment operator.  

```cook <datatype> <variable name> = <value>;``` 
#### for example:  
``` shell
 cook num n=25;
```
### List of basic datatypes supported in ACE language  
* integer  
* char
* boolean

In ACE, the user can declare and initialise variables of the above datatypes in separate steps or combine both processes into a single statement.  

### Integer datatype  
The ```num``` keyword is used to declare an integer. 

#### for example:  
```shell
cook num n1;
n1=23;
cook num n2=25;
```
### Char datatype  
The ```char``` keyword is used to declare a char.   

#### for example:  
```shell
cook char c1;
c1='a';
cook char c2='b';
```

### boolean datatype  
The ```flag``` keyword is used to declare a bool. 

#### for example:  
```shell
cook flag b1;
b1=true;
cook char b2=false;
```

### Syntax for binary operations   

* (+) - Addition
* (-) - Subtraction
* (*) - Multiplication
* (/) - Division
* (#) - Power
* (&) -BITWISE AND
* ( | ) - BITWISE OR
* (&&) - AND
* ( || ) -  OR
* (^)- XOR
* (%) - MODULO  

### Syntax for unary operations  
* (++) - ADDING ONE
* (--) -  DECREMENTING ONE
* (!) - NOT
* (~) - BITWISE NOT  

###syntax for strings 

```cook str <string name>= “some_string”;```

For strings, users can declare and initialise variables in separate steps or combine both processes into a single statement.  

#### for example:  
```shell
cook str s1;
s1="abc";
cook str s2="def";
```




