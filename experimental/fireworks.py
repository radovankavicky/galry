from galry import *
import pylab as plt
import numpy as np
import numpy.random as rdn
import time
import timeit
import os

from OpenGL import GL as gl

class ParticleVisual(Visual):
    def get_position_update_code(self):
        return """
        // update position
        position.x += velocities.x * tloc;
        position.y += velocities.y * tloc - 0.5 * g * tloc * tloc;
        """
        
    def get_color_update_code(self):
        return """
        // pass the color and point size to the fragment shader
        varying_color = color;
        varying_color.w = alpha;
        """
    
    def base_fountain(self, initial_positions=None,
        velocities=None, color=None, alpha=None, delays=None):
        
        self.size = initial_positions.shape[0]
        self.primitive_type = 'POINTS'
        # load texture
        path = os.path.dirname(os.path.realpath(__file__))
        particle = plt.imread(os.path.join(path, "../examples/images/particle.png"))
        
        size = float(max(particle.shape))
        
        # create the dataset
        self.add_uniform("point_size", vartype="float", ndim=1, data=size)
        self.add_uniform("t", vartype="float", ndim=1, data=0.)
        self.add_uniform("color", vartype="float", ndim=4, data=color)
        
        # add the different data buffers
        self.add_attribute("initial_positions", vartype="float", ndim=2, data=initial_positions)
        self.add_attribute("velocities", vartype="float", ndim=2, data=velocities)
        self.add_attribute("delays", vartype="float", ndim=1, data=delays)
        self.add_attribute("alpha", vartype="float", ndim=1, data=alpha)
        
        self.add_varying("varying_color", vartype="float", ndim=4)
        
        # add particle texture
        self.add_texture("tex", size=particle.shape[:2],
            ncomponents=particle.shape[2], ndim=2, data=particle)
            
        vs = """
        // compute local time
        const float tmax = 5.;
        const float tlocmax = 2.;
        const float g = %G_CONSTANT%;
        
        // Local time.
        float tloc = mod(t - delays, tmax);
        
        vec2 position = initial_positions;
        
        if ((tloc >= 0) && (tloc <= tlocmax))
        {
            // position update
            %POSITION_UPDATE%
            
            %COLOR_UPDATE%
        }
        else
        {
            varying_color = vec4(0., 0., 0., 0.);
        }
        
        gl_PointSize = point_size;
        """
            
        vs = vs.replace('%POSITION_UPDATE%', self.get_position_update_code())
        vs = vs.replace('%COLOR_UPDATE%', self.get_color_update_code())
        vs = vs.replace('%G_CONSTANT%', '3.')
            
        # self.add_uniform('cycle', vartype='int', data=0)
            
        self.add_vertex_main(vs)    
        
        self.add_fragment_main(
        """
            vec4 col = texture2D(tex, gl_PointCoord) * varying_color;
            out_color = col;
        """)

    def initialize(self, **kwargs):
        self.base_fountain(**kwargs)

        
        
def update(figure, parameter):
    t = parameter[0]
    # if not hasattr(figure, 'cycle'):
        # figure.cycle = 0
    # figure.cycle = np.mod(figure.cycle + 1, 2)
    # figure.set_data(t=t, cycle=figure.cycle, visual='fountain')
    figure.set_data(t=t, visual='fountain')

if __name__ == '__main__':        
    figure()

    # number of particles
    n = 50000

    # initial positions
    positions = .02 * rdn.randn(n, 2)

    # initial velocities
    velocities = np.zeros((n, 2))
    v = 1.5 + .5 * rdn.rand(n)
    angles = .1 * rdn.randn(n) + np.pi / 2
    velocities[:,0] = v * np.cos(angles)
    velocities[:,1] = v * np.sin(angles)

    # transparency
    alpha = .2 * rdn.rand(n)

    # color
    color = (0.70,0.75,.98,1.)

    # random delays
    delays = 10 * rdn.rand(n)
    
    figure()
            
    # framebuffer(display=False)
    # framebuffer(name='sc', framebuffer=1)
    # imshow(RefVar('sc', 'fbotex0'), #points=(-.5,-.5,.5,.5),
    # # imshow(np.random.rand(4,4,4), points=(-.5,-.5,.5,.5),
        # is_static=True)#, beforeclear=True)
    
    # # create the visual
    visual(ParticleVisual, 
        initial_positions=positions,
        velocities=velocities,
        alpha=alpha,
        color=color,
        delays=delays,
        is_static=True,
        name='fountain',
        )

    # TODO: beginning: copy sc => prev.1
    framebuffer(ntextures=2, coeffs=[1., .9], framebuffer=1)
    framebuffer(name='sc')
        
    # imshow(RefVar('framebuffer', 'fbotex0'), points=(-.5,.5,.5,-.5),
    # # imshow(np.random.rand(4,4,4), points=(-.5,-.5,.5,.5),
        # is_static=True, framebuffer='screen')#, beforeclear=True)
    
    animate(update, dt=.02)

    show()

