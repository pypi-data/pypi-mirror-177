#%%
import numpy as np


class SDOF_system():
    def __init__(self, m:float, k:float, c:float= 0):
        self.m = m
        self.k = k
        self.c = c
        self.__params__()

    def __params__(self):
        self.wn = np.sqrt(self.k/self.m)
        self.zeta = self.c/(2*self.m*self.wn)
        self.wd = self.wn *np.sqrt(1-self.zeta**2)
        self.delta = log_decrement(self.zeta) # logaritmic decretemnt
        
        self.T = (2*np.pi)/self.wn # period no damping
        self.Td = (2*np.pi)/self.wd # damping period

    def c_crit(self):
        return 2 * self.m*self.wn

    def amplitude(self, x0, v0):
        ''' amplitude for free under-damped vibrations

        representing the solution $X0*np.exo(-zeta*wn*t)*np.sin(wd*t + phi)$

        From RAO  eq. 2.73, eq.2.74
        return np.sqrt((x0*self.wn)**2 + (v0)**2 + 2*x0*v0*self.zeta*self.wn)/self.wd
        '''
        
        return np.sqrt(x0**2 + ( (v0 + x0*self.zeta*self.wn )/self.wd)**2)

    def phase(self, x0, v0):
        ''' Phase $phi$ for free under-damped vibrations

        representing the solution $X0*np.exo(-zeta*wn*t)*np.cos(wd*t - phi)$

        From RAO  eq. 2.73, eq.2.74
        '''
        
        # wn = self.wn
        # wd = self.wd
        return np.arctan2(v0+self.zeta*self.wn*x0,x0 *self.wd) 

    def free_response_at_t(self, t:np.array, x0:float, v0:float)->dict:
        """returns the free response at a specific time.

        Args:
            t (float): time in s
            x0 (float): position at t=0
            v0 (float): velocity at t=0

        Returns:
            dict: [description]
        """        
        #TODO: complete this
        A = self.amplitude(x0,v0)
        phi = self.phase(x0,v0)

        
        if self.zeta<1:
            # Ae^{-zeta \omega_n t}\cos(\omega_d t + \phi)\) 
            xs = A*np.exp(-self.zeta*self.wn*t)*np.cos(self.wd*t - phi)
            vs = -(np.cos(self.wd*t -phi)*self.wn*self.zeta + self.wd*np.sin(self.wd*t - phi) ) *A*np.exp(-self.zeta*self.wn*t)
            
        else:
            raise (Exception('Not implemented yet'))
        
        return {'t':t, 'xs':xs,'vs':vs}



    def free_response_at_t_funcs(self, x0:float, v0:float)->dict:
        """returns the free response function 

        Args:
            t (float): time in s
            x0 (float): position at t=0
            v0 (float): velocity at t=0

        Returns:
            dict: [description]
        """        
        #TODO: complete this
        A = self.amplitude(x0,v0)
        phi = self.phase(x0,v0)

        
        if self.zeta<1:
            # Ae^{-zeta \omega_n t}\cos(\omega_d t + \phi)\) 
            xf = lambda t: A*np.exp(-self.zeta*self.wn*t)*np.cos(self.wd*t - phi)
            vf = lambda t: -(np.cos(self.wd*t - phi)*self.wn*self.zeta + self.wd*np.sin(self.wd*t -phi) ) *A*np.exp(-self.zeta*self.wn*t)
            
        else:
            raise (Exception('Not implemented yet'))
        
        return {'x':xf,'v':vf}

    @classmethod
    def from_zeta(cls, zeta:float, m, k):
        return cls(m=m, k=k, c=2*zeta*np.sqrt(m*k))

    @classmethod
    def from_wn_kc(cls, wn:float, k:float, c:float):
        return cls(m=k/wn**2, k=k, c=c)

    @classmethod
    def from_wn_mc(cls, wn:float, m:float, c:float):
        return cls(m=m, k=m*wn**2, c=c)

    @classmethod
    def from_wn_mz(cls, wn:float, m:float, zeta:float):
        return cls(m=m, k=m*wn**2, c=2*zeta*m*wn)

    @classmethod
    def from_wn_kz(cls, wn:float, k:float, zeta:float):
        return cls(m=k/wn**2, k=k, c=2*zeta*wn/k)

def log_decrement(zeta):
    return (2*np.pi*zeta)/np.sqrt(1-zeta**2)


def zeta_from_log_decrement(delta):
    ''' Calculation of zeta based on logarithmic decrement

    require delta in log(X_{i+1}/X_{i})
    '''
    return delta/np.sqrt(4*np.pi**2 +delta**2)

def M(r, zeta):
    ''' Magnification factor
    '''
    return np.sqrt( 1/((1-r**2)**2+ (2*r*zeta)**2) )

def M_peak(zeta):
    ''' Magnification factor
    '''
    return 1/(2*zeta*np.sqrt( 1-zeta**2 ))

def r_Mpeak(zeta):
    ''' r where maximum Magnification factor occurs
    '''
    return np.sqrt( 1-2*zeta**2 )


def trans_ratio(r, zeta):
    ''' Transmissability ratio
    '''
    return np.sqrt( (1+ (2*r*zeta)**2)/((1-r**2)**2+ (2*r*zeta)**2) )

if __name__ == "__main__":
    rs= np.linspace(0,1,10)
    print(trans_ratio(rs, 0.1))
# %%
