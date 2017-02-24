""" Definition of the Paraboloid component, which evaluates the equation
(x-3)^2 + xy + (y+4)^2 = 3
"""
from __future__ import division, print_function
from openmdao.core.explicitcomponent import ExplicitComponent


class Paraboloid(ExplicitComponent):
    """
    Evaluates the equation f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3.
    """

    def initialize_variables(self):
        self.add_input('x', val=0.0)
        self.add_input('y', val=0.0)

        self.add_output('f_xy', val=0.0)

    def compute(self, inputs, outputs):
        """
        f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3

        Optimal solution (minimum): x = 6.6667; y = -7.3333
        """
        x = inputs['x']
        y = inputs['y']

        outputs['f_xy'] = (x-3.0)**2 + x*y + (y+4.0)**2 - 3.0

    def compute_partial_derivs(self, inputs, outputs, partials):
        """
        Jacobian for our paraboloid.
        """
        x = inputs['x']
        y = inputs['y']

        partials['f_xy', 'x'] = 2.0*x - 6.0 + y
        partials['f_xy', 'y'] = 2.0*y + 8.0 + x


if __name__ == "__main__":
    from openmdao.core.problem import Problem
    from openmdao.core.group import Group
    from openmdao.core.indepvarcomp import IndepVarComp

    model = Group()
    model.add_subsystem('des_vars', IndepVarComp((
        ('x', 3.0),
        ('y', -4.0),
    )))
    model.add_subsystem('parab_comp', Paraboloid())

    model.connect('des_vars.x', 'parab_comp.x')
    model.connect('des_vars.y', 'parab_comp.y')

    prob = Problem(model)
    prob.setup()
    prob.run()
    print(prob['parab_comp.f'])

    prob['des_vars.x'] = 5.0
    prob['des_vars.y'] = -2.0
    prob.run()
    print(prob['parab_comp.f'])