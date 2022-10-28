# This file defines the TypedVariable Class. This class is the parent classof type classes.
#
# One TypedVariable should have the following attributes:
#       initVal         --  The initial value from user                     eg: 0.4, 3, 5
#       tmpVal          --  The temporary value of variable                 eg: 0.4, 3, 5
#       initType        --  The type of the variable from user              eg: bool, float, int
#       initBounds      --  The bounds of the variable from user            eg: [[1,3]], [[1,3],[4,7]]
#       initDepenBounds --  The dependent bounds of the variable from user  eg: [[-a, a^2], [a, a+1]]
#       discVal         --  The discrete value of variable                  eg: 1, 2, [1,3,5]
#
#
#  One TypedVariable should have the following functions:
#       transformIntoDiscrete()         --          Transform a given value into the discrete field, return the discrete value
#       transformBack()                 --          Transform a given discrete value into tyoed field, return the typed value
#       updatediscVal()                 --          Update discrete value by given value
#       updatetmpVal()                  --          Update tmporary value by given value

class TypedVariable:
    def __init__(self, initVal, initType, initBounds, initDepenBounds):
        self.tmpVal = initVal
        self.initType = initType
        self.initBounds = initBounds
        self.initDepenBounds = initDepenBounds


    def transformIntoDiscrete(self):
        pass

    def transformBack(self):
        pass
    
    def updatediscVal(self, discVal):
        self.discVal = discVal

    def updatetmpVal(self, tmpVal):
        self.tmpVal = tmpVal


class Bool(TypedVariable):
    def __init__(self, initVal, initType, initBounds, initDepenBounds):
        super().__init__(initVal, initType, initBounds, initDepenBounds)

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
        super().updatediscVal(discVal)

    def updatetmpVal(self, tmpVal):
        super().updatetmpVal(tmpVal)



class Float(TypedVariable):
    def __init__(self, initVal, initType, initBounds, initDepenBounds):
        super().__init__(initVal, initType, initBounds, initDepenBounds)

    def transformIntoDiscrete(tmpVal):
        #TBD
    
    def transformBack(discVal):
        #TBD

    def updatediscVal(self, discVal):
        super().updatediscVal(discVal)

    def updatetmpVal(self, tmpVal):
        super().updatetmpVal(tmpVal)

class Int(TypedVariable):
    def __init__(self, initVal, initType, initBounds, initDepenBounds):
        super().__init__(initVal, initType, initBounds, initDepenBounds)
    
    def transformIntoDiscrete(tmpVal):
        return tmpVal
    
    def transformBack(discVal):
        return discVal
    
    def updatediscVal(self, discVal):
        super().updatediscVal(discVal)

    def updatetmpVal(self, tmpVal):
        super().updatetmpVal(tmpVal)