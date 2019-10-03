from brian2 import *
import matplotlib.pyplot as plt
import sys
map_size = 100
global foodx, foody, bugtrapx, bugtrapy, food_count, bug_plot, food_plot, sr_plot, sl_plot, sri_plot, sli_plot,outbugx,outbugy,outbugang,outfoodx,outfoody,outbugtrapx,outbugtrapy,outsrx,outsry,outslx,outsly,outsrix,outsriy,outslix,outsliy

food_count = 0
bugtrap_count = 0
foodx=50
foody=50
bugtrapx=30
bugtrapy=30
duration=2000
outbugx=np.zeros(int(duration/2))
outbugy=np.zeros(int(duration/2))
outbugang=np.zeros(int(duration/2))
outfoodx=np.zeros(int(duration/2))
outfoody=np.zeros(int(duration/2))
outbugtrapx=np.zeros(int(duration/2))
outbugtrapy=np.zeros(int(duration/2))
outsrx=np.zeros(int(duration/2))
outsry=np.zeros(int(duration/2))
outslx=np.zeros(int(duration/2))
outsly=np.zeros(int(duration/2))
outsrix=np.zeros(int(duration/2))
outsriy=np.zeros(int(duration/2))
outslix=np.zeros(int(duration/2))
outsliy=np.zeros(int(duration/2))

# Sensor neurons
a = 0.02
b = 0.2
c = -65
d = 0.5

Eex = 50 #for excitatory synapse
Ein = -70 #for inhibitory synapse
I0e = 1000
tau_ampae=1.0*ms
g_synpke=1
g_synmaxvale=(g_synpke/(tau_ampae/ms*exp(-1)))

I0i = 200
tau_ampai=1.0*ms
g_synpki=0.3
g_synmaxvali=(g_synpki/(tau_ampai/ms*exp(-1)))

sensor_eqs = '''
dv/dt = ((0.04*v**2)+(5*v)+(140)-(u)+I+(ge*(Eex-v))+(gi*(Ein-v)))/ms : 1
du/dt = (a*(b*v-u))/ms : 1

dze/dt = -ze/tau_ampae : 1
dge/dt = -ge/tau_ampae + ze/ms : 1

dzi/dt = -zi/tau_ampai : 1
dgi/dt = -gi/tau_ampai + zi/ms : 1

I = 2.2*mag*I0e / sqrt(((x-foodxx)**2+(y-foodyy)**2)) + magtrap*I0i / sqrt(((x-bugtrapxx)**2+(y-bugtrapyy)**2))*1.3 : 1

x : 1
y : 1
x_disp : 1
y_disp : 1
foodxx : 1
foodyy : 1
bugtrapxx : 1
bugtrapyy : 1
mag :1
magtrap :1
'''

sensor_reset = '''
v = c
u = u + d
'''

# creates 4 sensor neurons (2 for food aggressor, 2 for bug trap avoider) and 2 motor neurons
# for food aggressor, only the magnitude of I associated with euclidean distance from food source is taken into account
# for bug trap avoider, only the magnitude of I associated with euclidean distance from bug trap is taken into account


sre = NeuronGroup(1, sensor_eqs, clock=Clock(0.2*ms), threshold = "v>=30", reset = sensor_reset,method='euler')
sre.v = c
sre.u = c*b
sre.x_disp = 5
sre.y_disp = 5
sre.x = sre.x_disp
sre.y = sre.y_disp
sre.foodxx = foodx
sre.foodyy = foody
sre.bugtrapxx = bugtrapx
sre.bugtrapyy = bugtrapy
sre.mag=1
sre.magtrap=0

sri = NeuronGroup(1, sensor_eqs, clock=Clock(0.2*ms), threshold = "v>=30", reset = sensor_reset,method='euler')
sri.v = c
sri.u = c*b
sri.x_disp = 5
sri.y_disp = 5
sri.x = sri.x_disp
sri.y = sri.y_disp
sri.foodxx = foodx
sri.foodyy = foody
sri.bugtrapxx = bugtrapx
sri.bugtrapyy = bugtrapy
sri.mag=0
sri.magtrap=1

