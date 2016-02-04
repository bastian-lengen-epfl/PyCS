Getting time delay histograms
=============================



Generalities
------------

To obtain time delay histograms or PDFs, several steps need to be done; they are presented in the following subsections.
We assume that you have generated some mock curves as described in the previous section.



Run curve shifting algorithms on the mock curves
------------------------------------------------


The wrapper function to run any method on any set of mock curves has the funny name :py:func:`pycs.sim.run.multirun`.
As input, it takes those pkl files containing simulated curves, made in the previous section. The ouput of this step are pkl files of runresult objects.

One important argument of ``multirun`` is ``tsrand``. It is the radius (in days) of a uniform randomization of the input time shifts.

.. note:: Something nice : you can launch several identical "calls" to this multirun function (for instance simply by launching your script on several CPUs), and this will indeed process the pkl files in parallel. For this to work, the ``multirun`` function stores a temporary file in its results directory as soon as it starts working on a pickle file, so that other scripts know that they should not run on this same pkl file as well. You can see those temporary files, of course. If something goes wrong and they don't get deleted automatically as the scirpt crashed, you might have to remove them by hand, otherwise ``multirun`` will just skip those pkl files.

Here is an example script running all 3 methods. We assume that you've defined your favorite optimizers in ``myopt.py``.


::
	
	lcs = pycs.gen.util.readpickle("merged.pkl")

	
	# Spline method
	"""
	
	# Initial conditions for the analysis :
	# (You might want to set some timeshifts, fluxshifts, as well)
	# In this case we'll just add some spline ML :
	pycs.gen.splml.addtolc(lcs[0], knotstep=100)
	pycs.gen.splml.addtolc(lcs[2], knotstep=300)
	pycs.gen.splml.addtolc(lcs[3], knotstep=300)
	
	#pycs.sim.run.multirun("copies", lcs, myopt.spl, optset="spl1", tsrand=10.0)
	#pycs.sim.run.multirun("sim1tsr5", lcs, myopt.spl, optset="spl1", tsrand=10.0)
	"""
	
	
	# Disp method
	"""
	# We set up some polynomial ML :
	pycs.gen.polyml.addtolc(lcs[0], nparams=3, autoseasonsgap = 60.0)
	pycs.gen.polyml.addtolc(lcs[2], nparams=4, autoseasonsgap = 1000.0)
	pycs.gen.polyml.addtolc(lcs[3], nparams=4, autoseasonsgap = 1000.0)
	
	#myopt.disp(lcs)
	#pycs.gen.lc.display(lcs)
	
	#pycs.sim.run.multirun("copies", lcs, myopt.disp, optset="disp1", tsrand=10.0)
	#pycs.sim.run.multirun("sim1tsr5", lcs, myopt.disp, optset="disp1", tsrand=10.0)
	"""
	
	
	# Regdiff method
	"""
	# No need for ml, but time delays should be set about right.
	
	#pycs.sim.run.multirun("copies", lcs, myopt.regdiff, optset="regdiff2", tsrand=10.0)
	#pycs.sim.run.multirun("sim1tsr5", lcs, myopt.regdiff, optset="regdiff2", tsrand=10.0)
	"""
	



Analysing the measurement results
---------------------------------


We read the "runresults" pickle files created at the previous step, and turn them into plots.
This is very flexible, as you might want to plot and analyse many things.

For now, here is a typical example of the kind of plots we're after :

::

		
	copiesres = [
		pycs.sim.run.collect("sims_copies_opt_disp1", "red", "Dispersion"),
		pycs.sim.run.collect("sims_copies_opt_spl1", "blue", "Spline"),
		pycs.sim.run.collect("sims_copies_opt_regdiff1", "green", "Regdiff")
	]
	
	pycs.sim.plot.hists(copiesres, r=30.0, nbins=100)
	
	
	simres = [
		pycs.sim.run.collect("sims_sim1tsr5_opt_disp1", "red", "Dispersion"),
		pycs.sim.run.collect("sims_sim1tsr5_opt_spl1", "blue", "Splines"),
		pycs.sim.run.collect("sims_sim1tsr5_opt_regdiff1", "green", "Regdiff")
	]
	
	
	pycs.sim.plot.hists(simres, r=30.0, nbins=100)
	
	pycs.sim.plot.measvstrue(simres, r=5.0, nbins = 10, plotpoints=True, ploterrorbars=True, sidebyside=True, errorrange=8, binclip=False, binclipr=20.0)
	
	pycs.sim.plot.delayplot(copiesres, simres, rplot=30.0, rbins=5.0, nbins = 10, binclipr=100.0, displaytext=True, total=False)
	
	
	
	


	