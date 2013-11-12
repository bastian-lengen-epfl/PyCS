"""
Wrapper around scikit-learn's GPR 
"""

from sklearn.gaussian_process import GaussianProcess
import numpy as np


def regression(x, y, yerr, verbose=True):
	"""
	Give me data points
	yerr is the 1sigma error of each y
	I return a function : you pass an array of new x, the func returns (newy, newyerr)
	"""
	x = np.atleast_2d(x).T
	
#	gp = GaussianProcess(corr='squared_exponential',
#		theta0=1.0, thetaL=1e-2, thetaU=1e2, nugget = (yerr)**2,
#		random_start=100, verbose=verbose)
	
	
	gp = GaussianProcess(corr='squared_exponential',
		theta0=100.0, random_start=1, nugget = 0.001, verbose=verbose)

	gp.fit(x, y)
	
	#print gp

	def outfct(xgrid):
	
		ygrid, MSE = gp.predict(np.atleast_2d(xgrid).T, eval_MSE=True)
		sigmas = np.sqrt(MSE)
		return (ygrid, sigmas)
	
	return outfct