sle = NeuronGroup(1, sensor_eqs, clock=Clock(0.2*ms), threshold = "v>=30", reset = sensor_reset,method='euler')
sle.v = c
sle.u = c*b
sle.x_disp = -5
sle.y_disp = 5
sle.x = sle.x_disp
sle.y = sle.y_disp
sle.foodxx = foodx
sle.foodyy = foody
sle.bugtrapxx = bugtrapx
sle.bugtrapyy = bugtrapy
sle.mag=1
sle.magtrap=0

sli = NeuronGroup(1, sensor_eqs, clock=Clock(0.2*ms), threshold = "v>=30", reset = sensor_reset,method='euler')
sli.v = c
sli.u = c*b
sli.x_disp = -5
sli.y_disp = 5
sli.x = sli.x_disp
sli.y = sli.y_disp
sli.foodxx = foodx
sli.foodyy = foody
sli.bugtrapxx = bugtrapx
sli.bugtrapyy = bugtrapy
sli.mag=0
sli.magtrap=1

sbr = NeuronGroup(1, sensor_eqs, clock=Clock(0.2*ms), threshold = "v>=30", reset = sensor_reset,method='euler')
sbr.v = c
sbr.u = c*b
sbr.foodxx = foodx
sbr.foodyy = foody
sbr.bugtrapxx = bugtrapx
sbr.bugtrapyy = bugtrapy
sbr.mag=0
sbr.magtrap=0

sbl = NeuronGroup(1, sensor_eqs, clock=Clock(0.2*ms), threshold = "v>=30", reset = sensor_reset,method='euler')
sbl.v = c
sbl.u = c*b
sbl.foodxx = foodx
sbl.foodyy = foody
sbl.bugtrapxx = bugtrapx
sbl.bugtrapyy = bugtrapy
sbl.mag=0
sbl.magtrap=0


# The virtual bug

taum = 4*ms
base_speed = 9.5
turn_rate = 5*Hz
L = 1 # distance between virtual wheels

bug_eqs = '''
#equations for movement here
dx/dt = 20*speed*cos(angle)/second : 1
dy/dt = 20*speed*sin(angle)/second : 1
speed = (motorl+motorr)/2 + base_speed: 1
dangle/dt = turn_rate*(motorr-motorl)/L : 1
dmotorl/dt = -motorl/taum: 1
dmotorr/dt = -motorr/taum: 1
'''

#motorl,r = velocity
bug = NeuronGroup(1, bug_eqs, clock=Clock(0.2*ms),method='euler')
bug.motorl = 0
bug.motorr = 0
bug.angle = pi/2
bug.x = 0
bug.y = 0

# Synapses (sensors communicate with bug motor)
# excitatory synapses from food aggressor sensors to contralateral motors
# excitatory synapses from bug trap avoider sensors to ipsilateral motors
# inhibitory synapses from bug trap avoider sensors to food aggressor sensors

w = 10 # eta
syn_rre=Synapses(sre, sbl, clock=Clock(0.2*ms), model='''
                g_synmax:1
                ''',
		on_pre='''
		ze+= g_synmax
		''')

syn_rre.connect(i=[0],j=[0])
syn_rre.g_synmax=g_synmaxvale

syn_rri=Synapses(sri, sbr, clock=Clock(0.2*ms), model='''
                g_synmax:1
                ''',
		on_pre='''
		ze+= g_synmax
		''')

syn_rri.connect(i=[0],j=[0])
syn_rri.g_synmax=g_synmaxvale

syn_lle=Synapses(sle, sbr, clock=Clock(0.2*ms), model='''
                g_synmax:1
                ''',
		on_pre='''
		ze+= g_synmax
		''')

syn_lle.connect(i=[0],j=[0])
syn_lle.g_synmax=g_synmaxvale

