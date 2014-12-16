#!/usr/bin/env python
from nose.tools import assert_equal, assert_is
from numpy.testing import assert_almost_equal, assert_array_less
import numpy as np

from poisson import BmiPoisson


def test_component_name():
    model = BmiPoisson()

    name = model.get_component_name()
    assert_equal(name, '2D Poisson Solver')
    assert_is(model.get_component_name(), name)


def test_start_time():
    model = BmiPoisson()
    model.initialize()

    assert_almost_equal(model.get_start_time(), 0.0)


def test_end_time():
    model = BmiPoisson()
    model.initialize()

    assert_almost_equal(model.get_end_time(), np.finfo('d').max)


def test_initialize_defaults():
    model = BmiPoisson()
    model.initialize()

    assert_almost_equal(model.get_current_time(), 0.)
    assert_array_less(model.get_value('land_surface__elevation'), 1.)
    assert_array_less(0., model.get_value('land_surface__elevation'))


def test_initialize_from_file_like():
    from StringIO import StringIO
    import yaml

    config = StringIO(yaml.dump({'shape': (7, 5)}))
    model = BmiPoisson()
    model.initialize(config)

    assert_equal(model.get_grid_shape('land_surface__elevation'), (7, 5))


def test_initialize_from_file():
    import os
    import yaml
    import tempfile

    with tempfile.NamedTemporaryFile('w', delete=False) as fp:
        fp.write(yaml.dump({'shape': (7, 5)}))
        name = fp.name

    model = BmiPoisson()
    model.initialize(name)

    os.remove(name)

    assert_equal(model.get_grid_shape('land_surface__elevation'), (7, 5))


def test_update():
    model = BmiPoisson()
    model.initialize()

    for inc in xrange(10):
        model.update()
        assert_almost_equal(model.get_current_time(),
                            (inc + 1) * model.get_time_step())


def test_update_until():
    model = BmiPoisson()
    model.initialize()

    model.update_until(10.1)
    assert_almost_equal(model.get_current_time(), 10.1)


def test_finalize():
    model = BmiPoisson()
    model.initialize()
    model.update()
    model.finalize()
