![RocketPy Logo](https://raw.githubusercontent.com/RocketPy-Team/RocketPy/master/docs/static/RocketPy_Logo_Black.svg)

<br>

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RocketPy-Team/rocketpy/blob/master/docs/notebooks/getting_started_colab.ipynb)
[![PyPI](https://img.shields.io/pypi/v/rocketpy?color=g)](https://pypi.org/project/rocketpy/)
[![Documentation Status](https://readthedocs.org/projects/rocketpyalpha/badge/?version=latest)](https://docs.rocketpy.org/en/latest/?badge=latest)
[![Build Status](https://app.travis-ci.com/RocketPy-Team/RocketPy.svg?branch=master)](https://app.travis-ci.com/RocketPy-Team/RocketPy)
[![Contributors](https://img.shields.io/github/contributors/RocketPy-Team/rocketpy)](https://github.com/RocketPy-Team/RocketPy/graphs/contributors)
[![Chat on Discord](https://img.shields.io/discord/765037887016140840?logo=discord)](https://discord.gg/b6xYnNh)
[![Sponsor RocketPy](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/RocketPy-Team)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/rocketpy)
[![DOI](https://img.shields.io/badge/DOI-10.1061%2F%28ASCE%29AS.1943--5525.0001331-blue.svg)](http://dx.doi.org/10.1061/%28ASCE%29AS.1943-5525.0001331)

<img src="https://static.scarf.sh/a.png?x-pxid=6f4094ab-00fa-4a8d-9247-b7ed27e7164d" />

# RocketPy

RocketPy is the next-generation trajectory simulation solution for High-Power Rocketry. The code is written as a [Python](http://www.python.org) library and allows for a complete 6 degrees of freedom simulation of a rocket's flight trajectory, including high-fidelity variable mass effects as well as descent under parachutes. Weather conditions, such as wind profiles, can be imported from sophisticated datasets, allowing for realistic scenarios. Furthermore, the implementation facilitates complex simulations, such as multi-stage rockets, design and trajectory optimization and dispersion analysis.

<br>

## Main features

<details>
<summary>Nonlinear 6 degrees of freedom simulations</summary>
<ul>
  <li>Rigorous treatment of mass variation effects</li>
  <li>Solved using LSODA with adjustable error tolerances</li>
  <li>Highly optimized to run fast</li>
</ul>
</details>

<details>
<summary>Accurate weather modeling</summary>
<ul>
  <li>International Standard Atmosphere (1976)</li>
  <li>Custom atmospheric profiles</li>
  <li>Soundings (Wyoming, NOAARuc)</li>
  <li>Weather forecasts and reanalysis</li>
  <li>Weather ensembles</li>
</ul>
</details>

<details>
<summary>Aerodynamic models</summary>
<ul>
  <li>Barrowman equations for lift coefficients (optional)</li>
  <li>Drag coefficients can be easily imported from other sources (e.g. CFD simulations)</li>
</ul>
</details>

<details>
<summary>Parachutes with external trigger functions</summary>
<ul>
  <li>Test the exact code that will fly</li>
  <li>Sensor data can be augmented with noise</li>
</ul>
</details>

<details>
<summary>Solid, Hybrid and Liquid motors models</summary>
<ul>
  <li>Burn rate and mass variation properties from thrust curve</li>
  <li>Define custom rocket tanks based on their flux data</li>
  <li>CSV and ENG file support</li>
</ul>
</details>

<details>
<summary>Monte Carlo simulations</summary>
<ul>
  <li>Dispersion analysis</li>
  <li>Global sensitivity analysis</li>
</ul>
</details>

<details>
<summary>Flexible and modular</summary>
<ul>
  <li>Straightforward engineering analysis (e.g. apogee and lifting off speed as a function of mass)</li>
  <li>Non-standard flights (e.g. parachute drop test from a helicopter)</li>
  <li>Multi-stage rockets</li>
  <li>Custom continuous and discrete control laws</li>
  <li>Create new classes (e.g. other types of motors)</li>
</ul>
</details>

<details>
<summary>Integration with MATLAB®</summary>
<ul>
  <li>Straightforward way to run RocketPy from MATLAB®</li>
  <li>Convert RocketPy results to MATLAB® variables so that they can be processed by MATLAB®</li>
</ul>
</details>

<br>

## Validation

RocketPy's features have been validated in our latest [research article published in the Journal of Aerospace Engineering](http://dx.doi.org/10.1061/%28ASCE%29AS.1943-5525.0001331).

The table below shows a comparison between experimental data and the output from RocketPy.
Flight data and rocket parameters used in this comparison were kindly provided by [EPFL Rocket Team](https://github.com/EPFLRocketTeam) and [Notre Dame Rocket Team](https://ndrocketry.weebly.com/).

|         Mission         |    Result Parameter    | RocketPy  | Measured  | Relative Error  |
|:-----------------------:|:-----------------------|:---------:|:---------:|:---------------:|
|   Bella Lui Kaltbrumn   | Apogee altitude (m)    |   461.03  |   458.97  |   **0.45 %**    |
|   Bella Lui Kaltbrumn   | Apogee time (s)        |    10.61  |    10.56  |   **0.47 %**    |
|   Bella Lui Kaltbrumn   | Maximum velocity (m/s) |    86.18  |    90.00  |   **-4.24 %**   |
|   NDRT launch vehicle   | Apogee altitude (m)    | 1,310.44  | 1,320.37  |   **-0.75 %**   |
|   NDRT launch vehicle   | Apogee time (s)        |    16.77  |    17.10  |   **-1.90 %**   |
|   NDRT launch vehicle   | Maximum velocity (m/s) |   172.86  |   168.95  |   **2.31 %**    |

<br>

## Documentation

Check out documentation details using the links below:

- [User Guide](https://docs.rocketpy.org/en/latest/user/index.html)
- [Code Documentation](https://docs.rocketpy.org/en/latest/reference/index.html)
- [Development Guide](https://docs.rocketpy.org/en/latest/development/index.html)

<br>

# Join Our Community!

RocketPy is growing fast! Many university groups and rocket hobbyists have already started using it. The number of stars and forks for this repository is skyrocketing. And this is all thanks to a great community of users, engineers, developers, marketing specialists, and everyone interested in helping.

If you want to be a part of this and make RocketPy your own, join our [Discord](https://discord.gg/b6xYnNh) server today!

<br>

# Previewing

You can preview RocketPy's main functionalities by browsing through a sample notebook in [Google Colab](https://colab.research.google.com/github/RocketPy-Team/rocketpy/blob/master/docs/notebooks/getting_started_colab.ipynb). No installation is required!

When you are ready to run RocketPy locally, you can read the *Getting Started* section!

<br>

# Getting Started

## Quick Installation

To install RocketPy's latest stable version from PyPI, just open up your terminal and run:

```shell
pip install rocketpy
```

For other installation options, visit our [Installation Docs](https://docs.rocketpy.org/en/latest/user/installation.html).
To learn more about RocketPy's requirements, visit our [Requirements Docs](https://docs.rocketpy.org/en/latest/user/requirements.html).

<br>

## Running Your First Simulation

In order to run your first rocket trajectory simulation using RocketPy, you can start a Jupyter Notebook and navigate to the _docs/notebooks_ folder. Open _getting_started.ipynb_ and you are ready to go.

Otherwise, you may want to create your own script or your own notebook using RocketPy. To do this, let's see how to use RocketPy's four main classes:

- Environment - Keeps data related to weather.
- Motor - Subdivided into SolidMotor, HybridMotor and LiquidMotor. Keeps data related to rocket motors.
- Rocket - Keeps data related to a rocket.
- Flight - Runs the simulation and keeps the results.

The following image shows how the four main classes interact with each other:

![Diagram](https://raw.githubusercontent.com/RocketPy-Team/RocketPy/master/docs/static/Fluxogram-Page-2.svg)

A typical workflow starts with importing these classes from RocketPy:

```python
from rocketpy import Environment, Rocket, SolidMotor, Flight
```

Then create an Environment object. To learn more about it, you can use:

```python
help(Environment)
```

A sample code is:

```python
env = Environment(
    latitude=32.990254,
    longitude=-106.974998,
    elevation=1400,
    date=(2020, 3, 4, 12) # Tomorrow's date in year, month, day, hour UTC format
) 

env.set_atmospheric_model(type='Forecast', file='GFS')
```

This can be followed up by starting a Solid Motor object. To get help on it, just use:

```python
help(SolidMotor)
```

A sample Motor object can be created by the following code:

```python
Pro75M1670 = SolidMotor(
    thrust_source="../data/motors/Cesaroni_M1670.eng",
    burn_time=3.9,
    grain_number=5,
    grain_separation=5/1000,
    grain_density=1815,
    grain_outer_radius=33/1000,
    grain_initial_inner_radius=15/1000,
    grain_initial_height=120/1000,
    grains_center_of_mass_position=-0.85704,
    nozzle_radius=33/1000,
    throat_radius=11/1000,
    interpolation_method='linear'
)
```

With a Solid Motor defined, you are ready to create your Rocket object. As you may have guessed, to get help on it, use:

```python
help(Rocket)
```

A sample code to create a Rocket is:

```python
calisto = Rocket(
    radius=127 / 2000,
    mass=19.197 - 2.956,
    inertia_i=6.60,
    inertia_z=0.0351,
    power_off_drag="../../data/calisto/powerOffDragCurve.csv",
    power_on_drag="../../data/calisto/powerOnDragCurve.csv",
    center_of_dry_mass_position=0,
    coordinate_system_orientation="tail_to_nose"
)
calisto.set_rail_buttons(0.2, -0.5)
calisto.add_motor(Pro75M1670, position=-1.255)
calisto.add_nose(length=0.55829, kind="vonKarman", position=1.278)
calisto.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.040,
    span=0.100,
    position=-1.04956,
    cant_angle=0,
    radius=None,
    airfoil=None
)
calisto.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)
```

You may want to add parachutes to your rocket as well:

```python
def drogue_trigger(p, h, y):
    # p = pressure considering parachute noise signal
    # h = height above ground level considering parachute noise signal
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]

    # activate drogue when vz < 0 m/s.
    return True if y[5] < 0 else False

def main_trigger(p, h, y):
    # p = pressure considering parachute noise signal
    # h = height above ground level considering parachute noise signal
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
        
    # activate main when vz < 0 m/s and z < 800 m
    return True if y[5] < 0 and h < 800 else False

calisto.add_parachute('Main',
                    cd_s=10.0,
                    trigger=main_trigger, 
                    sampling_rate=105,
                    lag=1.5,
                    noise=(0, 8.3, 0.5))

calisto.add_parachute('Drogue',
                      cd_s=1.0,
                      trigger=drogue_trigger, 
                      sampling_rate=105,
                      lag=1.5,
                      noise=(0, 8.3, 0.5))
```

Finally, you can create a Flight object to simulate your trajectory. To get help on the Flight class, use:

```python
help(Flight)
```

To actually create a Flight object, use:

```python
test_flight = Flight(rocket=calisto, environment=env, rail_length=5.2, inclination=85, heading=0)
```

Once the Flight object is created, your simulation is done! Use the following code to get a summary of the results:

```python
test_flight.info()
```

To see all available results, use:

```python
test_flight.all_info()
```

Here is just a quick taste of what RocketPy is able to calculate. There are hundreds of plots and data points computed by RocketPy to enhance your analyses.

![6-DOF Trajectory Plot](https://raw.githubusercontent.com/RocketPy-Team/RocketPy/master/docs/static/rocketpy_example_trajectory.svg)

<br>

# Authors and Contributors

This package was originally created by [Giovani Ceotto](https://github.com/giovaniceotto/) as part of his work at [Projeto Jupiter](https://github.com/Projeto-Jupiter/). [Rodrigo Schmitt](https://github.com/rodrigo-schmitt/) was one of the first contributors.

Later, [Guilherme Fernandes](https://github.com/Gui-FernandesBR/) and [Lucas Azevedo](https://github.com/lucasfourier/) joined the team to work on the expansion and sustainability of this project.

Since then, the [RocketPy Team](https://github.com/orgs/RocketPy-Team/teams/rocketpy-team) has been growing fast and our contributors are what makes us special!

[![GitHub Contributors Image](https://contrib.rocks/image?repo=RocketPy-Team/RocketPy)](https://github.com/RocketPy-Team/RocketPy/contributors)

See a [detailed list of contributors](https://github.com/RocketPy-Team/RocketPy/contributors) who are actively working on RocketPy.

## Supporting RocketPy and Contributing

The easiest way to help RocketPy is to demonstrate your support by starring our repository!
[![starcharts stargazers over time](https://starchart.cc/rocketpy-team/rocketpy.svg)](https://starchart.cc/rocketpy-team/rocketpy)

You can also become a [sponsor](https://github.com/sponsors/RocketPy-Team) and help us financially to keep the project going.

If you are actively using RocketPy in one of your projects, reaching out to our core team via [Discord](https://discord.gg/b6xYnNh) and providing feedback can help improve RocketPy a lot!

And if you are interested in going one step further, please read [CONTRIBUTING.md](https://github.com/RocketPy-Team/RocketPy/blob/master/CONTRIBUTING.md) for details on our code of conduct and learn more about how you can contribute to the development of this next-gen trajectory simulation solution for rocketry.

<br>

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/RocketPy-Team/RocketPy/blob/master/LICENSE) file for details

<br>

## Release Notes

Want to know which bugs have been fixed and the new features of each version? Check out the [release notes](https://github.com/RocketPy-Team/RocketPy/releases).
