Synthesise data (2D or Healpix) using Cross Scattering Transform (https://arxiv.org/abs/2207.12527) usable for component separation (e.g. denoising).

1. startup

To generate test files run the follosing lines inside python::

   >import foscat.build_demo as dem
   >dem.genDemo()
   >quit()

2. run 2D test::

   >python test2D.py

to plot the corresponding results::

   >python test2Dplot.py

3. run spherical test::

   >python testHealpix.py

to plot the corresponding results::

   >python testHplot.py

Note: If mpi is available you can run testHealpix_mpi.py that uses 3 nodes to do the same computation than testHealpix.py.
