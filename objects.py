import numpy as np

'''Initialize detector with base position, length vector, intrinsice efficency,
    - callibration paramaters for a*x + b*x**2 + c*np.exp(x) + d
    - rmse for that callibration cuve
'''
class detector:
    def __init__(self, pos=(0, 0, 0), len = (0,1,0), int_eff = 1, cal = (0, 0, 0, 0), rmse = 0):
        self.pos =  pos
        self.int_eff = int_eff
        self.i_0 = i_0
        self.cal = cal
        self.rmse = rmse
    
    def solve_r(self, x):
        a = self.cal[0]
        b = self.cal[1]
        c = self.cal[2]
        d = self.cal[3]
        return a*x + b*x**2 + c*np.exp(x) + d

'''Defines a 3d enviroment given extents in x,y,z and specified cubic voxel size
NOTE, detectors do not need to be included in the enviroment space.
'''
class Environment:
    def __init__(self, x=(0, 20), y=(0, 20), z=(0, 20), voxelSize=1):
        self.voxelSize = voxelSize
        self.vxLen = np.cbrt(voxelSize)

        # Calculate the number of voxels in each dimension
        self.num_voxels_x = int((x[1] - x[0]) / self.vxLen)
        self.num_voxels_y = int((y[1] - y[0]) / self.vxLen)
        self.num_voxels_z = int((z[1] - z[0]) / self.vxLen)

        # Create a 3D zeros array with corresponding coordinates
        self.zeros_array = np.zeros((self.num_voxels_x, self.num_voxels_y, self.num_voxels_z))

        # Generate coordinates for each point in the array
        self.x_coords = np.linspace(x[0], x[1], self.num_voxels_x)
        self.y_coords = np.linspace(y[0], y[1], self.num_voxels_y)
        self.z_coords = np.linspace(z[0], z[1], self.num_voxels_z)

        self.XX, self.YY, self.ZZ = np.meshgrid(self.x_coords, self.y_coords, self.z_coords)