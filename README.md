# Hackathon_26
# Heat Sink Simulation
Problem:
Analyzing temperature distributions of heat sinks fins with complex geometry is extremely difficult

Solve:
Users draw a heat sink shape that is assumed to be mirrored across the x-axis. The program then calculates the temperature distribution using finite difference method. The distribution is shown to the user using a color gradiant to represent the temperature.

# How to use
- Run main.py
- A window will open where you are asked for the x and y dimensions
- A grid will pop up with changeable parameters:
    - there is a dropdown of heat sink materials you can choose. 
    - If you decide to use a different heat sink material than what the options are, you will need to input the conductive heat transfer coefficient
    - there is a dropdown of surrounding fluid materials you can choose. 
    - If you decide to use a different fluid material than what the options are, you will need to input the convective heat transfer coefficient
    - The ambient temperature of the fluid can be changed (free stream temperature)
    - The temperature of the heat source can be changed
    - In the grid you can draw your desired geometry. It is assumed the real heat sink is symmetric across the x-axis.
- Once parameters are set, click "Run Physics" and the program will calculate and show the temperature distribution.
- Change parameters and click "Run Physics" again to use the same geometry.
- Click "clear" to reset geometry


# How the math works:
The user first inputs the materials of the heat sink and surrounding convective fluid then draws their desired geometry. 
The program then splits the geometry into several finite elements. Using the principles of heat transfer equations for the temperature at each node are constructed. Using the sympy and numpy packages the equation at each node are turned into a matrix-vector equation and the temperature distribution is solved for.













# Project setup:
