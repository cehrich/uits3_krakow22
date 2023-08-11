from skspatial.objects import Point,Line,Vector
import numpy as np
import math

class Vertex:
    def __init__(self,position=None,point=None,dca=None,dca2origin=None,openingAngle=None):
        if position : self.position = position
        else : self.position = [0,0,0]

        if point : self.point = point
        else : self.point = Point(self.position)

        if dca : self.dca = dca
        else : self.dca = -1

        if dca2origin : self.dca2origin = dca2origin
        else : self.dca2origin = -1

        if openingAngle : self.openingAngle = openingAngle
        else : self.openingAngle = 0
        
    def fromTracks(self,tracks):
        if len(tracks) == 2:
            intersections = [tracks[0].line.intersect_line(tracks[1].line, check_coplanar=False),
                            tracks[1].line.intersect_line(tracks[0].line, check_coplanar=False)]
            self.point = Point([np.mean([intersections[i][j] for i in range(len(tracks))]) for j in range(3)])
            self.position = [self.point[0],self.point[1],self.point[2]]
            self.dcaVec = Vector.from_points(intersections[0],intersections[1])
            self.dca = tracks[0].line.distance_line(tracks[1].line)
            self.dca2origin = self.point.distance_point(Point([0,0,0]))
            self.openingAngle = tracks[1].vector.angle_between(tracks[0].vector)
        else:
            raise Exception("Provide 2 tracks to construct vertex: #tracks_given = "+len(tracks))
            
    def twistVertex(self, angle):
        zsign = -1
        if self.position[2]>0:
            zsign = 1
        ysign = -1
        if self.position[1]>0:
            ysign = 1
        R = math.sqrt(self.position[0]**2+self.position[1]**2)
        phiX = math.acos(self.position[0]/R)
        phiY = math.asin(self.position[1]/R)
        self.position[0]=  R*math.cos(phiX+ysign*angle*math.pi/180)
        self.position[1]=  R*math.sin(phiY+ysign*angle*math.pi/180)

        self.point = Point(self.position)
        #return self