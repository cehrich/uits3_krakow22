from skspatial.objects import Line,Vector

class Track:
    def __init__(self,point=None,vector=None,line=None, nClusters=None, rms=None):
        if point : self.point = point
        else : self.point = [0,0,0]

        if vector : self.vector = vector
        else : self.vector = [1,0,0]

        #if unitVector : self.unitVector = unitVector
        #else : self.unitVector = [1,0,0]
            
        if line : self.line = line
        else : self.line = Line(point=self.point, direction=self.vector)

        if nClusters : self.nClusters = nClusters
        else : self.nClusters = 0

        if rms : self.rms = rms
        else : self.rms = 0
    
    def fromClusters(self,clusters):
        nClusters = len(clusters)
        if nClusters > 1:
            self.nClusters = nClusters
            clusterPositions = [cluster.globalPos for cluster in clusters]
            line = Line.best_fit(clusterPositions)
            self.line = line
            self.point = line.point
            self.vector = line.vector
            if self.vector[2] < 0: self.vector  = Vector([axis*-1 for axis in self.vector])

            rms = lambda self,clusters: (sum(self.line.distance_point(cluster.globalPos)**2 for cluster in clusters)/len(clusters))**(1/2)
            self.rms = rms(self,clusters)
        else:
            raise Exception("Not enough clusters to construct track: #clusters = "+len(clusters))

 #   def calcUnitVector:
  #      magnitude=sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
   #     for coord, vecVal enumerate(self.vector):
    #        self.unitVector[coord]=vecVal/magnitude
     #   return unitVector
           
    def propagate2point(self,point):
        return self.line.project_point(point)
    
  #  def pathThroughDet(self,ALPIDE): #WIP may not cancel this
    #    detThick=0.025 #25 micron detector in mm
    #    radius = [
    #    "ALPIDE_0" : 30,
    #    "ALPIDE_1" : 24,
    #    "ALPIDE_2" : 18,
     #   "ALPIDE_3" : 18,
     #   "ALPIDE_4" : 30,
     #   ]
        
        
    