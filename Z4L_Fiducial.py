from HiggsAnalysis.CombinedLimit.PhysicsModel import *


class H4lZ4lInclusiveFiducialRatio( PhysicsModel ):
    ''' Model used to unfold differential distributions '''

    def __init__(self):
        PhysicsModel.__init__(self)
        self.SigmaRange=[0.,10]
        self.RatioSigmaRange=[0.,10]
        self.MHRange=[115.,130.]
        self.DeltaMHmZRange=[30.,40.]
        self.defaultMH = 125.0
        self.defaultDeltaMHmZ = 33.8124
        self.fixMH = False
        self.fixDeltaMHmZ = False
        self.debug=1

    def setPhysicsOptions(self,physOptions):
        if self.debug>0:print "Setting PhysicsModel Options"
        for po in physOptions:
            if po.startswith("SigmaRange="):
                self.SigmaRange=po.replace("SigmaRange=","").split(":")
                if len(self.SigmaRange)!=2:
                    raise RunTimeError, "SigmaRange require minimal and maximal values: SigmaRange=min:max"
                if self.debug>0:print "new SigmaRange is ", self.SigmaRange
            if po.startswith("RatioSigmaRange="):
                self.RatioSigmaRange=po.replace("RatioSigmaRange=","").split(":")
                if len(self.RatioSigmaRange)!=2:
                    raise RunTimeError, "RatioSigmaRange require minimal and maximal values: RatioSigmaRange=min:max"
                if self.debug>0:print "new RatioSigmaRange is ", self.RatioSigmaRange
            if po.startswith("MHRange="):
                if self.debug>0: print "setting MH mass range floating:",po.replace("MHRange=","").split(":")
                self.MHRange=po.replace("MHRange=","").split(",")
                #checks
                if len(self.MHRange) != 2:
                    raise RuntimeError, "MH range definition requires two extrema"
                elif float(self.MHRange[0]) >= float(self.MHRange[1]):
                    raise RuntimeError, "Extrema for MH mass range defined with inverterd order. Second must be larger the first"
            if po.startswith("DeltaMHmZRange="):
                if self.debug>0: print "setting MH-MZ mass range floating:",po.replace("DeltaMHmZRange=","").split(":")
                self.DeltaMHmZRange=po.replace("DeltaMHmZRange=","").split(",")
                #checks
                if len(self.DeltaMHmZRange) != 2:
                    raise RuntimeError, "MH-MZ range definition requires two extrema"
                elif float(self.DeltaMHmZRange[0]) >= float(self.DeltaMHmZRange[1]):
                    raise RuntimeError, "Extrema for MH-MZ mass range defined with inverterd order. Second must be larger the first"
            if po.startswith("defaultMH="):
                self.defaultMH=float( po.replace('defaultMH=','') )
            if po.startswith("defaultDeltaMHmZ="):
                self.defaultDeltaMHmZ=float( po.replace('defaultDeltaMHmZ=','') )
            if po.startswith("fixMH"):
                self.fixMH = True
            if po.startswith("fixDeltaMHmZ"):
                self.fixDeltaMHmZ = True
            #verbose
            if po.startswith("verbose"):
                self.debug = 1

    def doParametersOfInterest(self):
        POIs=""
        if self.debug>0:print "Setting pois"

        self.modelBuilder.doVar("SigmaH[1,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("SigmaH4e[1,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("SigmaH4mu[1,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("RatioSigmaHoZ[1,%s,%s]" % (self.RatioSigmaRange[0], self.RatioSigmaRange[1]))
        self.modelBuilder.doVar("RatioSigmaHoZ4e[1,%s,%s]" % (self.RatioSigmaRange[0], self.RatioSigmaRange[1]))
        self.modelBuilder.doVar("RatioSigmaHoZ4mu[1,%s,%s]" % (self.RatioSigmaRange[0], self.RatioSigmaRange[1]))

        POIs+="SigmaH,"
        POIs+="SigmaH4e,"
        POIs+="SigmaH4mu,"
        POIs+="RatioSigmaHoZ,"
        POIs+="RatioSigmaHoZ4e,"
        POIs+="RatioSigmaHoZ4mu,"

        # --- Other parameters ----
        poiNames=[]
        # set Parameter MH
        if self.modelBuilder.out.var("MH"):
            if len(self.MHRange) == 2:
                print 'MH will be left floating within', self.MHRange[0], 'and', self.MHRange[1]
                self.modelBuilder.out.var("MH").setRange(float(self.MHRange[0]),float(self.MHRange[1]))
                self.modelBuilder.out.var("MH").setConstant(False)
                poiNames += [ 'MH' ]
            else:
                print 'MH will be assumed to be', self.defaultMH
                self.modelBuilder.out.var("MH").removeRange()
                self.modelBuilder.out.var("MH").setVal(self.defaultMH)
                self.modelBuilder.out.var("MH").setConstant(True)
        else:
            if len(self.MHRange) == 2:
                print 'MH will be left floating within', self.MHRange[0], 'and', self.MHRange[1]
                self.modelBuilder.doVar("MH[%s,%s]" % (self.MHRange[0],self.MHRange[1]))
                poiNames += [ 'MH' ]
            else:
                print 'MH (not there before) will be assumed to be', self.defaultMH
                self.modelBuilder.doVar("MH[%g]" % self.defaultMH)
        # set Parameter DeltaMHmZ 
        if self.modelBuilder.out.var("DeltaMHmZ"):
            if len(self.DeltaMHmZRange) == 2:
                print 'DeltaMHmZ will be left floating within', self.DeltaMHmZRange[0], 'and', self.DeltaMHmZRange[1]
                self.modelBuilder.out.var("DeltaMHmZ").setRange(float(self.DeltaMHmZRange[0]),float(self.DeltaMHmZRange[1]))
                self.modelBuilder.out.var("DeltaMHmZ").setConstant(False)
                poiNames += [ 'DeltaMHmZ' ]
            else:
                print 'DeltaMHmZ will be assumed to be', self.defaultDeltaMHmZ
                self.modelBuilder.out.var("DeltaMHmZ").removeRange()
                self.modelBuilder.out.var("DeltaMHmZ").setVal(self.defaultDeltaMHmZ)
                self.modelBuilder.out.var("DeltaMHmZ").setConstant(True)
        else:
            if len(self.DeltaMHmZRange) == 2:
                print 'DeltaMHmZ will be left floating within', self.DeltaMHmZRange[0], 'and', self.DeltaMHmZRange[1]
                self.modelBuilder.doVar("DeltaMHmZ[%s,%s]" % (self.DeltaMHmZRange[0],self.DeltaMHmZRange[1]))
                poiNames += [ 'DeltaMHmZ' ]
            else:
                print 'DeltaMHmZ (not there before) will be assumed to be', self.defaultDeltaMHmZ
                self.modelBuilder.doVar("DeltaMHmZ[%g]" % self.defaultDeltaMHmZ)

        if (self.fixMH):
            self.modelBuilder.out.var("MH").setConstant(True)
            for ixx in range(poiNames.count('MH')): poiNames.remove('MH')
        if (self.fixDeltaMHmZ):
            self.modelBuilder.out.var("DeltaMHmZ").setConstant(True)
            for ixx in range(poiNames.count('DeltaMHmZ')): poiNames.remove('DeltaMHmZ')

        for poi in poiNames:
            POIs += "%s,"%poi
        POIs = POIs[:-1] # remove last comma
        self.modelBuilder.doSet("POI",POIs)
        print "set up pois"
        self.setup()

    def setup(self):
        self.modelBuilder.factory_('expr::sigma_trueH4e("@0", SigmaH4e)')
        self.modelBuilder.factory_('expr::sigma_trueH4mu("@0", SigmaH4mu)')
        self.modelBuilder.factory_('expr::sigma_trueH2e2mu("(@0-@1-@2)", SigmaH, SigmaH4e, SigmaH4mu)')
        self.modelBuilder.factory_('expr::sigma_trueZ4e("(@0/@1)", SigmaH4e, RatioSigmaHoZ4e)')
        self.modelBuilder.factory_('expr::sigma_trueZ4mu("(@0/@1)", SigmaH4mu, RatioSigmaHoZ4mu)')
        self.modelBuilder.factory_('expr::sigma_trueZ2e2mu("(@0/@1-@2/@3-@4/@5)", SigmaH, RatioSigmaHoZ, SigmaH4e, RatioSigmaHoZ4e, SigmaH4mu, RatioSigmaHoZ4mu)')

    def getYieldScale(self,bin,process):
        if not self.DC.isSignal[process]: return 1
        if process in [ "trueH4e", "trueH4mu","trueH2e2mu","trueZ4e", "trueZ4mu","trueZ2e2mu"]:
            return "sigma_"+process
        else: 
            return 1


class H4lZ4lInclusiveFiducialRatioV2( PhysicsModel ):
    ''' Model used to unfold differential distributions '''

    def __init__(self):
        PhysicsModel.__init__(self)
        self.SigmaRange=[0.,10]
        self.RatioSigmaRange=[0.,10]
        self.MHRange=[115.,130.]
        self.DeltaMHmZRange=[30.,40.]
        self.defaultMH = 125.0
        self.defaultDeltaMHmZ = 33.8124
        self.fixMH = False
        self.fixDeltaMHmZ = False
        self.debug=1

    def setPhysicsOptions(self,physOptions):
        if self.debug>0:print "Setting PhysicsModel Options"
        for po in physOptions:
            if po.startswith("SigmaRange="):
                self.SigmaRange=po.replace("SigmaRange=","").split(":")
                if len(self.SigmaRange)!=2:
                    raise RunTimeError, "SigmaRange require minimal and maximal values: SigmaRange=min:max"
                if self.debug>0:print "new SigmaRange is ", self.SigmaRange
            if po.startswith("RatioSigmaRange="):
                self.RatioSigmaRange=po.replace("RatioSigmaRange=","").split(":")
                if len(self.RatioSigmaRange)!=2:
                    raise RunTimeError, "RatioSigmaRange require minimal and maximal values: RatioSigmaRange=min:max"
                if self.debug>0:print "new RatioSigmaRange is ", self.RatioSigmaRange
            if po.startswith("MHRange="):
                if self.debug>0: print "setting MH mass range floating:",po.replace("MHRange=","").split(":")
                self.MHRange=po.replace("MHRange=","").split(",")
                #checks
                if len(self.MHRange) != 2:
                    raise RuntimeError, "MH range definition requires two extrema"
                elif float(self.MHRange[0]) >= float(self.MHRange[1]):
                    raise RuntimeError, "Extrema for MH mass range defined with inverterd order. Second must be larger the first"
            if po.startswith("DeltaMHmZRange="):
                if self.debug>0: print "setting MH-MZ mass range floating:",po.replace("DeltaMHmZRange=","").split(":")
                self.DeltaMHmZRange=po.replace("DeltaMHmZRange=","").split(",")
                #checks
                if len(self.DeltaMHmZRange) != 2:
                    raise RuntimeError, "MH-MZ range definition requires two extrema"
                elif float(self.DeltaMHmZRange[0]) >= float(self.DeltaMHmZRange[1]):
                    raise RuntimeError, "Extrema for MH-MZ mass range defined with inverterd order. Second must be larger the first"
            if po.startswith("defaultMH="):
                self.defaultMH=float( po.replace('defaultMH=','') )
            if po.startswith("defaultDeltaMHmZ="):
                self.defaultDeltaMHmZ=float( po.replace('defaultDeltaMHmZ=','') )
            if po.startswith("fixMH"):
                self.fixMH = True
            if po.startswith("fixDeltaMHmZ"):
                self.fixDeltaMHmZ = True
            #verbose
            if po.startswith("verbose"):
                self.debug = 1

    def doParametersOfInterest(self):
        POIs=""
        if self.debug>0:print "Setting pois"

        self.modelBuilder.doVar("SigmaH4e[1,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("SigmaH4mu[1,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("SigmaH2e2mu[1,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("RatioSigmaHoZ4e[1,%s,%s]" % (self.RatioSigmaRange[0], self.RatioSigmaRange[1]))
        self.modelBuilder.doVar("RatioSigmaHoZ4mu[1,%s,%s]" % (self.RatioSigmaRange[0], self.RatioSigmaRange[1]))
        self.modelBuilder.doVar("RatioSigmaHoZ2e2mu[1,%s,%s]" % (self.RatioSigmaRange[0], self.RatioSigmaRange[1]))

        POIs+="SigmaH4e,"
        POIs+="SigmaH4mu,"
        POIs+="SigmaH2e2mu,"
        POIs+="RatioSigmaHoZ4e,"
        POIs+="RatioSigmaHoZ4mu,"
        POIs+="RatioSigmaHoZ2e2mu,"

        # --- Other parameters ----
        poiNames=[]
        # set Parameter MH
        if self.modelBuilder.out.var("MH"):
            if len(self.MHRange) == 2:
                print 'MH will be left floating within', self.MHRange[0], 'and', self.MHRange[1]
                self.modelBuilder.out.var("MH").setRange(float(self.MHRange[0]),float(self.MHRange[1]))
                self.modelBuilder.out.var("MH").setConstant(False)
                poiNames += [ 'MH' ]
            else:
                print 'MH will be assumed to be', self.defaultMH
                self.modelBuilder.out.var("MH").removeRange()
                self.modelBuilder.out.var("MH").setVal(self.defaultMH)
                self.modelBuilder.out.var("MH").setConstant(True)
        else:
            if len(self.MHRange) == 2:
                print 'MH will be left floating within', self.MHRange[0], 'and', self.MHRange[1]
                self.modelBuilder.doVar("MH[%s,%s]" % (self.MHRange[0],self.MHRange[1]))
                poiNames += [ 'MH' ]
            else:
                print 'MH (not there before) will be assumed to be', self.defaultMH
                self.modelBuilder.doVar("MH[%g]" % self.defaultMH)
        # set Parameter DeltaMHmZ
        if self.modelBuilder.out.var("DeltaMHmZ"):
            if len(self.DeltaMHmZRange) == 2:
                print 'DeltaMHmZ will be left floating within', self.DeltaMHmZRange[0], 'and', self.DeltaMHmZRange[1]
                self.modelBuilder.out.var("DeltaMHmZ").setRange(float(self.DeltaMHmZRange[0]),float(self.DeltaMHmZRange[1]))
                self.modelBuilder.out.var("DeltaMHmZ").setConstant(False)
                poiNames += [ 'DeltaMHmZ' ]
            else:
                print 'DeltaMHmZ will be assumed to be', self.defaultDeltaMHmZ
                self.modelBuilder.out.var("DeltaMHmZ").removeRange()
                self.modelBuilder.out.var("DeltaMHmZ").setVal(self.defaultDeltaMHmZ)
                self.modelBuilder.out.var("DeltaMHmZ").setConstant(True)
        else:
            if len(self.DeltaMHmZRange) == 2:
                print 'DeltaMHmZ will be left floating within', self.DeltaMHmZRange[0], 'and', self.DeltaMHmZRange[1]
                self.modelBuilder.doVar("DeltaMHmZ[%s,%s]" % (self.DeltaMHmZRange[0],self.DeltaMHmZRange[1]))
                poiNames += [ 'DeltaMHmZ' ]
            else:
                print 'DeltaMHmZ (not there before) will be assumed to be', self.defaultDeltaMHmZ
                self.modelBuilder.doVar("DeltaMHmZ[%g]" % self.defaultDeltaMHmZ)

        if (self.fixMH):
            self.modelBuilder.out.var("MH").setConstant(True)
            for ixx in range(poiNames.count('MH')): poiNames.remove('MH')
        if (self.fixDeltaMHmZ):
            self.modelBuilder.out.var("DeltaMHmZ").setConstant(True)
            for ixx in range(poiNames.count('DeltaMHmZ')): poiNames.remove('DeltaMHmZ')

        for poi in poiNames:
            POIs += "%s,"%poi
        POIs = POIs[:-1] # remove last comma
        self.modelBuilder.doSet("POI",POIs)
        print "set up pois"
        self.setup()

    def setup(self):
        self.modelBuilder.factory_('expr::sigma_trueH4e("@0", SigmaH4e)')
        self.modelBuilder.factory_('expr::sigma_trueH4mu("@0", SigmaH4mu)')
        self.modelBuilder.factory_('expr::sigma_trueH2e2mu("@0", SigmaH2e2mu)')
        self.modelBuilder.factory_('expr::sigma_trueZ4e("(@0/@1)", SigmaH4e, RatioSigmaHoZ4e)')
        self.modelBuilder.factory_('expr::sigma_trueZ4mu("(@0/@1)", SigmaH4mu, RatioSigmaHoZ4mu)')
        self.modelBuilder.factory_('expr::sigma_trueZ2e2mu("(@0/@1)", SigmaH2e2mu, RatioSigmaHoZ2e2mu)')

    def getYieldScale(self,bin,process):
        if not self.DC.isSignal[process]: return 1
        if process in [ "trueH4e", "trueH4mu","trueH2e2mu","trueZ4e", "trueZ4mu","trueZ2e2mu"]:
            return "sigma_"+process
        else:
            return 1



class Z4lInclusiveFiducial( PhysicsModel ):
    ''' Model used to unfold differential distributions '''

    def __init__(self):
        PhysicsModel.__init__(self)
        self.SigmaRange=[0.,10]
        self.MZRange=[80,110]
        self.defaultMZ = 91.1876
        self.fixMZ = False
        self.debug=1


    def setPhysicsOptions(self,physOptions):
        if self.debug>0:print "Setting PhysicsModel Options"
        for po in physOptions:
            if po.startswith("SigmaRange="):
                self.SigmaRange=po.replace("SigmaRange=","").split(":")
                if len(self.SigmaRange)!=2:
                    raise RunTimeError, "SigmaRange require minimal and maximal values: SigmaRange=min:max"
                if self.debug>0: print "new SigmaRange is ", self.SigmaRange
            if po.startswith("MZRange="):
                if self.debug>0: print "setting MZ floating:",po.replace("MZRange=","").split(":")
                self.MZRange=po.replace("MZRange=","").split(",")
                #checks
                if len(self.MZRange) != 2:
                    raise RuntimeError, "MZRange require minimal and maximal values: MZRange=min:max"
                elif float(self.MZRange[0]) >= float(self.MZRange[1]):
                    raise RuntimeError, "Extrema for MZRange defined with inverterd order. Second must be larger the first"
            if po.startswith("defaultMZ="):
                self.defaultMZ=float( po.replace('defaultMZ=','') )
            if po.startswith("fixMZ"):
                self.fixMZ = True
            #verbose
            if po.startswith("verbose"):
                self.debug = 1

    def doParametersOfInterest(self):
        POIs=""
        if self.debug>0:print "Setting POIs"
                
        self.modelBuilder.doVar("SigmaZ[1,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("SigmaZ4e[0.25,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("SigmaZ4mu[0.25,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
                
        POIs+="SigmaZ,"
        POIs+="SigmaZ4e,"
        POIs+="SigmaZ4mu,"
                                        
        poiNames=[]
        if self.modelBuilder.out.var("MZ"):
            if len(self.MZRange) == 2:
                print 'MZ will be left floating within', self.MZRange[0], 'and', self.MZRange[1]
                self.modelBuilder.out.var("MZ").setRange(float(self.MZRange[0]),float(self.MZRange[1]))
                self.modelBuilder.out.var("MZ").setConstant(False)
                poiNames += [ 'MZ' ]
            else:
                print 'MZ will be assumed to be', self.defaultMZ
                self.modelBuilder.out.var("MZ").removeRange()
                self.modelBuilder.out.var("MZ").setVal(self.defaultMZ)
        else:
            if len(self.MZRange) == 2:
                print 'MZ will be left floating within', self.MZRange[0], 'and', self.MZRange[1]
                self.modelBuilder.doVar("MZ[%s,%s]" % (self.MZRange[0],self.MZRange[1]))
                poiNames += [ 'MZ' ]
            else:
                print 'MZ (not there before) will be assumed to be', self.defaultMZ
                self.modelBuilder.doVar("MZ[%g]" % self.defaultMZ)

        if (self.fixMZ): 
            self.modelBuilder.out.var("MZ").setConstant(True)
            for ixx in range(poiNames.count('MZ')): poiNames.remove('MZ')

        for poi in poiNames:
            POIs += ",%s"%poi

        self.modelBuilder.doSet("POI",POIs)

        print "set up pois"
        self.setup()

    def setup(self):

        self.modelBuilder.factory_('expr::sigma_trueZ4e("@0", SigmaZ4e)')
        self.modelBuilder.factory_('expr::sigma_trueZ4mu("@0", SigmaZ4mu)')
        self.modelBuilder.factory_('expr::sigma_trueZ2e2mu("(@0-@1-@2)", SigmaZ, SigmaZ4e, SigmaZ4mu)')

    def getYieldScale(self,bin,process):

        if not self.DC.isSignal[process]: return 1

        if process in ["trueZ4e","trueZ4mu","trueZ2e2mu"]: 
            return "sigma_"+process
        else : return 1




class Z4lInclusiveFiducialV2( PhysicsModel ):
    ''' Model used to unfold differential distributions '''

    def __init__(self):
        PhysicsModel.__init__(self)
        self.SigmaRange=[0.,10]
        self.MZRange=[80,110]
        self.defaultMZ = 91.1876
        self.fixMZ = False
        self.debug=1


    def setPhysicsOptions(self,physOptions):
        if self.debug>0:print "Setting PhysicsModel Options"
        for po in physOptions:
            if po.startswith("SigmaRange="):
                self.SigmaRange=po.replace("SigmaRange=","").split(":")
                if len(self.SigmaRange)!=2:
                    raise RunTimeError, "SigmaRange require minimal and maximal values: SigmaRange=min:max"
                if self.debug>0: print "new SigmaRange is ", self.SigmaRange
            if po.startswith("MZRange="):
                if self.debug>0: print "setting MZ floating:",po.replace("MZRange=","").split(":")
                self.MZRange=po.replace("MZRange=","").split(",")
                #checks
                if len(self.MZRange) != 2:
                    raise RuntimeError, "MZRange require minimal and maximal values: MZRange=min:max"
                elif float(self.MZRange[0]) >= float(self.MZRange[1]):
                    raise RuntimeError, "Extrema for MZRange defined with inverterd order. Second must be larger the first"
            if po.startswith("defaultMZ="):
                self.defaultMZ=float( po.replace('defaultMZ=','') )
            if po.startswith("fixMZ"):
                self.fixMZ = True
            #verbose
            if po.startswith("verbose"):
                self.debug = 1

    def doParametersOfInterest(self):
        POIs=""
        if self.debug>0:print "Setting POIs"

        self.modelBuilder.doVar("SigmaZ4e[1.0,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("SigmaZ4mu[1.0,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))
        self.modelBuilder.doVar("SigmaZ2e2mu[1.0,%s,%s]" % (self.SigmaRange[0], self.SigmaRange[1]))

        POIs+="SigmaZ4e,"
        POIs+="SigmaZ4mu,"
        POIs+="SigmaZ2e2mu,"

        poiNames=[]
        if self.modelBuilder.out.var("MZ"):
            if len(self.MZRange) == 2:
                print 'MZ will be left floating within', self.MZRange[0], 'and', self.MZRange[1]
                self.modelBuilder.out.var("MZ").setRange(float(self.MZRange[0]),float(self.MZRange[1]))
                self.modelBuilder.out.var("MZ").setConstant(False)
                poiNames += [ 'MZ' ]
            else:
                print 'MZ will be assumed to be', self.defaultMZ
                self.modelBuilder.out.var("MZ").removeRange()
                self.modelBuilder.out.var("MZ").setVal(self.defaultMZ)
                self.modelBuilder.out.var("MZ").setConstant(True)
        else:
            if len(self.MZRange) == 2:
                print 'MZ will be left floating within', self.MZRange[0], 'and', self.MZRange[1]
                self.modelBuilder.doVar("MZ[%s,%s]" % (self.MZRange[0],self.MZRange[1]))
                poiNames += [ 'MZ' ]
            else:
                print 'MZ (not there before) will be assumed to be', self.defaultMZ
                self.modelBuilder.doVar("MZ[%g]" % self.defaultMZ)
        if (self.fixMZ):
            self.modelBuilder.out.var("MZ").setConstant(True)
            for ixx in range(poiNames.count('MZ')): poiNames.remove('MZ')

        for poi in poiNames:
            POIs += ",%s"%poi

        self.modelBuilder.doSet("POI",POIs)
        print "set up pois"
        self.setup()

    def setup(self):
        self.modelBuilder.factory_('expr::sigma_trueZ4e("@0", SigmaZ4e)')
        self.modelBuilder.factory_('expr::sigma_trueZ4mu("@0", SigmaZ4mu)')
        self.modelBuilder.factory_('expr::sigma_trueZ2e2mu("@0", SigmaZ2e2mu)')

    def getYieldScale(self,bin,process):
        if not self.DC.isSignal[process]: return 1
        if process in ["trueZ4e","trueZ4mu","trueZ2e2mu"]:
            return "sigma_"+process
        else : return 1



class Z4lDifferentialFiducial( PhysicsModel ):
        ''' Model used to unfold differential distributions '''

        def __init__(self):
                PhysicsModel.__init__(self)
                self.Range=[0.,10]
                self.fracRange=[0.,0.5]
                self.nBin=4
                self.mZRange=[]
                self.debug=1
                self.mass=0

        def setPhysicsOptions(self,physOptions):
                if self.debug>0:print "Setting PhysicsModel Options"
                for po in physOptions:
                        if po.startswith("range="):
                                self.Range=po.replace("range=","").split(":")
                                if len(self.Range)!=2:
                                        raise RunTimeError, "Range require minimal and maximal values: range=min:max"
                                if self.debug>0:print "new Range is ", self.Range
                        if po.startswith("nBin="):
                                self.nBin=int(po.replace("nBin=",""))
                                if self.debug>0:print "new n. of bins is ",self.nBin
                        if po.startswith("Z4lMassRange="):
                                if self.debug>0: print "setting Z4l mass range floating:",po.replace("Z4lMassRange=","").split(":")
                                self.mZRange=po.replace("Z4lMassRange=","").split(",")
                                #checks
                                if len(self.mZRange) != 2:
                                        raise RuntimeError, "Z4l mass range definition requires two extrema"
                                elif float(self.mZRange[0]) >= float(self.mZRange[1]):
                                        raise RuntimeError, "Extrema for Z4l mass range defined with inverterd order. Second must be larger the first"
                        if po.startswith("mass="):
                                self.mass=float( po.replace('mass=','') )

                        #verbose
                        if po.startswith("verbose"):
                                self.debug = 1

        def doParametersOfInterest(self):
                POIs=""
                if self.debug>0:print "Setting pois"
                for iBin in range(0,self.nBin):
                    if self.modelBuilder.out.var("Z4lrBin%d" % (iBin)):
                        self.modelBuilder.out.var("Z4lrBin%d" % (iBin)).setRange(self.Range[0], self.Range[1])
                        self.modelBuilder.out.var("Z4lrBin%d" % (iBin)).setConstant(False)
                    else :
                        self.modelBuilder.doVar("Z4lrBin%d[1, %s,%s]" % (iBi, self.Range[0],self.Range[1]))

                    if self.modelBuilder.out.var("Z4lfrac4eBin%d" % (iBin)):
                        self.modelBuilder.out.var("Z4lfrac4eBin%d" % (iBin)).setRange(self.fracRange[0], self.fracRange[1])
                        self.modelBuilder.out.var("Z4lfrac4eBin%d" % (iBin)).setConstant(False)
                    else :
                        self.modelBuilder.doVar("Z4lfrac4eBin%d[0.25, %s,%s]" % (iBin, self.fracRange[0],self.fracRange[1]))

                    if self.modelBuilder.out.var("Z4lfrac4muBin%d" % (iBin)):
                        self.modelBuilder.out.var("Z4lfrac4muBin%d" % (iBin)).setRange(self.fracRange[0], self.fracRange[1])
                        self.modelBuilder.out.var("Z4lfrac4muBin%d" % (iBin)).setConstant(False)
                    else :
                        self.modelBuilder.doVar("Z4lfrac4muBin%d[0.25, %s,%s]" % (iBin, self.fracRange[0],self.fracRange[1]))

                    if iBin>=0:
                        POIs+="Z4lrBin%d,"%iBin
                        POIs+="Z4lfrac4eBin%d,"%iBin
                        POIs+="Z4lfrac4muBin%d,"%iBin
                        if self.debug>0:print "Added Bin%d to the POIs"%iBin
                        #if iBin==self.nBin-1: #for out-of-acceptance bin 
                                #if self.debug>0:print "   and set constant to the value 1 "
                                #self.modelBuilder.out.var("r_Bin%d"%iBin).removeRange()
                                #self.modelBuilder.out.var("r_Bin%d"%iBin).setVal(1)
                                #self.modelBuilder.out.var("r_Bin%d"%iBin).setConstant(True)

                # --- Higgs Mass as other parameter ----
#               if self.options.mass != 0:
#                   if self.modelBuilder.out.var("MH"):
#                     self.modelBuilder.out.var("MH").removeRange()
#                     self.modelBuilder.out.var("MH").setVal(self.options.mass)
#                   else:
#                     self.modelBuilder.doVar("MH[%g]" % self.options.mass);
                poiNames=[]
                if self.modelBuilder.out.var("MH"):
                    if len(self.mZRange) == 2:
                        print 'MH will be left floating within', self.mZRange[0], 'and', self.mZRange[1]
                        self.modelBuilder.out.var("MH").setRange(float(self.mZRange[0]),float(self.mZRange[1]))
                        self.modelBuilder.out.var("MH").setConstant(False)
                        poiNames += [ 'MH' ]
                    else:
                        print 'MH will be assumed to be', self.mass
                        self.modelBuilder.out.var("MH").removeRange()
                        self.modelBuilder.out.var("MH").setVal(self.mass)
                else:
                    if len(self.mZRange) == 2:
                        print 'MH will be left floating within', self.mZRange[0], 'and', self.mZRange[1]
                        self.modelBuilder.doVar("MH[%s,%s]" % (self.mZRange[0],self.mZRange[1]))
                        poiNames += [ 'MH' ]
                    else:
                        print 'MH (not there before) will be assumed to be', self.mass
                        self.modelBuilder.doVar("MH[%g]" % self.mass)
                for poi in poiNames:
                        POIs += ",%s"%poi
                self.modelBuilder.doSet("POI",POIs)
                self.setup()

        def setup(self):        
               for iBin in range(0,self.nBin):
                 self.modelBuilder.factory_('expr::frac_trueZ2e2muBin%d("@0*(1-@1-@2)", Z4lrBin%d, Z4lfrac4eBin%d, Z4lfrac4muBin%d)' % (iBin,iBin,iBin,iBin))
                 self.modelBuilder.factory_('expr::frac_trueZ4eBin%d("@0*@1", Z4lrBin%d, Z4lfrac4eBin%d)'% (iBin,iBin,iBin))
                 self.modelBuilder.factory_('expr::frac_trueZ4muBin%d("@0*@1", Z4lrBin%d, Z4lfrac4muBin%d)'% (iBin,iBin,iBin))

        def getYieldScale(self,bin,process):

             if not self.DC.isSignal[process]: return 1

             #print "print process"
             #print process
             name = "fiducial_%s" % process
             
             self.modelBuilder.factory_('expr::%s("@0", frac_%s)' % (name, process))
             if process in [ "trueZ2e2muBin0","trueZ4eBin0","trueZ4muBin0","trueZ2e2muBin1","trueZ4eBin1","trueZ4muBin1","trueZ2e2muBin2","trueZ4eBin2","trueZ4muBin2","trueZ2e2muBin3","trueZ4eBin3","trueZ4muBin3"]: 
                     return name
             else :
                     return 1
                     
Z4linclusiveFiducial=Z4lInclusiveFiducial()
Z4linclusiveFiducialV2=Z4lInclusiveFiducialV2()
Z4ldifferentialFiducial=Z4lDifferentialFiducial()
h4lZ4lInclusiveFiducialRatio=H4lZ4lInclusiveFiducialRatio()
h4lZ4lInclusiveFiducialRatioV2=H4lZ4lInclusiveFiducialRatioV2()
