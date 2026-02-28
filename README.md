# Hackathon_26
# Heat Sink Simpulation
Problem:
Analyzing temperature distributions of heat sinks fins with complex geometry is extremely difficult

Solve:
Users draw a heat sink shape that is assumed to be mirrored across the x-axis. The program then calculates the temperature distribution using finite difference method. The distribution is shown to the user using a color gradiant to represent the temperature.

# How to use
- Run main.py
- A window will open where you are asked for the x and y dimensions
- A grid will pop up with changable parameters:
    - there is a dropdown of materials you can choose. 
    - If you decide to use a different material than what the options are, you will need to input the ______
    - The temperature ambient temperature of the fluid can be changed (free stream temperature)
    - The temperature of the heat source can be changed



# How the math works:
The user first inputs the materials of the heat sink and surrounding convective fluid then draws their desired geometry. 
The program then splits the geometry into several finite elements. Using the principles of heat transfer equations for the temperature at each node are constructed. Using the sympy and numpy packages the equation at each node are turned into a matrix-vector equation and the temperature distribution is solved for.













# Project setup:
