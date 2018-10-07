# 重来

## 问什么要重写文法？

因为之前的文法比较不友好，首先为了优雅和准确，那个文法采用递归的形式，

并且递归的层数较多，造成了模拟文法时，不得不花费大力气去用数据结构来进行回溯， 

在层数深的情况下，这对于语法分析和语义分析造成了很大的困难，并且递归造成的回溯解决问题时，

容易使得语法和语义分析不易分开，建树拆开会进行两次递归模拟，很麻烦，不拆开,其中的数据结构又

难以维护，debug时会花费大量时间对于递归过程分析。

## 重写文法(参考给的文件和网络little c文法)

> 目的：降低递归层数，拆分语句(便于分析，特别是语义分析)

> 句子

Sentence -->Statement | Assignment | Control | Expression | Constant | FunctionStatement | FunctionCall 

> 声明语句

Statement --> Type ID; | Type ID[ Constant ]; | Type ID[ Constant ] = { ConstantList };
Type --> int | float 
ConstantList --> ∑ | Constant ConstantRest
ConstantRest --> ∑ | ,Constant | ConstantRest
ConstantRest --> (,Constant)*

> 赋值语句

Assignment --> ID = Expression;

> 控制语句

Control --> IfControl | WhileControl 
IfElseControl --> IfControl ElseControl
IfControl --> if( Expression ){ Sentence }
ElseControl --> ∑ | else{ Sentence } 
WhileControl --> while( Expression ){ Sentence }

> 表达式

Expression --> ( Expression ) | Expression Operator Expression | SingleOperator Expression | ArrayIndex | Constant
SingleOperator --> ! | ++ | --
Operate --> + | - | * | / | ++ | -- | > | < | >= | <= | &

> 常量

Constant --> Num | String
Num --> [0-9] | [1-9][0-9]+    
String --> [a-zA-Z0-9\n%:,.]+  

> 函数声明、调用

FunctionStatement --> Type FunctionName( StateParameterList ){ Sentence }
StateParameterList --> ∑ | Parameter ParameterRest
Parameter --> Type ID
ParameterRest --> ∑ | ,Parameter | ParameterRest
Type --> int | float | char | double

FunctionCall --> ID( CallParameterList );
CallParameterList --> ∑ | ID ParameterRest
ParameterRest --> ∑ | ,ID | ParameterRest

> return语句

Return --> return Expresstion;
