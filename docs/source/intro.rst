Introduction
============
Goal of this package is to provide an easy to use API for event-based evaluations in activity recognition problems.

As pointed out by :cite:`ward2011performance`, standard precision and recall values aren't sufficient to describe the nature of the
errors in a dataset. Therefore the authors introduced new categories, metrics and visualisations for event-based evaluations.

The package implements the methods proposed by :cite:`ward2011performance` beside the typical precision and recall calculations.
We provide also useful functions to interface with other modules of your activity recognition workflow and visualisation tools in the package.

Installation
------------
Easiest way is to install it with pip (command line)::

    pip install ward-metrics

To update to the latest version you can call (command line)::

    pip install ward-metrics --upgrade


To import the packege in the project your can simply write::

    import wardmetrics

The package is currently only tested with python 3 (>=3.3).

For adapting the package to your needs, checkout the our `Github repository`__.

.. _repo: https://github.com/phev8/ward-metrics

__ repo_

References
----------
.. bibliography:: references.bib
