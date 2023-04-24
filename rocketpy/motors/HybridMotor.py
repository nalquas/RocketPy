# -*- coding: utf-8 -*-

__author__ = "Giovani Hidalgo Ceotto, Oscar Mauricio Prada Ramirez, João Lemes Gribel Soares, Lucas Kierulff Balabram, Lucas Azevedo Pezente"
__copyright__ = "Copyright 20XX, RocketPy Team"
__license__ = "MIT"

import numpy as np
from scipy import integrate
from functools import cached_property

from rocketpy.Function import Function, funcify_method
from rocketpy.motors import SolidMotor, LiquidMotor, Motor


class HybridMotor(Motor):
    """Class to specify characteristics and useful operations for Hybrid
    motors.

    Attributes
    ----------

        Geometrical attributes:
        Motor.coordinateSystemOrientation : str
            Orientation of the motor's coordinate system. The coordinate system
            is defined by the motor's axis of symmetry. The origin of the
            coordinate system  may be placed anywhere along such axis, such as
            at the nozzle area, and must be kept the same for all other
            positions specified. Options are "nozzleToCombustionChamber" and
            "combustionChamberToNozzle".
        Motor.nozzleRadius : float
            Radius of motor nozzle outlet in meters.
        Motor.nozzlePosition : float
            Motor's nozzle outlet position in meters, specified in the motor's
            coordinate system. See `Motor.coordinateSystemOrientation` for
            more information.
        Motor.throatRadius : float
            Radius of motor nozzle throat in meters.
        Motor.grainNumber : int
            Number of solid grains.
        Motor.grainSeparation : float
            Distance between two grains in meters.
        Motor.grainDensity : float
            Density of each grain in kg/meters cubed.
        Motor.grainOuterRadius : float
            Outer radius of each grain in meters.
        Motor.grainInitialInnerRadius : float
            Initial inner radius of each grain in meters.
        Motor.grainInitialHeight : float
            Initial height of each grain in meters.
        Motor.grainInitialVolume : float
            Initial volume of each grain in meters cubed.
        Motor.grainInnerRadius : Function
            Inner radius of each grain in meters as a function of time.
        Motor.grainHeight : Function
            Height of each grain in meters as a function of time.

        Mass and moment of inertia attributes:
        Motor.grainInitialMass : float
            Initial mass of each grain in kg.
        Motor.propellantInitialMass : float
            Total propellant initial mass in kg.
        Motor.mass : Function
            Propellant total mass in kg as a function of time.
        Motor.massDot : Function
            Time derivative of propellant total mass in kg/s as a function
            of time.
        Motor.inertiaI : Function
            Propellant moment of inertia in kg*meter^2 with respect to axis
            perpendicular to axis of cylindrical symmetry of each grain,
            given as a function of time.
        Motor.inertiaIDot : Function
            Time derivative of inertiaI given in kg*meter^2/s as a function
            of time.
        Motor.inertiaZ : Function
            Propellant moment of inertia in kg*meter^2 with respect to axis of
            cylindrical symmetry of each grain, given as a function of time.
        Motor.inertiaDot : Function
            Time derivative of inertiaZ given in kg*meter^2/s as a function
            of time.

        Thrust and burn attributes:
        Motor.thrust : Function
            Motor thrust force, in Newtons, as a function of time.
        Motor.totalImpulse : float
            Total impulse of the thrust curve in N*s.
        Motor.maxThrust : float
            Maximum thrust value of the given thrust curve, in N.
        Motor.maxThrustTime : float
            Time, in seconds, in which the maximum thrust value is achieved.
        Motor.averageThrust : float
            Average thrust of the motor, given in N.
        Motor.burnOutTime : float
            Total motor burn out time, in seconds. Must include delay time
            when the motor takes time to ignite. Also seen as time to end thrust
            curve.
        Motor.exhaustVelocity : float
            Propulsion gases exhaust velocity, assumed constant, in m/s.
        Motor.burnArea : Function
            Total burn area considering all grains, made out of inner
            cylindrical burn area and grain top and bottom faces. Expressed
            in meters squared as a function of time.
        Motor.Kn : Function
            Motor Kn as a function of time. Defined as burnArea divided by
            nozzle throat cross sectional area. Has no units.
        Motor.burnRate : Function
            Propellant burn rate in meter/second as a function of time.
        Motor.interpolate : string
            Method of interpolation used in case thrust curve is given
            by data set in .csv or .eng, or as an array. Options are 'spline'
            'akima' and 'linear'. Default is "linear".
    """

    def __init__(
        self,
        thrustSource,
        grainsCenterOfMassPosition,
        grainNumber,
        grainDensity,
        grainOuterRadius,
        grainInitialInnerRadius,
        grainInitialHeight,
        grainSeparation,
        nozzleRadius,
        burn_time=None,
        nozzlePosition=0,
        throatRadius=0.01,
        reshapeThrustCurve=False,
        interpolationMethod="linear",
        coordinateSystemOrientation="nozzleToCombustionChamber",
    ):
        """Initialize Motor class, process thrust curve and geometrical
        parameters and store results.

        Parameters
        ----------
        thrustSource : int, float, callable, string, array
            Motor's thrust curve. Can be given as an int or float, in which
            case the thrust will be considered constant in time. It can
            also be given as a callable function, whose argument is time in
            seconds and returns the thrust supplied by the motor in the
            instant. If a string is given, it must point to a .csv or .eng file.
            The .csv file shall contain no headers and the first column must
            specify time in seconds, while the second column specifies thrust.
            Arrays may also be specified, following rules set by the class
            Function. See help(Function). Thrust units are Newtons.
        burn_time: float, tuple of float, optional
            Motor's burn time.
            If a float is given, the burn time is assumed to be between 0 and the
            given float, in seconds.
            If a tuple of float is given, the burn time is assumed to be between
            the first and second elements of the tuple, in seconds.
            If not specified, automatically sourced as the range between the first- and
            last-time step of the motor's thrust curve. This can only be used if the
            motor's thrust is defined by a list of points, such as a .csv file, a .eng
            file or a Function instance whose source is a list.
        grainNumber : int
            Number of solid grains
        grainDensity : int, float
            Solid grain density in kg/m3.
        grainOuterRadius : int, float
            Solid grain outer radius in meters.
        grainInitialInnerRadius : int, float
            Solid grain initial inner radius in meters.
        grainInitialHeight : int, float
            Solid grain initial height in meters.
        grainSeparation : int, float
            Distance between grains, in meters.
        nozzleRadius : int, float
            Motor's nozzle outlet radius in meters.
        nozzlePosition : int, float, optional
            Motor's nozzle outlet position in meters, in the motor's coordinate
            system. See `Motor.coordinateSystemOrientation` for details.
            Default is 0, in which case the origin of the coordinate system
            is placed at the motor's nozzle outlet.
        throatRadius : int, float, optional
            Motor's nozzle throat radius in meters. Used to calculate Kn curve.
            Optional if the Kn curve is not interesting. Its value does not
            impact trajectory simulation.
        reshapeThrustCurve : boolean, tuple, optional
            If False, the original thrust curve supplied is not altered. If a
            tuple is given, whose first parameter is a new burn out time and
            whose second parameter is a new total impulse in Ns, the thrust
            curve is reshaped to match the new specifications. May be useful
            for motors whose thrust curve shape is expected to remain similar
            in case the impulse and burn time varies slightly. Default is
            False.
        interpolationMethod : string, optional
            Method of interpolation to be used in case thrust curve is given
            by data set in .csv or .eng, or as an array. Options are 'spline'
            'akima' and 'linear'. Default is "linear".
        coordinateSystemOrientation : string, optional
            Orientation of the motor's coordinate system. The coordinate system
            is defined by the motor's axis of symmetry. The origin of the
            coordinate system  may be placed anywhere along such axis, such as
            at the nozzle area, and must be kept the same for all other
            positions specified. Options are "nozzleToCombustionChamber" and
            "combustionChamberToNozzle". Default is "nozzleToCombustionChamber".

        Returns
        -------
        None
        """
        super().__init__(
            thrustSource,
            nozzleRadius,
            burn_time,
            nozzlePosition,
            reshapeThrustCurve,
            interpolationMethod,
            coordinateSystemOrientation,
        )
        self.liquid = LiquidMotor(
            thrustSource,
            nozzleRadius,
            burn_time,
            nozzlePosition,
            reshapeThrustCurve,
            interpolationMethod,
            coordinateSystemOrientation,
        )
        self.solid = SolidMotor(
            thrustSource,
            grainsCenterOfMassPosition,
            grainNumber,
            grainDensity,
            grainOuterRadius,
            grainInitialInnerRadius,
            grainInitialHeight,
            grainSeparation,
            nozzleRadius,
            burn_time,
            nozzlePosition,
            throatRadius,
            reshapeThrustCurve,
            interpolationMethod,
            coordinateSystemOrientation,
        )

    @funcify_method("Time (s)", "mass (kg)")
    def mass(self):
        """Evaluates the total propellant mass of the motor as the sum
        of each tank mass and the grains mass.

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        Function
            Total propellant mass of the motor, in kg.
        """
        return self.solid.mass + self.liquid.mass

    @cached_property
    def propellantInitialMass(self):
        """Returns the initial propellant mass of the motor

        Parameters
        ----------
        None

        Returns
        -------
        float
            Initial propellant mass of the motor, in kg.
        """
        return self.solid.propellantInitialMass + self.liquid.propellantInitialMass

    @funcify_method("Time (s)", "mass flow rate (kg/s)", extrapolation="zero")
    def massFlowRate(self):
        """Evaluates the mass flow rate of the motor as the sum of each tank
        mass flow rate and the grains mass flow rate.

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        Function
            Mass flow rate of the motor, in kg/s.
        """
        return self.solid.massFlowRate + self.liquid.massFlowRate

    @funcify_method("Time (s)", "center of mass (m)")
    def centerOfMass(self):
        """Calculates and returns the time derivative of motor center of mass.
        The formulas used are the Bernoulli equation, law of the ideal gases and
        Boyle's law. The result is a function of time, object of the
        Function class.

        Parameters
        ----------
        None

        Returns
        -------
        Function
            Position of the center of mass as a function of time.
        """
        massBalance = (
            self.solid.mass * self.solid.centerOfMass
            + self.liquid.mass * self.liquid.centerOfMass
        )
        return massBalance / self.mass

    @cached_property
    def inertiaTensor(self):
        """Calculates the propellant principal moment of inertia relative
        to the tank center of mass. The z-axis correspond to the motor axis
        of symmetry while the x and y axes complete the right-handed coordinate
        system. The time derivatives of the products of inertia are also
        evaluated.
        Products of inertia are assumed null due to symmetry.

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        tuple (of Functions)
            The two first arguments are equivalent and represent inertia Ix,
            and Iy. The third argument is inertia Iz.
        """
        solidCorrection = (
            self.solid.mass * (self.solid.centerOfMass - self.centerOfMass) ** 2
        )
        liquidCorrection = (
            self.liquid.mass * (self.liquid.centerOfMass - self.centerOfMass) ** 2
        )

        solidInertia = self.solid.inertiaTensor
        liquidInertia = self.liquid.inertiaTensor

        self.InertiaI = (
            solidInertia[0] + solidCorrection + liquidInertia[0] + liquidCorrection
        )
        self.InertiaZ = (
            solidInertia[2] + solidCorrection + liquidInertia[2] + liquidCorrection
        )

        # Set naming convention
        self.InertiaI.reset("Time (s)", "inertia y (kg*m^2)")
        self.InertiaZ.reset("Time (s)", "inertia z (kg*m^2)")

        return self.InertiaI, self.InertiaI, self.InertiaZ

    @funcify_method("Time (s)", "Inertia I_11 (kg m²)")
    def I_11(self):
        """Inertia tensor 11 component, which corresponds to the inertia
        relative to the e_1 axis, centered at the instantaneous center of mass.

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        float
            Propellant inertia tensor 11 component at time t.

        Notes
        -----
        The e_1 direction is assumed to be the direction perpendicular to the
        motor body axis.
        Due to symmetry, the inertia tensor 22 component is equal to the
        inertia tensor 11 component.

        References
        ----------
        .. [1] https://en.wikipedia.org/wiki/Moment_of_inertia#Inertia_tensor
        """
        solidCorrection = (
            self.solid.mass * (self.solid.centerOfMass - self.centerOfMass) ** 2
        )
        liquidCorrection = (
            self.liquid.mass * (self.liquid.centerOfMass - self.centerOfMass) ** 2
        )

        I_11 = self.solid.I_11 + solidCorrection + self.liquid.I_11 + liquidCorrection
        return I_11

    @funcify_method("Time (s)", "Inertia I_22 (kg m²)")
    def I_22(self):
        """Inertia tensor 22 component, which corresponds to the inertia
        relative to the e_2 axis, centered at the instantaneous center of mass.

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        float
            Propellant inertia tensor 22 component at time t.

        Notes
        -----
        The e_2 direction is assumed to be the direction perpendicular to the
        motor body axis and to the e_1 axis.
        Due to symmetry, the inertia tensor 22 component is equal to the
        inertia tensor 11 component.

        References
        ----------
        .. [1] https://en.wikipedia.org/wiki/Moment_of_inertia#Inertia_tensor
        """
        return self.I_11

    @funcify_method("Time (s)", "Inertia I_33 (kg m²)")
    def I_33(self):
        """Inertia tensor 33 component, which corresponds to the inertia
        relative to the e_3 axis, centered at the instantaneous center of mass.

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        float
            Propellant inertia tensor 33 component at time t.

        Notes
        -----
        The e_3 direction is assumed to be the direction parallel to the motor
        body axis.

        References
        ----------
        .. [1] https://en.wikipedia.org/wiki/Moment_of_inertia#Inertia_tensor
        """
        return self.solid.I_33 + self.liquid.I_33

    @funcify_method("Time (s)", "Inertia I_12 (kg m²)")
    def I_12(self):
        return 0

    @funcify_method("Time (s)", "Inertia I_13 (kg m²)")
    def I_13(self):
        return 0

    @funcify_method("Time (s)", "Inertia I_23 (kg m²)")
    def I_23(self):
        return 0

    def addTank(self, tank, position):
        """Adds a tank to the motor.

        Parameters
        ----------
        tank : Tank
            Tank object to be added to the motor.
        position : float
            Position of the tank relative to the nozzle exit. The
            tank reference point is its tank_geometry zero point.

        Returns
        -------
        None
        """
        self.liquid.addTank(tank, position)
        self.solid.massFlowRate = self.massDot - self.liquid.massFlowRate

    def allInfo(self):
        """Prints out all data and graphs available about the Motor.

        Parameters
        ----------
        None

        Return
        ------
        None
        """
        # Print nozzle details
        print("Nozzle Details")
        print("Nozzle Radius: " + str(self.nozzleRadius) + " m")
        print("Nozzle Throat Radius: " + str(self.solid.throatRadius) + " m")

        # Print grain details
        print("\nGrain Details")
        print("Number of Grains: " + str(self.solid.grainNumber))
        print("Grain Spacing: " + str(self.solid.grainSeparation) + " m")
        print("Grain Density: " + str(self.solid.grainDensity) + " kg/m3")
        print("Grain Outer Radius: " + str(self.solid.grainOuterRadius) + " m")
        print("Grain Inner Radius: " + str(self.solid.grainInitialInnerRadius) + " m")
        print("Grain Height: " + str(self.solid.grainInitialHeight) + " m")
        print("Grain Volume: " + "{:.3f}".format(self.solid.grainInitialVolume) + " m3")
        print("Grain Mass: " + "{:.3f}".format(self.solid.grainInitialMass) + " kg")

        # Print motor details
        print("\nMotor Details")
        print("Total Burning Time: " + str(self.burnDuration) + " s")
        print(
            "Total Propellant Mass: "
            + "{:.3f}".format(self.propellantInitialMass)
            + " kg"
        )
        print(
            "Propellant Exhaust Velocity: "
            + "{:.3f}".format(self.exhaustVelocity)
            + " m/s"
        )
        print("Average Thrust: " + "{:.3f}".format(self.averageThrust) + " N")
        print(
            "Maximum Thrust: "
            + str(self.maxThrust)
            + " N at "
            + str(self.maxThrustTime)
            + " s after ignition."
        )
        print("Total Impulse: " + "{:.3f}".format(self.totalImpulse) + " Ns")

        # Show plots
        print("\nPlots")
        self.thrust.plot(*self.burn_time)
        self.mass.plot(*self.burn_time)
        self.massFlowRate.plot(*self.burn_time)
        self.solid.grainInnerRadius.plot(*self.burn_time)
        self.solid.grainHeight.plot(*self.burn_time)
        self.solid.burnRate.plot(0, self.solid.grainBurnOut)
        self.solid.burnArea.plot(*self.burn_time)
        self.solid.Kn.plot(*self.burn_time)
        self.centerOfMass.plot(*self.burn_time, samples=50)
        self.inertiaTensor[0].plot(*self.burn_time, samples=50)
        self.inertiaTensor[2].plot(*self.burn_time, samples=50)

        return None
