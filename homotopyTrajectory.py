import math
# Initialize all the constant parameters that need not be changed throughout the program

g=9.8
zeroLiftDragCoeff=0.055 # Denoted bt CD0
mass=600
surfaceArea=1.028
liftInducedDragCoeff=0.08 #denoted by K
beta=0.000138888888888


#The main parameters that change and the components that store this increase
# range_curr=0
# height=0
# velocity=0
# pathangle=0
# density=0
# drange=0
# dheight=0
# dvelocity=0
# dpathangle=0
# flighttime=0


#The load component and the max load component which shall be calculated from the equation given be below
# load=0
# loadMax=0 #referred to as n in the paper


#Other lot of unrequired vaariables kept for future use
# DragInduced=0
# LiftInduced=0
# intialLift=0
# zeroLiftDrag=0
# liftInducedDrag=0
# angleOfAttack=0



def initialize():
    
    intialLift=0
    height=10000
    velocity=250
    pathangle=-0.1 #radians
    density=1.225*math.exp(-beta*height)
    loadMax=density*velocity*velocity*surfaceArea*math.sqrt(zeroLiftDragCoeff/liftInducedDragCoeff)/(2*mass*g)

    return intialLift,height,velocity,pathangle,density,loadMax



def obtainIncrements(velocity,pathangle,height,range_curr):
    drange=velocity*math.cos(pathangle)
    dheight=velocity*math.sin(pathangle)

    density=1.225*math.exp(-beta*height)
    zeroLiftDrag=density*velocity*velocity*surfaceArea*zeroLiftDragCoeff/2
    liftInducedDrag=2*(mass*g)*(mass*g)*liftInducedDragCoeff/(density*velocity*velocity*surfaceArea)

    load=density*velocity*velocity*surfaceArea*math.sqrt(zeroLiftDragCoeff/liftInducedDragCoeff)/(2*mass*g)
    dpathangle=g*(load-math.cos(pathangle))/velocity
    dvelocity=-(zeroLiftDrag+liftInducedDrag*load*load)/mass - g*math.sin(pathangle)

    return drange,dheight,dpathangle,dvelocity


if __name__ == "__main__":

    #Setting up variables
    intialLift,height,velocity,pathangle,density,loadMax=initialize() 
    incrementTime=1
    
    #Checking for LoadMax quantity
    load=loadMax

    flighttime=1
    range_curr=0

    while height>=0:
        flighttime=flighttime+incrementTime
        drange,dheight,dpathangle,dvelocity=obtainIncrements(velocity,pathangle,height,range_curr)
        
        #updating the increments for each iteration
        range_curr=range_curr+drange*incrementTime
        height=height+dheight*incrementTime
        velocity=velocity+dvelocity*incrementTime
        pathangle=pathangle+dpathangle*incrementTime

        print(flighttime," ",range_curr," ",pathangle," ",height," ",velocity," ",density," ",load)
        flighttime=flighttime+1
