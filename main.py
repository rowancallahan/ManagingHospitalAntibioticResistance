''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy import signal
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from bokeh.models.widgets import CheckboxGroup

# Set up data

def LotkaVolterra(state,t, constants):

  x = state[0]
  y = state[1]
  a = constants[0]
  b = constants[1]
  c = constants[2]
  d = constants[3]
  t1 = constants[4]
  t2 = constants[5]
  ab1 = (signal.square(t * t2* np.pi) + 1) / 2
  ab2 = (signal.square((t - 0.5) * t1 * np.pi) + 1) / 2

  xd = a * ab1 - b * y
  yd = c * ab2 - d * x
  return [xd,yd]


t = np.arange(0,500,1)
state0 = [1,0]
constant_value = [0.1,0.005,0.1,0.005,0.02,0.02]
state = odeint(LotkaVolterra, state0, t, args=(constant_value,))
x = state[:,0]
y = state[:,1]
plt.plot(t, x,'r--', t, y, 'g^')


source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="Antibiotic Resistance Prevalence",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 100], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

checkbox_group = CheckboxGroup(
    labels=["Option 1", "Option 2", "Option 3"], active=[0, 1])

x_range = (-20,-10) # could be anything - e.g.(0,1)
y_range = (20,30)
plot2 = figure(x_range=x_range, y_range=y_range)
img_path = 'static/current.jpg'
plot2.image_url(url=[img_path],x=x_range[0],y=y_range[1],w=x_range[1]-x_range[0],h=y_range[1]-y_range[0])




# Set up widgets
text = TextInput(title="title", value='Antibiotic in Use')
a = Slider(title="a", value=0.01, start=0.0, end=0.05, step=0.001)
b = Slider(title="b", value=0.01, start=0.0, end=0.05, step=0.001)
c = Slider(title="c", value=0.01, start=0.0, end=0.05, step=0.001)
d = Slider(title="d", value=0.01, start=0.0, end=0.05, step=0.001)
e = Slider(title="e", value=0.01, start=0.0, end=0.05, step=0.001)
f = Slider(title="f", value=0.01, start=0.0, end=0.05, step=0.001)
checkbox_group = CheckboxGroup(
    labels=["Option 1", "Option 2", "Option 3"], active=[0, 1])

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    a_val = a.value
    b_val = b.value
    c_val = c.value
    d_val = d.value
    e_val = e.value
    f_val = f.value

    # Generate the new curve

    t = np.arange(0, 500, 1)
    state0 = [0.5, 0]
    constant_value = [a_val, b_val, c_val, d_val,e_val,f_val]
    state = odeint(LotkaVolterra, state0, t, (constant_value,))
    x = state[:, 0]
    y = state[:, 1]


    source.data = dict(x=t, y=y)

for w in [a, b, c, d,e,f]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(text, a, b, c, d,e,f, checkbox_group)

curdoc().add_root(row(inputs, plot,plot2, width=800))
curdoc().title = "Sliders"