syn_lli=Synapses(sli, sbl, clock=Clock(0.2*ms), model='''
                g_synmax:1
                ''',
		on_pre='''
		ze+= g_synmax
		''')

syn_lli.connect(i=[0],j=[0])
syn_lli.g_synmax=g_synmaxvale

syn_llIN = Synapses(sli, sle, clock=Clock(0.2*ms), model='''
                g_synmax:1
                ''',
		on_pre='''
		zi += g_synmax
		''')

syn_llIN.connect(i=[0],j=[0])
syn_llIN.g_synmax=g_synmaxvali

syn_rrIN = Synapses(sri, sre, clock=Clock(0.2*ms), model='''
                g_synmax:1
                ''',
		on_pre='''
		zi += g_synmax
		''')

syn_rrIN.connect(i=[0],j=[0])
syn_rrIN.g_synmax=g_synmaxvali

syn_r = Synapses(sbr, bug, clock=Clock(0.2*ms), on_pre='motorr += w')
syn_r.connect(i=[0],j=[0])
syn_l = Synapses(sbl, bug, clock=Clock(0.2*ms), on_pre='motorl += w')
syn_l.connect(i=[0],j=[0])

f = figure(1)
bug_plot = plot(bug.x, bug.y, 'ko')
food_plot = plot(foodx, foody, 'b*')
bugtrap_plot = plot(bugtrapx, bugtrapy, 'rX',markersize=30)
sr_plot = plot([0], [0], 'w')
sl_plot = plot([0], [0], 'w')
sri_plot = plot([0], [0], 'w')   # also adds sensor antennas for bug trap avoiding
sli_plot = plot([0], [0], 'w')

@network_operation()
def update_positions():
    global foodx, foody, food_count, bugtrapx, bugtrapy, bugtrap_count
    sre.x = bug.x + sre.x_disp*sin(bug.angle)+ sre.y_disp*cos(bug.angle)
    sre.y = bug.y + - sre.x_disp*cos(bug.angle) + sre.y_disp*sin(bug.angle)

    sle.x = bug.x +  sle.x_disp*sin(bug.angle)+sle.y_disp*cos(bug.angle)
    sle.y = bug.y  - sle.x_disp*cos(bug.angle)+sle.y_disp*sin(bug.angle)

    sri.x = bug.x + sri.x_disp*sin(bug.angle)+ sri.y_disp*cos(bug.angle)
    sri.y = bug.y + - sri.x_disp*cos(bug.angle) + sri.y_disp*sin(bug.angle)

    sli.x = bug.x +  sli.x_disp*sin(bug.angle)+sli.y_disp*cos(bug.angle)
    sli.y = bug.y  - sli.x_disp*cos(bug.angle)+sli.y_disp*sin(bug.angle)

    if ((bug.x-foodx)**2+(bug.y-foody)**2) < 16:
        food_count += 1
        foodx = randint(-map_size+10, map_size-10)
        foody = randint(-map_size+10, map_size-10)

        bug.motorl = 0 # prevents any potential glitches by resetting each motor
        bug.motorr = 0

        bugtrap_count += 1          # whenever another food is generated, another bugtrap is generated
        bugtrapx = randint(-map_size+10, map_size-10)
        bugtrapy = randint(-map_size+10, map_size-10)

    if ((bug.x-bugtrapx)**2+(bug.y-bugtrapy)**2) < 16: # if bug hits a bugtrap, it dies and ends the simulation
        title('BUG TRAPPED! Food Eaten: %i' %food_count) # shows number of food eaten
        plt.plot(MB.x[0], MB.y[0]) # plots path
        sys.exit()

    if (bug.x < -map_size):
        bug.x = -map_size
        bug.angle = pi - bug.angle
    if (bug.x > map_size):
	bug.x = map_size
	bug.angle = pi - bug.angle
    if (bug.y < -map_size):
	bug.y = -map_size
	bug.angle = -bug.angle
    if (bug.y > map_size):
	bug.y = map_size
	bug.angle = -bug.angle

    sre.foodxx = foodx
    sre.foodyy = foody
    sle.foodxx = foodx
    sle.foodyy = foody

    sri.bugtrapxx = bugtrapx
    sri.bugtrapyy = bugtrapy
    sli.bugtrapxx = bugtrapx
    sli.bugtrapyy = bugtrapy

