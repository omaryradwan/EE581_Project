# This file defines the TypedVariable Class. This class is the parent classof type classes.
#
# One TypedVariable should have the following attributes:
#       initVal         --  The initial value from user                     eg: 0.4, 3, 5
#       tmpVal          --  The temporary value of variable                 eg: 0.4, 3, 5
#       initType        --  The type of the variable from user              eg: bool, float, int
#       initBounds      --  The bounds of the variable from user            eg: [[1,3]], [[1,3],[4,7]]
#       initDepenBounds --  The dependent bounds of the variable from user  eg: [[-a, a^2], [a, a+1]]
#       initIterator    --  The iterator parameter of this variable         eg: t, T
#       initStepSize    --  The default step size of iterator               eg: 0.01
#       initItBound     --  The bound of iterator parameter                 eg: [0, 100]
#       initItFunc      --  The function of step size, default 0.01x        eg: x^2+2x
#       discVal         --  The discrete value of variable                  eg: 1, 2, [1,3,5]
#
#
#  One TypedVariable should have the following functions:
#       transformIntoDiscrete()         --          Transform a given value into the discrete field, return the discrete value

class TypedVariable:
    def __init__(self, initVal, initType, initBounds, initDepenBounds, initIterator, initStepSize, initItBound, initItFunc):
        self.tmpVal = initVal
        self.initType = initType
        self.initBounds = initBounds
        self.initDepenBounds = initDepenBounds
        self.initIterator = initIterator
        self.initStepSize = initStepSize
        self.initItBound = initItBound
        self.initItFunc = initItFunc

    def transformIntoDiscrete(self):
        pass

    def transformBack(self):
        pass


class Bool(TypedVariable):
    def __init__(self, initVal, initType, initBounds, initDepenBounds, initIterator, initStepSize, initItBound, initItFunc):
        super().__init__(initVal, initType, initBounds, initDepenBounds, initIterator, initStepSize, initItBound, initItFunc)

    def transformIntoDiscrete(tmpVal):
        discrete = 0
        if tmpVal:
            discVal = 1
        return discVal
    
    def transformBack(discVal):
        tmpVal = false
        if discVal == 1:
            tmpVal = true
        return tmpVal
    
    def updatediscVal(self, discVal):
        self.discVal = discVal

    def updatetmpVal(self, tmpVal):
        self.tmpVal = tmpVal


class Float(TypedVariable):
    def __init__(self, initVal, initType, initBounds, initDepenBounds, initIterator, initStepSize, initItBound, initItFunc):
        super().__init__(initVal, initType, initBounds, initDepenBounds, initIterator, initStepSize, initItBound, initItFunc)

    def transformIntoDiscrete(tmpVal):
        #TBD
    
    def transformBack(discVal):
        #TBD

class Int(TypedVariable):
    def __init__(self, initVal, initType, initBounds, initDepenBounds, initIterator, initStepSize, initItBound, initItFunc):
        super().__init__(initVal, initType, initBounds, initDepenBounds, initIterator, initStepSize, initItBound, initItFunc)
    
    def transformIntoDiscrete(tmpVal):
        return tmpVal
    
    def transformBack(discVal):
        return discVal