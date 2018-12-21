function sys = process(t,x,flag,u,p)


    %drange=velocity*cos(pathangle);
    %dheight=velocity*sin(pathangle);
    %dpathangle=g*(load-cos(pathangle))/velocity;

    %density=1.225*exp(-beta*height);
    %zeroLiftDrag=density*velocity*velocity*surfaceArea*zeroLiftDragCoeff/2;
    %liftInducedDrag=2*(mass*g)*(mass*g)*liftInducedDragCoeff/(density*velocity*velocity*surfaceArea);

    %dvelocity=-(zeroLiftDrag+liftInducedDrag*load*load)/mass - g*sin(pathangle);

    %load=density*velocity*velocity*surfaceArea*sqrt(zeroLiftDragCoeff/liftInducedDragCoeff)/(2*mass*g);
  

  
  switch flag,
    case 0 % f(x,u,p,t)
        sys = [x(2);
        - x(3)*u+16*t-8;
        u;
        x(1)^2+x(2)^2+0.0005*(x(2)+16*t-8-0.1*x(3)*u^2)^2];
    case 1 % df/dx
        sys = [0 0 0 2*x(1);
        1 0 0 (2*x(2)+2*0.0005*(x(2)+16*t-8-0.1*x(3)*u^2));
        0 -u 0 2*0.0005*(x(2)+16*t-8-0.1*x(3)*u^2)*(-0.1*u^2);
        0 0 0 0];
    case 2 % df/du
        sys = [0 -x(3) 1 (2*0.0005*(x(2)+16*t-8-0.1*x(3)*u^2)*(-2*0.1*x(3)*u))];
    case 3 % df/dp
        sys = [];
    case 4 % df/dt
        sys = [0 16 0 2*0.0005*(x(2)+16*t-8-0.1*x(3)*u^2)*16];
    case 5 % x0
        sys = [0;-1;-sqrt(5);0];
    case 6 % dx0/dp
        sys = [];
    case 7 % M
        sys = [];
    case 8 % unused flag
        sys = [];
    otherwise
        error([’unhandled flag = ’,num2str(flag)]);
end
