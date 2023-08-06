=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format follows the recommendations of
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_, and adapts the
markup language to use reStructuredText.

This projects adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


Unreleased_
===========


1.0_ -- 2022-11-20
==================

Added
-----

- [code] The produced SVG now defines a view box.

Changed
-------

- [packaging] The project's repository has been relocated under the cate/ group
  of the Inrias GitLab instance.

Fixed
-----

- [bug] The depictions of the stretching phase and the complete flow were
  lacking a background.
- [bug] The depiction of torsions now respects the sign convention.


1.0b0_ -- 2019-01-04
====================

Added
-----

- [code] ``core.Template`` class is now the interface to manipulate templates.
- [code] ``core.convert_order_position`` to convert an order vector into a
  position vector, and vice-versa.
- [code] ``export`` module to manage supported export formats.
- [code] New external dependency ``multiset``.

Changed
-------

- [code] Complete rewrite of the optimization logic to compute of a
  depth-optimal sequence of crossings.
- [code] Complete refactor of the SVG export code.
- [code] Public namespaces of each module have been cleaned of all unnecessary
  objects.

- [doc] Improve README.

Removed
-------

- [code] Legacy optimization logic of ``main`` module:
    - ``all_subsets``, ``createTree``, ``detectDoubles``, ``getNeighbours``,
      ``getPermutations``, ``getTorsions``, ``updatePermutationList`` and
      ``updatePosition`` functions.
    - ``Node`` and ``Tree`` classes.
- [code] Legacy drawing logic: ``drawTemplate`` module and
  ``main.drawSVGTemplate`` function.

Fixed
-----

- [bug] float parsing for scale argument in CLI.


0.0.1 -- 2018-07-27
===================

Added
-----

- [code] CLI interface.
- [code] Validation logic for linking matrix.
- [code] Optimization logic to minimize template height.
- [code] SVG drawing logic.

- [doc] Example input matrices: elementary matrices of size 5 and 6.


.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. links to git diffs

.. _Unreleased: https://gitlab.inria.fr/cate/cate/compare/v1.0...master
.. _1.0: https://gitlab.inria.fr/cate/cate/compare/v1.0b0...v1.0
.. _1.0b0: https://gitlab.inria.fr/cate/cate/compare/v0.0.1...v1.0b0
