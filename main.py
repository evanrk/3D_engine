import math
import pygame, sys
import numpy as np
import time

WIDTH, HEIGHT = 500, 500

aspect_ratio = HEIGHT/WIDTH
fov = 90
zfar = 10
znear = 1
fps = 30
camera_position = [0, 0, 0]

class Vertex:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

"""
TODO:
Camera movement
Camera rotation
Turn mesh into triangles

"""


vertices = [
  [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
]

triangles = [
  		#BACK
  		[[0, 0, 1.0],    [0, 1, 1.0],    [1, 1, 1.0]],
  		[[0, 0, 1.0],    [1, 1, 1.0],    [1, 0, 1.0]],
  
  		#RIGHT
  		[[1, 0, 1.0],    [1, 1, 1.0],    [1, 1, 2.0]],
  		[[1, 0, 1.0],    [1, 1, 2.0],    [1, 0, 2.0]],
  
  		#FRONT
  		[[1, 0, 2.0],    [1, 1, 2.0],    [0, 1, 2.0]],
  		[[1, 0, 2.0],    [0, 1, 2.0],    [0, 0, 2.0]],
  
  		#LEFT
  		[[0, 0, 2.0],    [0, 1, 2.0],    [0, 1, 1.0]],
  		[[0, 0, 2.0],    [0, 1, 1.0],    [0, 0, 1.0]],
  
  		#TOP
  		[[0, 1, 1.0],    [0, 1, 2.0],    [1, 1, 2.0]],
  		[[0, 1, 1.0],    [1, 1, 2.0],    [1, 1, 1.0]],
  
  		#BOTTOM
  		[[1, 0, 2.0],    [0, 0, 2.0],    [0, 0, 1.0]],
  		[[1, 0, 2.0],    [0, 0, 1.0],    [1, 0, 1.0]]
    ]

def project_pos(positions_list, fov:float, aspect_ratio:float, znear:float, zfar:float):
  projection_matrix = np.zeros((4, 4))

  projection_matrix[0][0] = aspect_ratio * 1/math.tan((fov*180/math.pi)/2)
  projection_matrix[1][1] = 1/math.tan((fov*180/math.pi)/2)
  projection_matrix[2][2] = zfar / (zfar-znear)
  projection_matrix[3][2] = -zfar*znear/(zfar-znear)
  projection_matrix[2][3] = 1

  projected_pos = []
  for pos in positions_list:
    pos.append(1) #to be able to dot product
    projected_pos.append(np.array(pos).dot(projection_matrix))

  for index, pos in enumerate(projected_pos):
    projected_pos[index] = pos[:2]
  return projected_pos


# projects the 3d points onto the 2d plane so that it can be visualized on a 2d screen
# def project_pos(positions_list, fov:float, aspect_ratio:float, znear:float, zfar:float):
#   projected_pos = []
#   fov_scale = 1/math.tan((fov * math.pi / 180)/2)
#   for pos in positions_list:

#     print(pos[0])
#     x = pos[0]*fov_scale*aspect_ratio
#     y = pos[1]*fov_scale
    
#     z_scale = zfar/(zfar-znear)
    
#     z = pos[2] * z_scale
#     if z:
#       print(f"Scaled pos:{x/z, y/z}, Scale: {z_scale}, z: {z}")
#       projected_pos.append([x/z, y/z])
#     else:
#       print(f"Scaled pos:{'OUT OF RANGE', 'OUT OF RANGE'}, Scale: {z_scale}, z: {z}")
#   print("="*50)
  
#   return projected_pos, pos[2]


def normalize_pos(positions_list, scale=1):
  normalized_pos = []
  for pos in positions_list:
    normalized_pos.append([pos[0]*scale + WIDTH/2, pos[1]*-scale + HEIGHT/2])
  
  return normalized_pos

def main():
  pygame.init()
  pygame.display.set_caption("   3D renderer")
  screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
  screen.fill((20, 240, 30))
  
  # point of origin
  pygame.draw.polygon(screen, (0, 0, 255), [[WIDTH/2-0.1, HEIGHT/2-1], [WIDTH/2-0.1, HEIGHT/2+1], [WIDTH/2+0.1, HEIGHT/2-1], [WIDTH/2+0.1, HEIGHT/2+1]], 2)
  
  theta_x = 0
  theta_z = 0
  while True:
    screen.fill((20,240,30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.display.quit()
          pygame.quit()
          sys.exit()
    
    theta_x += 0.01
    theta_z += 0.01

    #rotation matricies
    rotation_x, rotation_z = np.zeros((3, 3)), np.zeros((3, 3))
    
    #X rotation
    rotation_x[0][0] = 1
    rotation_x[1][1] = math.cos(theta_x * 0.5)
    rotation_x[1][2] = -math.sin(theta_x * 0.5)
    rotation_x[2][1] = math.sin(theta_x * 0.5)
    rotation_x[2][2] = math.cos(theta_x * 0.5)
    # rotation_x[3][3] = 1
    
    #Z rotation
    rotation_z[0][0] = math.cos(theta_z)
    rotation_z[0][1] = math.sin(theta_z)
    rotation_z[1][0] = -math.sin(theta_z)
    rotation_z[1][1] = math.cos(theta_z)
    rotation_z[2][2] = 1
    # rotation_z[3][3] = 1
    
  
    for triangle in triangles:
      rotated_triangle = [0, 0, 0]
      
      #rotation on x-axis
      rotated_triangle[0] = np.array([triangle[0]]).dot(rotation_x).tolist()[0]
      rotated_triangle[1] = np.array([triangle[1]]).dot(rotation_x).tolist()[0]
      rotated_triangle[2] = np.array([triangle[2]]).dot(rotation_x).tolist()[0]
  
      #rotation on z-axis
      rotated_triangle[0] = np.array([rotated_triangle[0]]).dot(rotation_z).tolist()[0]
      rotated_triangle[1] = np.array([rotated_triangle[1]]).dot(rotation_z).tolist()[0]
      rotated_triangle[2] = np.array([rotated_triangle[2]]).dot(rotation_z).tolist()[0]

      translated_triangle = rotated_triangle
      for i in range(3):
        translated_triangle[i][2] = rotated_triangle[i][2] + 3
      
      # projected_triangle = [xscaled, yscaled, zscaled, z(unscaled)]
      projected_triangle = project_pos(translated_triangle, fov, aspect_ratio, znear, zfar)
      # pygame.draw.polygon(screen, (0, 0, 0), normalize_pos(projected_triangle, scale=-100))
      pygame.draw.polygon(screen, (255, 255, 255), normalize_pos(projected_triangle, scale=-100), 3)
      
      pygame.display.update()
    time.sleep(1/fps)

main()