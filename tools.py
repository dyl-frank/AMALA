import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Applies Gaussian distribution to weight map
def gaussian(x, mean, std_dev):
    return 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / std_dev)**2)

def map_weights(compilation, space):
    positions_and_values = []
    for i, x in enumerate(space.x_coords):
       for j, y in enumerate(space.y_coords):
            for k, z in enumerate(space.z_coords):
                positions_and_values.append((x, y, z, compilation[i, j, k]))
    return positions_and_values

'''Accepts detector count, detector object, enviroment object. Draws predicted radius on a numpy array'''
def trace_omega(count, detector, env):
    # Apply inverse square estimate
    r = detector.solve_r(count)

    error = detector.rmse
    arry = np.copy(env.zeros_array)

    # Create 3D coordinate grids using meshgrid
    X, Y, Z = np.meshgrid(env.x_coords, env.y_coords, env.z_coords, indexing='ij')

    # Calculate the distance for each point in the environment to the detector
    distances = np.sqrt((X - detector.pos[0])**2 + (Y - detector.pos[1])**2 + (Z - detector.pos[2])**2)

    # Set elements in arry to 1 where the distance is within the specified range
    for i, x in enumerate(env.x_coords):
        for j, y in enumerate(env.y_coords):
            for k, z in enumerate(env.z_coords):
                s = np.sqrt((x - detector.pos[0])**2 + (y - detector.pos[1])**2 + (z - detector.pos[2])**2)
                if (r - error) <= s <= (r + error):
                    weight = gaussian(s, mean = r, std_dev = error)
                    arry[i, j, k] = weight
    return arry


'''Plots a weight map using matplotlib'''
def plot_weights(weight_map, min_weight=0):
    
    refined_map = [el for el in weight_map if el[3] > min_weight]

    x_vals = [el[0] for el in refined_map]
    y_vals = [el[1] for el in refined_map]
    z_vals = [el[2] for el in refined_map]
    w_vals = [el[3] for el in refined_map]

    # Set the background color to black
    plt.rcParams['axes.facecolor'] = 'grey'
    
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    p = ax.scatter(x_vals, y_vals, z_vals, c=w_vals, s=0.15, cmap="viridis", marker='o', label="weights")
    ax.scatter(218.6, -26.93, 59.42, c="red", s=100, marker='o', label="actual")
    ax.scatter(227.81663551401869, -16.956521739130434, 49.56521739130434, c="black", s=100, marker='o', label="predicted")
    
    cbar = plt.colorbar(p)
    cbar.set_label('Weight')

    ax.set_title("Weights")
    
    # Set the text color to white
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.zaxis.label.set_color('black')
    ax.title.set_color('black')
    
    # Set the ticks color to white
    ax.tick_params(axis='x', colors='b')
    ax.tick_params(axis='y', colors='b')
    ax.tick_params(axis='z', colors='b')

    # Show the plot
    plt.legend()
    plt.show()

