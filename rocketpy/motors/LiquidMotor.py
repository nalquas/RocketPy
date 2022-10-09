# -*- coding: utf-8 -*-

__author__ = "Giovani Hidalgo Ceotto, Oscar Mauricio Prada Ramirez, João Lemes Gribel Soares, Mateus Stano and Pedro Henrique Marinho Bressan"
__copyright__ = "Copyright 20XX, RocketPy Team"
__license__ = "MIT"

from abc import ABC, abstractmethod
import functools

import numpy as np
from scipy import integrate

from rocketpy.Function import Function
from rocketpy.motors import Motor
from rocketpy.supplement import Disk, Cylinder, Hemisphere


class LiquidMotor(Motor):
    def __init__(
        self,
        thrustSource,
        burnOut,
        nozzleRadius,
        throatRadius,
        reshapeThrustCurve=False,
        interpolationMethod="linear",
    ):

        super.__init__()
        self.tanks = []
        pass

    def evaluateMassFlowRate(self):
        massFlowRate = 0

        for tank in self.tanks:
            massFlowRate += tank.get("tank").netMassFlowRate

        return massFlowRate

    def evaluateCenterOfMass(self):
        totalMass = 0
        massBalance = 0

        for tankElement in self.tanks:
            tank = tankElement.get("tank")
            tankPosition = tankElement.get("position")
            totalMass += tank.mass
            massBalance += tank.mass * (tankPosition + tank.centerOfMass)

        return massBalance / totalMass

    def evaluateInertiaTensor(self):
        pass

    def addTank(self, tank, position):
        self.tanks.append({"tank": tank, "position": position})


class Tank(ABC):
    def __init__(
        self, name, diameter, height, gas, liquid=0, bottomCap="flat", upperCap="flat"
    ):
        self.name = name
        self.diameter = diameter
        self.height = height
        self.gas = gas
        self.liquid = liquid
        self.bottomCap = bottomCap
        self.upperCap = upperCap

        self.capMap = {
            "flat": Disk,
            "spherical": Hemisphere,
        }
        self.setTankGeometry()

        pass

    def setTankGeometry(self):
        self.cylinder = Cylinder(self.diameter / 2, self.height)
        self.bottomCap = self.capMap.get(self.bottomCap)(
            self.diameter / 2, fill_direction="upwards"
        )
        self.upperCap = self.capMap.get(self.upperCap)(
            self.diameter / 2, fill_direction="downwards"
        )

    def setTankFilling(self, t):
        liquidVolume = self.liquidVolume.getValueOpt(t)

        if liquidVolume < self.bottomCap.volume:
            self.bottomCap.filled_volume = liquidVolume
            self.cylinder.filled_volume = 0
            self.upperCap.filled_volume = 0
        elif liquidVolume <= self.bottomCap.volume + self.cylinder.volume:
            self.bottomCap.filled_volume = self.bottomCap.volume
            self.cylinder.filled_volume = liquidVolume - self.bottomCap.volume
            self.upperCap.filled_volume = 0
        elif (
            liquidVolume
            <= self.bottomCap.volume + self.cylinder.volume + self.upperCap.volume
        ):
            self.bottomCap.filled_volume = self.bottomCap.volume
            self.cylinder.filled_volume = self.cylinder.volume
            self.upperCap.filled_volume = liquidVolume - (
                self.bottomCap.volume + self.cylinder.volume
            )
        else:
            raise ValueError(
                "Tank is overfilled. Check input data to make sure it is correct."
            )

    @abstractmethod
    def mass(self):
        """Returns the total mass of liquid and gases inside the tank as a
        function of time.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        Function
            Mass of the tank as a function of time. Units in kg.
        """
        pass

    @abstractmethod
    def netMassFlowRate(self):
        """Returns the net mass flow rate of the tank as a function of time.
        Net mass flow rate is the mass flow rate entering the tank minus the
        mass flow rate exiting the tank, including liquids and gases. Positive
        is defined as a net mass flow rate entering the tank.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        Function
            Net mass flow rate of the tank as a function of time.
            Positive is defined as a net mass flow rate entering the tank.
        """
        pass

    @abstractmethod
    def liquidVolume(self):
        """Returns the volume of liquid inside the tank as a function
        of time.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        Function
            Tank's liquid volume as a function of time.
        """
        pass

    def centerOfMass(self, t):
        """Returns the center of mass of the tank's fluids as a function of
        time.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        Function
            Center of mass of the tank's fluids as a function of time.
        """
        self.setTankFilling(t)

        bottomCapMass = self.liquid.density * self.bottomCap.filled_volume
        cylinderMass = self.liquid.density * self.cylinder.filled_volume
        upperCapMass = self.liquid.density * self.upperCap.filled_volume

        centerOfMass = (
            self.bottomCap.filled_centroid * bottomCapMass
            + self.cylinder.filled_centroid * cylinderMass
            + self.upperCap.filled_centroid * upperCapMass
        ) / (bottomCapMass + cylinderMass + upperCapMass)

        return centerOfMass

    def inertiaTensor(self, t):
        """Returns the inertia tensor of the tank's fluids as a function of
        time.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        Function
            Inertia tensor of the tank's fluids as a function of time.
        """
        # TODO: compute inertia for non flat caps
        self.setTankFilling(t)

        cylinder_mass = self.cylinder.filled_volume * self.liquid.density

        # For a solid cylinder, ixx = iyy = mr²/4 + mh²/12
        self.inertiaI = cylinder_mass * (
            self.diameter**2 + self.cylinder.filled_height**2 / 12
        )

        # fluids considered inviscid so no shear resistance from torques in z axis
        self.inertiaZ = 0

        return self.inertiaI, self.inertiaZ


