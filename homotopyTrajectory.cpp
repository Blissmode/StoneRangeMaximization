#include <bits/stdc++.h>
using namespace std;

#define fastio ios_base::sync_with_stdio(0);cin.tie(NULL);cout.tie(NULL)


// Initialize all the constant parameters that need not be changed throughout the program

const double g=9.8;
const double zeroLiftDragCoeff=0.055; // Denoted bt CD0
const double mass=600;
const double surfaceArea=1.028;
const double liftInducedDragCoeff=0.08; //denoted by K
const double beta=0.000138888888888;


//The main parameters that change and the components that store this increase
double range,height,velocity, pathangle,density;
double drange,dheight,dvelocity, dpathangle;
double flighttime=0;


//The load component and the max load component which shall be calculated from the equation given be below
double load,loadMax; //referred to as n in the paper


//Other lot of unrequired vaariables kept for future use
double DragInduced,LiftInduced,intialLift;
double zeroLiftDrag,liftInducedDrag;
double angleOfAttack;


void initialize();
void obtainIncrements();

int main()
{
    fastio;  //Removing the sync from stdio, check the define for more info

    //Setting up variables
    initialize(); 
    cout<<density<<" "<<loadMax<<endl;
    
    //Checking for LoadMax quantity
    load=loadMax;

    cout<<"[";
    while(height>=0)
    {
        flighttime++;
        obtainIncrements();
        
        //updating the increments for each iteration
        range+=drange;
        height+=dheight;
        velocity+=dvelocity;
        pathangle+=dpathangle;

        // cout<<"Time:"<<flighttime<<"||"<<"Range:"<<range<<"||"<<"Path Angle:"<<pathangle<<"||"<<"Height:"<<height<<"||"<<"Velocity:"<<velocity<<"||"<<"Density:"<<density<<"||load:"<<load<<endl;
        // cout<<height<<",";
    }
    cout<<"]";
}




void initialize()
{
    intialLift=0;

    height=10000;
    velocity=250;
    pathangle=-0.1; //radians
    density=1.225*exp(-beta*height);
    loadMax=density*velocity*velocity*surfaceArea*sqrt(zeroLiftDragCoeff/liftInducedDragCoeff)/(2*mass*g);
}



void obtainIncrements()
{
    drange=velocity*cos(pathangle);
    dheight=velocity*sin(pathangle);
    dpathangle=g*(load-cos(pathangle))/velocity;

    density=1.225*exp(-beta*height);
    zeroLiftDrag=density*velocity*velocity*surfaceArea*zeroLiftDragCoeff/2;
    liftInducedDrag=2*(mass*g)*(mass*g)*liftInducedDragCoeff/(density*velocity*velocity*surfaceArea);

    dvelocity=-(zeroLiftDrag+liftInducedDrag*load*load)/mass - g*sin(pathangle);

    load=density*velocity*velocity*surfaceArea*sqrt(zeroLiftDragCoeff/liftInducedDragCoeff)/(2*mass*g);

    if(dheight>0)
        dheight*=-1;
    if(drange<0)
        drange*=-1;
}