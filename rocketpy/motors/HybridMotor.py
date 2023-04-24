class HybridMotor(Motor):
    """Class to specify characteristics and useful operations for Hybrid
    motors.

    Attributes
    ----------

        Geometrical attributes:
        Motor.coordinateSystemOrientation : str
            Orientation of the motor's coordinate system. The coordinate system
            is defined by the motor's axis of symmetry. The origin of the
            coordinate system  may be placed anywhere along such axis, such as at the
            nozzle area, and must be kept the same for all other positions specified.
            Options are "nozzleToCombustionChamber" and "combustionChamberToNozzle".
        Motor.nozzleRadius : float
            Radius of motor nozzle outlet in meters.
        Motor.nozzlePosition : float
            Motor's nozzle outlet position in meters. More specifically, the coordinate
            of the nozzle outlet specified in the motor's coordinate system.
            See `Motor.coordinateSystemOrientation` for more information.
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
        grainNumber,
        grainDensity,
        grainOuterRadius,
        grainInitialInnerRadius,
        grainInitialHeight,
        oxidizerTankRadius,
        oxidizerTankHeight,
        oxidizerInitialPressure,
        oxidizerDensity,
        oxidizerMolarMass,
        oxidizerInitialVolume,
        distanceGrainToTank,
        injectorArea,
        burn_time=None,
        grainSeparation=0,
        nozzleRadius=0.0335,
        nozzlePosition=0,
        throatRadius=0.0114,
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
        oxidizerTankRadius :
            Oxidizer Tank inner radius.
        oxidizerTankHeight :
            Oxidizer Tank Height.
        oxidizerInitialPressure :
            Initial pressure of the oxidizer tank, could be equal to the pressure of the source cylinder in atm.
        oxidizerDensity :
            Oxidizer theoretical density in liquid state, for N2O is equal to 1.98 (Kg/m^3).
        oxidizerMolarMass :
            Oxidizer molar mass, for the N2O is equal to 44.01 (g/mol).
        oxidizerInitialVolume :
            Initial volume of oxidizer charged in the tank.
        distanceGrainToTank :
            Distance between the solid grain center of mass and the base of the oxidizer tank.
        injectorArea :
            injector outlet area.
        grainSeparation : int, float, optional
            Distance between grains, in meters. Default is 0.
        nozzleRadius : int, float, optional
            Motor's nozzle outlet radius in meters. Used to calculate Kn curve.
            Optional if the Kn curve is not interesting. Its value does not impact
            trajectory simulation.
        nozzlePosition : int, float, optional
            Motor's nozzle outlet position in meters. More specifically, the coordinate
            of the nozzle outlet specified in the motor's coordinate system.
            See `Motor.coordinateSystemOrientation` for more information.
            Default is 0, in which case the origin of the motor's coordinate system
            is placed at the motor's nozzle outlet.
        throatRadius : int, float, optional
            Motor's nozzle throat radius in meters. Its value has very low
            impact in trajectory simulation, only useful to analyze
            dynamic instabilities, therefore it is optional.
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
            coordinate system  may be placed anywhere along such axis, such as at the
            nozzle area, and must be kept the same for all other positions specified.
            Options are "nozzleToCombustionChamber" and "combustionChamberToNozzle".
            Default is "nozzleToCombustionChamber".

        Returns
        -------
        None
        """
        super().__init__(
            thrustSource,
            burn_time,
            nozzleRadius,
            nozzlePosition,
            throatRadius,
            reshapeThrustCurve,
            interpolationMethod,
        )

        # Define motor attributes
        # Grain and nozzle parameters
        self.grainNumber = grainNumber
        self.grainSeparation = grainSeparation
        self.grainDensity = grainDensity
        self.grainOuterRadius = grainOuterRadius
        self.grainInitialInnerRadius = grainInitialInnerRadius
        self.grainInitialHeight = grainInitialHeight
        self.oxidizerTankRadius = oxidizerTankRadius
        self.oxidizerTankHeight = oxidizerTankHeight
        self.oxidizerInitialPressure = oxidizerInitialPressure
        self.oxidizerDensity = oxidizerDensity
        self.oxidizerMolarMass = oxidizerMolarMass
        self.oxidizerInitialVolume = oxidizerInitialVolume
        self.distanceGrainToTank = distanceGrainToTank
        self.injectorArea = injectorArea

        # Other quantities that will be computed
        self.zCM = None
        self.oxidizerInitialMass = None
        self.grainInnerRadius = None
        self.grainHeight = None
        self.burnArea = None
        self.burnRate = None
        self.Kn = None

        # Compute uncalculated quantities
        # Grains initial geometrical parameters
        self.grainInitialVolume = (
            self.grainInitialHeight
            * np.pi
            * (self.grainOuterRadius**2 - self.grainInitialInnerRadius**2)
        )
        self.grainInitialMass = self.grainDensity * self.grainInitialVolume
        self.propellantInitialMass = (
            self.grainNumber * self.grainInitialMass
            + self.oxidizerInitialVolume * self.oxidizerDensity
        )
        # Dynamic quantities
        self.evaluateMassDot()
        self.evaluateMass()
        self.evaluateGeometry()
        self.evaluateInertia()
        self.evaluateCenterOfMass()

    @property
    def exhaustVelocity(self):
        """Calculates and returns exhaust velocity by assuming it
        as a constant. The formula used is total impulse/propellant
        initial mass. The value is also stored in
        self.exhaustVelocity.

        Parameters
        ----------
        None

        Returns
        -------
        self.exhaustVelocity : float
            Constant gas exhaust velocity of the motor.
        """
        return self.totalImpulse / self.propellantInitialMass

    def evaluateMassDot(self):
        """Calculates and returns the time derivative of propellant
        mass by assuming constant exhaust velocity. The formula used
        is the opposite of thrust divided by exhaust velocity. The
        result is a function of time, object of the Function class,
        which is stored in self.massDot.

        Parameters
        ----------
        None

        Returns
        -------
        self.massDot : Function
            Time derivative of total propellant mass as a function
            of time.
        """
        # Create mass dot Function
        self.massDot = self.thrust / (-self.exhaustVelocity)
        self.massDot.setOutputs("Mass Dot (kg/s)")
        self.massDot.setExtrapolation("zero")

        # Return Function
        return self.massDot

    def evaluateCenterOfMass(self):
        """Calculates and returns the time derivative of motor center of mass.
        The formulas used are the Bernoulli equation, law of the ideal gases and Boyle's law.
        The result is a function of time, object of the Function class, which is stored in self.zCM.

        Parameters
        ----------
        None

        Returns
        -------
        zCM : Function
            Position of the center of mass as a function
            of time.
        """

        self.zCM = 0

        return self.zCM

    def evaluateGeometry(self):
        """Calculates grain inner radius and grain height as a
        function of time by assuming that every propellant mass
        burnt is exhausted. In order to do that, a system of
        differential equations is solved using scipy.integrate.
        odeint. Furthermore, the function calculates burn area,
        burn rate and Kn as a function of time using the previous
        results. All functions are stored as objects of the class
        Function in self.grainInnerRadius, self.grainHeight, self.
        burnArea, self.burnRate and self.Kn.

        Parameters
        ----------
        None

        Returns
        -------
        geometry : list of Functions
            First element is the Function representing the inner
            radius of a grain as a function of time. Second
            argument is the Function representing the height of a
            grain as a function of time.
        """
        # Define initial conditions for integration
        y0 = [self.grainInitialInnerRadius, self.grainInitialHeight]

        # Define time mesh
        t = self.massDot.source[:, 0]

        density = self.grainDensity
        rO = self.grainOuterRadius

        # Define system of differential equations
        def geometryDot(y, t):
            grainMassDot = self.massDot(t) / self.grainNumber
            rI, h = y
            rIDot = (
                -0.5 * grainMassDot / (density * np.pi * (rO**2 - rI**2 + rI * h))
            )
            hDot = 1.0 * grainMassDot / (density * np.pi * (rO**2 - rI**2 + rI * h))
            return [rIDot, hDot]

        # Solve the system of differential equations
        sol = integrate.odeint(geometryDot, y0, t)

        # Write down functions for innerRadius and height
        self.grainInnerRadius = Function(
            np.concatenate(([t], [sol[:, 0]])).transpose().tolist(),
            "Time (s)",
            "Grain Inner Radius (m)",
            self.interpolate,
            "constant",
        )
        self.grainHeight = Function(
            np.concatenate(([t], [sol[:, 1]])).transpose().tolist(),
            "Time (s)",
            "Grain Height (m)",
            self.interpolate,
            "constant",
        )

        # Create functions describing burn rate, Kn and burn area
        self.evaluateBurnArea()
        self.evaluateKn()
        self.evaluateBurnRate()

        return [self.grainInnerRadius, self.grainHeight]

    def evaluateBurnArea(self):
        """Calculates the BurnArea of the grain for
        each time. Assuming that the grains are cylindrical
        BATES grains.

        Parameters
        ----------
        None

        Returns
        -------
        burnArea : Function
        Function representing the burn area progression with the time.
        """
        self.burnArea = (
            2
            * np.pi
            * (
                self.grainOuterRadius**2
                - self.grainInnerRadius**2
                + self.grainInnerRadius * self.grainHeight
            )
            * self.grainNumber
        )
        self.burnArea.setOutputs("Burn Area (m2)")
        return self.burnArea

    def evaluateBurnRate(self):
        """Calculates the BurnRate with respect to time.
        This evaluation assumes that it was already
        calculated the massDot, burnArea timeseries.

        Parameters
        ----------
        None

        Returns
        -------
        burnRate : Function
        Rate of progression of the inner radius during the combustion.
        """
        self.burnRate = (-1) * self.massDot / (self.burnArea * self.grainDensity)
        self.burnRate.setOutputs("Burn Rate (m/s)")
        return self.burnRate

    def evaluateKn(self):
        KnSource = (
            np.concatenate(
                (
                    [self.grainInnerRadius.source[:, 1]],
                    [self.burnArea.source[:, 1] / self.throatArea],
                )
            ).transpose()
        ).tolist()
        self.Kn = Function(
            KnSource,
            "Grain Inner Radius (m)",
            "Kn (m2/m2)",
            self.interpolate,
            "constant",
        )
        return self.Kn

    def evaluateInertia(self):
        """Calculates propellant inertia I, relative to directions
        perpendicular to the rocket body axis and its time derivative
        as a function of time. Also calculates propellant inertia Z,
        relative to the axial direction, and its time derivative as a
        function of time. Products of inertia are assumed null due to
        symmetry. The four functions are stored as an object of the
        Function class.

        Parameters
        ----------
        None

        Returns
        -------
        list of Functions
            The first argument is the Function representing inertia I,
            while the second argument is the Function representing
            inertia Z.
        """

        # Inertia I
        # Calculate inertia I for each grain
        grainMass = self.mass / self.grainNumber
        grainMassDot = self.massDot / self.grainNumber
        grainNumber = self.grainNumber
        grainInertiaI = grainMass * (
            (1 / 4) * (self.grainOuterRadius**2 + self.grainInnerRadius**2)
            + (1 / 12) * self.grainHeight**2
        )

        # Calculate each grain's distance d to propellant center of mass
        initialValue = (grainNumber - 1) / 2
        d = np.linspace(-initialValue, initialValue, grainNumber)
        d = d * (self.grainInitialHeight + self.grainSeparation)

        # Calculate inertia for all grains
        self.inertiaI = grainNumber * grainInertiaI + grainMass * np.sum(d**2)
        self.inertiaI.setOutputs("Propellant Inertia I (kg*m2)")

        # Inertia I Dot
        # Calculate each grain's inertia I dot
        grainInertiaIDot = (
            grainMassDot
            * (
                (1 / 4) * (self.grainOuterRadius**2 + self.grainInnerRadius**2)
                + (1 / 12) * self.grainHeight**2
            )
            + grainMass
            * ((1 / 2) * self.grainInnerRadius - (1 / 3) * self.grainHeight)
            * self.burnRate
        )

        # Calculate inertia I dot for all grains
        self.inertiaIDot = grainNumber * grainInertiaIDot + grainMassDot * np.sum(
            d**2
        )
        self.inertiaIDot.setOutputs("Propellant Inertia I Dot (kg*m2/s)")

        # Inertia Z
        self.inertiaZ = (
            (1 / 2.0)
            * self.mass
            * (self.grainOuterRadius**2 + self.grainInnerRadius**2)
        )
        self.inertiaZ.setOutputs("Propellant Inertia Z (kg*m2)")

        # Inertia Z Dot
        self.inertiaZDot = (1 / 2.0) * self.massDot * (
            self.grainOuterRadius**2 + self.grainInnerRadius**2
        ) + self.mass * self.grainInnerRadius * self.burnRate
        self.inertiaZDot.setOutputs("Propellant Inertia Z Dot (kg*m2/s)")

        return [self.inertiaI, self.inertiaZ]

    def allInfo(self):
        pass
