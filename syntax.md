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
cook flag b2=false;
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

* ```(&&)``` and ```(||)``` are Short-circuiting (lazy) boolean operators

### Syntax for unary operations  
* (++) - ADDING ONE
* (--) -  DECREMENTING ONE
* (!) - NOT
* (~) - BITWISE NOT  

### syntax for strings 

```cook str <string name>= “some_string”;```

For strings, users can declare and initialise variables in separate steps or combine both processes into a single statement.  

#### for example:  
```shell
cook str s1;
s1="abc";
cook str s2="def";
```

### Syntax for Arrays 
* Arrays are used to store elements 
* They cannot have different datatype elements
* Declaration of Array:  ```cook < datatype > < arrayname >[length of array];```
* Declaration + Initialization :```cook < datatype > < arrayname > = {values comma separated };```  

```shell
cook num arr1[5];
cook num arr2={ 1 , 2 , 3 , 4 , 5};
```  
* To calculate length: ```len(< arrayname >)```
* For head: ```headof(< arrayname >)```  
* For tail: ```tailof(< arrayname >)```  
* For Cons: ```< array name > = < element > :: < array name >```  
* For accessing  element at ith index : ```< arrayname >[i]```
* For modifying element at ith index : ```< arrayname >[i]=< some value >;```  

```shell
cook num length=len(arr);
cook num head=headof(arr);
cook num tail=tailof(arr);
cook num new_arr= 6 :: arr1;
cook num second_element=arr1[2];
arr1[2]=7;
```


### Syntax for Tuples
* Tuples are used to store elements, also the elements can have different datatypes
* The tuple remains immutable
* The tuple will contain basic datatyples like integers and strings and won't support nested components like lists, tuples, etc .  
* Declaration + Initialization :```cook < tuple name > = (values comma separated);```  

```shell
cook tup=( 1 , "A" , 3 , "C" , 5 );
```  
* To calculate length: ```len(< tuple name >)```
* For head: ```headof(< tuple name >)```  
* For tail: ```tailof(< tuple name >)```   
* For accessing  element at ith index : ```< tuple name >[i]```
* 
```shell
cook num length=len(tup);
cook num head=headof(tup);
cook num tail=tailof(tup);
cook num second_element=tup[2];
```

### Syntax for List 
* List are used to store elements, also the elements can have different datatypes
* Declaration of List:  ```cook < list name > = [];```
* Declaration + Initialization :```cook < list name > = [values comma separated ];```  

```shell
cook list1=[];
cook list2=[ 1 , "abcd" , 3 , 4 , 5];
```  
* To calculate length: ```len(< list name >)```
* For head: ```headof(< list name >)```  
* For tail: ```tailof(< list name >)```  
* For accessing  element at ith index : ```< list name >[i]```
* For modifying element at ith index : ```< list name >[i]=< some value >;```  

```shell
cook num length=len(list1);
cook num head=headof(list1);
cook num tail=tailof(list1);
cook num second_element=list1[2];
list1[2]=7;
```

## Syntax to Print 
* Print to the terminal: ```echo( expression to be printed ) ;```
```shell
cook num a=5;
echo(a);
echo(" This prints Hello !");
```  

## Branches and Loops
* ***Branches*** :
* if/else if ( boolean expression or integer ->{false if 0 else true}) {...}
* else {...}
```shell
cook num a=2;
if(a>2){
    echo("The number is greater than 2");
}
else if(a<2>){
    echo("The number is less than 2");
}
else{
    echo("The number is 2");
}
```  

* ***Loops*** :
* floop is used as an iteration statement(similar to for loop).
* ```break``` exits from loops, and ```continue``` exits the current iteration and continues with the next.
* Used as : ```floop(declaration + initialization ; stopping condition ; iteration ){.....}```  

```shell
floop(cook num a=1; a < 5; a++){
    continue;
    echo(a);
}
```  

* wloop is used as an iteration statement(similar to while loop). 
* Used as : ```wloop(stopping condition){.....}```  

```shell
cook num iter=5;
wloop(iter>0){
    echo(iter);
    iter--;
    break;
}
```

## Using Functions 
* The functions are entities used to give an output based on certain inputs( not necessary to always have an input and output).
* The language also supports void return type.
* Defining Functions : ```func <data type/void> <function name> ( parameters with data type comma separated ){...... return something  }```
  ```shell
  func num increment_by_one(num a){
  return a+1;
  }
  
  cook num a=5;
  cook num b=increment_by_one(a);
  echo(b);
  ```