@network_operation(dt=2*ms)
def update_plot(t):
    global foodx, foody, bugtrapx, bugtrapy, bug_plot, food_plot, bugtrap_plot, sr_plot, sl_plot,sri_plot, sli_plot,outbugx,outbugy,outbugang,outfoodx,outfoody,outbugtrapx,outbugtrapy,outsrx,outsry,outslx,outsly,outsrix,outsriy,outslix,outsliy
    indx=int(.5*t/ms+1)
    bug_plot[0].remove()
    food_plot[0].remove()
    bugtrap_plot[0].remove()
    sr_plot[0].remove()
    sl_plot[0].remove()
    sri_plot[0].remove()
    sli_plot[0].remove()
    bug_x_coords = [bug.x, bug.x-4*cos(bug.angle), bug.x-8*cos(bug.angle)]    # bug body
    bug_y_coords = [bug.y, bug.y-4*sin(bug.angle), bug.y-8*sin(bug.angle)]
    outbugx[indx-1]=bug.x[0]
    outbugy[indx-1]=bug.y[0]
    outbugang[indx-1]=bug.angle[0]
    outfoodx[indx-1]=foodx
    outfoody[indx-1]=foody
    outbugtrapx[indx-1]=bugtrapx
    outbugtrapy[indx-1]=bugtrapy
    outsrx[indx-1]=sre.x[0]
    outsry[indx-1]=sre.y[0]
    outslx[indx-1]=sle.x[0]
    outsly[indx-1]=sle.y[0]
    outsrix[indx-1]=sri.x[0]
    outsriy[indx-1]=sri.y[0]
    outslix[indx-1]=sli.x[0]
    outsliy[indx-1]=sli.y[0]
    bug_plot = plot(bug_x_coords, bug_y_coords, 'ko')     # bug's current position
    sr_plot = plot([bug.x, sre.x], [bug.y, sre.y], 'b')
    sl_plot = plot([bug.x, sle.x], [bug.y, sle.y], 'r')
    sri_plot = plot([bug.x-8*cos(bug.angle), sri.x-8*cos(bug.angle)], [bug.y-8*sin(bug.angle), sri.y-8*sin(bug.angle)], 'y') # antennas to the bug body
    sli_plot = plot([bug.x-8*cos(bug.angle), sli.x-8*cos(bug.angle)], [bug.y-8*sin(bug.angle), sli.y-8*sin(bug.angle)], 'g')
    food_plot = plot(foodx, foody, 'b*')
    bugtrap_plot = plot(bugtrapx, bugtrapy, 'rX',markersize=30)
    axis([-100,100,-100,100])
    title('R&B = Food Aggressor Sensor, Y&G = Trap Avoider Sensor')
    draw()
    pause(0.01)

MB = StateMonitor(bug, ('motorl', 'motorr', 'speed', 'angle', 'x', 'y'), record = True)
run(duration*ms,report='text')
np.save('outbugx',outbugx)
np.save('outbugy',outbugy)
np.save('outbugang',outbugang)
np.save('outfoodx',outfoodx)
np.save('outfoody',outfoody)
np.save('outbugtrapx',outfoodx)
np.save('outbugtrapy',outfoody)
np.save('outsrx',outsrx)
np.save('outsry',outsry)
np.save('outslx',outslx)
np.save('outsly',outsly)

plt.clf()
plt.plot(MB.x[0], MB.y[0], 'k')
plt.plot(foodx, foody, 'b*')
plt.plot(bugtrapx, bugtrapy, 'rX',markersize=30)
axis([-100,100,-100,100])
title('Food Eaten: %i, Traps Avoided: %i' %(food_count,bugtrap_count)) # when simulation ends, plots path and reports food eaten and bug traps avoided