# @MrGribel
class MassFlowRateBasedTank(Tank):
    def __init__(
        self,
        name,
        diameter,
        height,
        bottomCap,
        upperCap,
        gas,
        liquid,
        initial_liquid_mass,
        initial_gas_mass,
        liquid_mass_flow_rate_in,
        gas_mass_flow_rate_in,
        liquid_mass_flow_rate_out,
        gas_mass_flow_rate_out,
        burn_out_time=300,
    ):
        """A motor tank defined based on liquid and gas mass flow rates.

        Parameters
        ----------
        name : str
            Name of the tank.
        diameter : float
            Diameter of the tank in meters.
        height : float
            Height of the tank in meters.
        bottomCap : str
            Type of bottom cap. Options are "flat" and "spherical".
        upperCap : str
            Type of upper cap. Options are "flat" and "spherical".
        gas : Gas
            motor.Gas object.
        liquid : Liquid
            motor.Liquid object.
        initial_liquid_mass : float
            Initial mass of liquid in the tank in kg.
        initial_gas_mass : float
            Initial mass of gas in the tank in kg.
        liquid_mass_flow_rate_in : str, float, array_like or callable
            Liquid mass flow rate entering the tank as a function of time.
            All values should be positive.
            If string is given, it should be the filepath of a csv file
            containing the data. For more information, see Function.
        gas_mass_flow_rate_in : str, float, array_like or callable
            Gas mass flow rate entering the tank as a function of time.
            All values should be positive.
            If string is given, it should be the filepath of a csv file
            containing the data. For more information, see Function.
        liquid_mass_flow_rate_out : str, float, array_like or callable
            Liquid mass flow rate exiting the tank as a function of time.
            All values should be positive.
            If string is given, it should be the filepath of a csv file
            containing the data. For more information, see Function.
        gas_mass_flow_rate_out : str, float, array_like or callable
            Gas mass flow rate exiting the tank as a function of time.
            All values should be positive.
            If string is given, it should be the filepath of a csv file
            containing the data. For more information, see Function.
        burn_out_time : float, optional
            Time in seconds greater than motor burn out time to use for
            numerical integration stopping criteria. Default is 300.
        """
        super().__init__(name, diameter, height, gas, liquid, bottomCap, upperCap)

        self.initial_liquid_mass = initial_liquid_mass
        self.initial_gas_mass = initial_gas_mass
        self.burn_out_time = burn_out_time

        self.gas_mass_flow_rate_in = Function(
            gas_mass_flow_rate_in,
            "Time (s)",
            "Inlet Gas Propellant Mass Flow Rate (kg/s)",
            "linear",
            "zero",
        )

        self.gas_mass_flow_rate_out = Function(
            gas_mass_flow_rate_out,
            "Time (s)",
            "Outlet Gas Propellant Mass Flow Rate (kg/s)",
            "linear",
            "zero",
        )

        self.liquid_mass_flow_rate_in = Function(
            liquid_mass_flow_rate_in,
            "Time (s)",
            "Inlet Liquid Propellant Mass Flow Rate (kg/s)",
            "linear",
            "zero",
        )

        self.liquid_mass_flow_rate_out = Function(
            liquid_mass_flow_rate_out,
            "Time (s)",
            "Outlet Liquid Propellant Mass Flow Rate (kg/s)",
            "linear",
            "zero",
        )

    @functools.cached_property
    def netMassFlowRate(self):
        """Returns the net mass flow rate of the tank as a function of time.
        Net mass flow rate is the mass flow rate entering the tank minus the
        mass flow rate exiting the tank, including liquids and gases. Positive
        is defined as a net mass flow rate entering the tank.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        Function
            Net mass flow rate of the tank as a function of time.
            Positive is defined as a net mass flow rate entering the tank.
        """
        self.liquid_net_mass_flow_rate = (
            self.liquid_mass_flow_rate_in - self.liquid_mass_flow_rate_out
        )

        self.liquid_net_mass_flow_rate.setOutputs(
            "Net Liquid Propellant Mass Flow Rate (kg/s)"
        )
        self.liquid_net_mass_flow_rate.setExtrapolation("zero")

        self.gas_net_mass_flow_rate = (
            self.gas_mass_flow_rate_in - self.gas_mass_flow_rate_out
        )

        self.gas_net_mass_flow_rate.setOutputs(
            "Net Gas Propellant Mass Flow Rate (kg/s)"
        )
        self.gas_net_mass_flow_rate.setExtrapolation("zero")

        self.net_mass_flow_rate = (
            self.liquid_net_mass_flow_rate + self.gas_net_mass_flow_rate
        )

        self.net_mass_flow_rate.setOutputs(
            "Net Propellant Mass Flow Rate Entering Tank (kg/s)"
        )
        self.net_mass_flow_rate.setExtrapolation("zero")

        return self.net_mass_flow_rate

    @functools.cached_property
    def mass(self):
        """Returns the total mass of liquid and gases inside the tank as a
        function of time.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        Function
            Mass of the tank as a function of time. Units in kg.
        """
        # Create an event function for solve_ivp

        def stopping_criteria(t, y):
            if y[0] / self.initial_liquid_mass > 0.95:
                return -1
            else:
                return self.netMassFlowRate(t)

        stopping_criteria.terminal = True

        # solve ODE's for liquid and gas masses
        sol = integrate.solve_ivp(
            lambda t, y: (
                self.liquid_net_mass_flow_rate(t),
                self.gas_net_mass_flow_rate(t),
            ),
            (0, self.burn_out_time),
            (self.initial_liquid_mass, self.initial_gas_mass),
            first_step=1e-3,
            vectorized=True,
            events=stopping_criteria,
            method="LSODA",
        )

        self.liquid_mass = Function(
            np.column_stack((sol.t, sol.y[0])),
            "Time (s)",
            "Liquid Propellant Mass In Tank (kg)",
        )

        self.gas_mass = Function(
            np.column_stack((sol.t, sol.y[1])),
            "Time (s)",
            "Gas Propellant Mass In Tank (kg)",
        )

        self.mass = self.liquid_mass + self.gas_mass
        self.mass.setOutputs("Total Propellant Mass In Tank (kg)")
        self.mass.setExtrapolation("constant")

        return self.mass

    @functools.cached_property
    def liquidVolume(self):
        """Returns the volume of liquid inside the tank as a function of time.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        Function
            Volume of liquid inside the tank as a function of time. Units in m^3.
        """
        self.liquid_volume = self.liquid_mass / self.liquid.density
        self.liquid_volume.setOutputs("Liquid Propellant Volume In Tank (m^3)")
        self.liquid_volume.setExtrapolation("constant")

        return self.liquid_volume


# @phmbressan
class UllageBasedTank(Tank):
    def __init__(
        self,
        name,
        diameter,
        height,
        endcap,
        liquid,
        gas,
        ullage,
    ):
        super().__init__(name, diameter, height, endcap, gas, liquid)
        pass


# @ompro07
class MassBasedTank(Tank):
    def __init__(
        self,
        name,
        diameter,
        height,
        bottomCap,
        upperCap,
        liquid_mass,
        gas_mass,
        liquid,
        gas,
    ):
        super().__init__(name, diameter, height, bottomCap, upperCap, gas, liquid)
        pass
