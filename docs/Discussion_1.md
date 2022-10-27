1 map into discrete domain

2 math

3 map back into discrete domain
projection to original space

What’s the input?
initial condition:
# of parameters,
type of parameters,
initial bounds of each parameter,
dependent bounds:
-a <= b <= a^2
-a <= b <= a^2/(e^a+2a)
cost function -- non-linear:
f(a,b,...)
iterating parameter:
bound, step size, iterating function(step size as a function of iterating parameter)
Ex: t [0, 100], 0.1, step size = 0.1
Ex: t [0, 100], 0.1, step size = f(t)

What’s the output?
A trace of all locally optimal points

Algorithm to find neighboring points
Simulated annealing
Particle swarm optimization
Genetic Algorithm

Find the most optimal algorithm

Questions:
1 How to convert dependent bounds into discrete space
calculate bounds -> convert as float/bool/int
2 How to convert different type of parameters into discrete space
int
  float  --  number of significance figure, the power 
  0.0564 -> {564, -4}  
  bool  --  0/1


Backlog:
weather in {sunny, cloudy, raining, snowing} enumerate

1 Class object 
2 JSON -> Parser
3 Class Interpret -> Math 
4 Environment
  4A Algorithms
  4B Cost Function
5 Computation of Best Case
6 Trace Dump

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

class Bool:
  bounds: ...
  init_val: ....
  transformation = ...

Bool1.bounds = {upper: B2.val, lower: B3.val}


Presentation:
5 slides, 10 min
1 problem statement
2 implementation, how far
3 TBD
4 TBD
5 still need to do, hope to do
