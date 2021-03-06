import math
import matplotlib.pyplot as plt
import time 
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


def plot_graphs(velocities,range_currs,pathangles,time,control_input,heights):
    plt.plot(time,control_input)
    plt.ylabel('control_input')
    plt.xlabel('time')
    plt.savefig('controlVsTime.jpg')
    plt.close()

    plt.plot(time,velocities)
    plt.ylabel('velocity')
    plt.xlabel('time')
    plt.savefig('velocityVsTime.jpg')
    plt.close()

    plt.plot(time,pathangles)
    plt.ylabel('path angle')
    plt.xlabel('time')
    plt.savefig('Path_angleVsTime.jpg')
    plt.close()


    plt.plot(range_currs,heights)
    plt.ylabel('Altitude')
    plt.xlabel('Range')
    plt.savefig('altitudeVsrange.jpg')
    plt.close()


def simulate(velocities,range_currs,pathangles,time,control_input,heights):

    plt.subplot(2,2,1)
    plt.plot(time,control_input)
    plt.ylabel('control_input')
    plt.xlabel('time')
    # plt.savefig('controlVsTime.jpg')
    # plt.close()

    plt.subplot(2,2,2)    
    plt.plot(time,velocities)
    plt.ylabel('velocity')
    plt.xlabel('time')
    # plt.savefig('velocityVsTime.jpg')
    # plt.close()

    plt.subplot(2,2,3)
    plt.plot(time,pathangles)
    plt.ylabel('path angle')
    plt.xlabel('time')
    # plt.savefig('Path_angleVsTime.jpg')
    # plt.close()

    plt.subplot(2,2,4)
    plt.plot(range_currs,heights)
    plt.ylabel('Altitude')
    plt.xlabel('Range')
    # plt.savefig('altitudeVsrange.jpg')
    # plt.close()

    plt.show(block=False)
    plt.pause(1)
    plt.close()


def obtainIncrements(velocity,pathangle,height,range_curr,load):
    drange=velocity*math.cos(pathangle)
    dheight=velocity*math.sin(pathangle)
    dpathangle=g*(load-math.cos(pathangle))/velocity

    density=1.225*math.exp(-beta*height)
    zeroLiftDrag=density*velocity*velocity*surfaceArea*zeroLiftDragCoeff/2
    liftInducedDrag=2*(mass*g)*(mass*g)*liftInducedDragCoeff/(density*velocity*velocity*surfaceArea)

    dvelocity=-(zeroLiftDrag+liftInducedDrag*load*load)/mass - g*math.sin(pathangle)
    
    load=density*velocity*velocity*surfaceArea*math.sqrt(zeroLiftDragCoeff/liftInducedDragCoeff)/(2*mass*g)

    return drange,dheight,dpathangle,dvelocity,load



def solve_by_euler(incrementTime):
    intialLift,height,velocity,pathangle,density,loadMax=initialize() 
    
    #Checking for LoadMax quantity
    load=loadMax

    flighttime=0
    range_curr=0
    t=0

    velocities=[]
    range_currs=[]
    heights=[]
    pathangles=[]
    time=[]
    control_input=[]

 
    call=0


    while height>=0:
        flighttime=flighttime+incrementTime
        drange,dheight,dpathangle,dvelocity,load=obtainIncrements(velocity,pathangle,height,range_curr,load)
        
        velocities.append(velocity)
        range_currs.append(range_curr)
        pathangles.append(pathangle)
        time.append(flighttime)
        control_input.append(load)
        heights.append(height)

        #updating the increments for each iteration
        range_curr=range_curr+drange*incrementTime
        height=height+dheight*incrementTime
        velocity=velocity+dvelocity*incrementTime
        pathangle=pathangle+dpathangle*incrementTime

        print(flighttime," ",range_curr," ",pathangle," ",height," ",velocity," ",density," ",load)

        # Uncomment for simulations.

        # if call%100==0:
        #     simulate(velocities,range_currs,pathangles,time,control_input,heights)
        # call=call+1


    return velocities,range_currs,heights,pathangles,time,control_input





def solve_by_RK4th(incrementTime):

    intialLift,height,velocity,pathangle,density,loadMax=initialize()
    
    #Checking for LoadMax quantity
    load=loadMax

    flighttime=0
    range_curr=0
    t=0

    velocities=[]
    range_currs=[]
    heights=[]
    pathangles=[]
    time=[]
    control_input=[]

    call=0


    while height>=0:
        flighttime=flighttime+incrementTime

        drange1,dheight1,dpathangle1,dvelocity1,load1=obtainIncrements(velocity,pathangle,height,range_curr,load)
        drange2,dheight2,dpathangle2,dvelocity2,load2=obtainIncrements(velocity+0.5*dvelocity1,pathangle+0.5*dpathangle1,height+0.5*dheight1,range_curr+0.5*drange1,load1)
        drange3,dheight3,dpathangle3,dvelocity3,load3=obtainIncrements(velocity+0.5*dvelocity2,pathangle+0.5*dpathangle2,height+0.5*dheight2,range_curr+0.5*drange2,load2)
        drange4,dheight4,dpathangle4,dvelocity4,load4=obtainIncrements(velocity+dvelocity3,pathangle+dpathangle3,height+dheight3,range_curr+drange3,load3)

        drange=(drange1+2*drange2+2*drange3+drange4)
        dheight=(dheight1+2*dheight2+2*dheight3+dheight4)
        dvelocity=(dvelocity1+2*dvelocity2+2*dvelocity3+dvelocity4)
        dpathangle=(dpathangle1+2*dpathangle2+2*dpathangle3+dpathangle4)
        load=load4



        velocities.append(velocity)
        range_currs.append(range_curr)
        pathangles.append(pathangle)
        time.append(flighttime)
        control_input.append(load)
        heights.append(height)

        # Uncomment for simulations.

        # if call%100==0:
        #     simulate(velocities,range_currs,pathangles,time,control_input,heights)
        # call=call+1

        #updating the increments for each iteration
        range_curr=range_curr+(1/6)*drange*incrementTime
        height=height+(1/6)*dheight*incrementTime
        velocity=velocity+(1/6)*dvelocity*incrementTime
        pathangle=pathangle+(1/6)*dpathangle*incrementTime

        print(flighttime," ",range_curr," ",pathangle," ",height," ",velocity," ",density," ",load)

    return velocities,range_currs,heights,pathangles,time,control_input
    



if __name__ == "__main__":
    # Defines the time step.

    incrementTime=0.1
    
    # To run simulations for Euler method.
    velocities,range_currs,heights,pathangles,time,control_input= solve_by_euler(incrementTime)
    # To run simulations for RK method.
    velocities,range_currs,heights,pathangles,time,control_input=solve_by_RK4th(incrementTime)

    plot_graphs(velocities,range_currs,pathangles,time,control_input,heights)
            
