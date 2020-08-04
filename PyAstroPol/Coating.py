import numpy as np
import copy as cp
import random as rd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime as dt
#
from .Source import *
from .Surface import *
#

class Coating():
    """
    Multi-layer coating effects on transmission and reflection
    For geometric ray tracing purposes, their thickness is neglected. 
    // Attributes : General
    RI : Complex Float (N,1) : Array of refractive indiced of all the layers
    Thick : Float (N,1) : Array of thicknesses of all the layers
    // Attributes : Polarization
    rs : FloatComplex(N,1) : Complex coefficient of reflection for s-polarization of all Rays 
    rp : FloatComplex(N,1) : Complex coefficient of reflection for p-polarization of all Rays 
    ts : FloatComplex(N,1) : Complex coefficient of transmission for s-polarization of all Rays 
    tp : FloatComplex(N,1) : Complex coefficient of transmission for p-polarization of all Rays
    """
    def __init__(self, RI, Thick):
        if (len(RI) != len(Thick)):
            print('Error! Check the inputs!')
            return
        self.RI = np.copy(RI)
        self.Thick = np.copy(Thick)
        return
    
    # This will compute effects on transmission and reflection
    def applyToSurface(self, Surf):                                
        self.Wavelength = np.copy(Surf.iRays.Wavelength)
        self.iRI, self.sRI = np.copy(Surf.iRI), np.copy(Surf.tRI)
        self.iTheta, self.sTheta = np.copy(Surf.iTheta), np.copy(Surf.tTheta)
        
        # for s-polarization
        iEta, sEta = self.iRI*np.cos(self.iTheta), self.sRI*np.cos(self.sTheta)
        CoatMatrix = np.matrix([[1,0],[0,1]])
        for RI_j, Thick_j in zip(self.RI, self.Thick):
            Theta_j = np.arcsin(self.iRI/RI_j)*np.sin(self.iTheta)
            Eta_j = RI_j*np.cos(Theta_j)
            LayerMatrix_j = np.matrix([[np.cos(Delta_j), 1j*np.sin(Delta_j)/Eta_j],
                                       [1j*Eta_j*np.sin(Delta_j), np.cos(Delta_j)]])
            CoatMatrix = LayerMatrix_j*CoatMatrix  
        E = CoatMatrix[0,0] + CoatMatrix[0,1]*sEta
        H = CoatMatrix[1,0] + CoatMatrix[1,1]*sEta
        self.rs, self.ts = (iEta*E - H)/(iEta*E + H), 2*iEta/(iEta*E + H)
        
        # for p-polarization
        iEta, sEta = self.iRI/np.cos(self.iTheta), self.sRI/np.cos(self.sTheta)
        m_00, m_01, m_10, m_11 = 1, 0, 0, 1
        for RI_j, Thick_j in zip(self.RI, self.Thick):
            Theta_j = np.arcsin(self.iRI/RI_j)*np.sin(self.iTheta)
            Eta_j = RI_j/np.cos(Theta_j)
            Delta_j = RI_j*Thick_j*np.cos(Theta_j)*2*np.pi/self.Wavelength
            temp00 = m_00*np.cos(Delta_j) + m_01*1j*Eta_j*np.sin(Delta_j)
            temp01 = m_00*1j*np.sin(Delta_j)/Eta_j + m_01*np.cos(Delta_j)
            temp10 = m_10*np.cos(Delta_j) + m_11*1j*Eta_j*np.sin(Delta_j)
            temp11 = m_10*1j*np.sin(Delta_j)/Eta_j + m_11*np.cos(Delta_j)
            m_00, m_01 = np.copy(temp00), np.copy(temp01)
            m_10, m_11 = np.copy(temp10), np.copy(temp11)
        E, H = m_00 + m_01*sEta, m_10 + m_11*sEta
        self.rp, self.tp= (iEta*E - H)/(iEta*E + H), 2*iEta/(iEta*E + H)
        return
                                            
        
        