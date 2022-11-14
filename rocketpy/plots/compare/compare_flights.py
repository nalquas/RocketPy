__author__ = "Guilherme Fernandes Alves, Mateus Stano Junqueira"
__copyright__ = "Copyright 20XX, RocketPy Team"
__license__ = "MIT"

import matplotlib.pyplot as plt


class CompareFlights:
    """A class to compare the results of multiple flights.

    Parameters
    ----------
    flights : list
        A list of Flight objects to be compared.

    Attributes
    ----------
    flights : list
        A list of Flight objects to be compared.

    """

    def __init__(self, flights: list) -> None:
        """Initializes the CompareFlights class.

        Parameters
        ----------
        flights : list
            A list of Flight objects to be compared.

        Returns
        -------
        None
        """

        self.flights = flights

        return None

    def __create_comparison_figure(
        self,
        figsize=(7, 10),  # (width, height)
        legend=True,
        n_rows=3,
        n_cols=1,
        n_plots=3,
        title="Comparison",
        x_labels=["Time (s)", "Time (s)", "Time (s)"],
        y_labels=["x (m)", "y (m)", "z (m)"],
        flight_attributes=["x", "y", "z"],
    ):
        """Creates a figure to compare the results of multiple flights.

        Parameters
        ----------
        figsize : tuple, optional
            The size of the figure, by default (7, 10)
        legend : bool, optional
            Whether to show the legend or not, by default True
        n_rows : int, optional
            The number of rows of the figure, by default 3
        n_cols : int, optional
            The number of columns of the figure, by default 1
        n_plots : int, optional
            The number of plots in the figure, by default 3
        title : str, optional
            The title of the figure, by default "Comparison"
        x_labels : list, optional
            The x labels of each subplot, by default ["Time (s)", "Time (s)", "Time (s)"]
        y_labels : list, optional
            The y labels of each subplot, by default ["x (m)", "y (m)", "z (m)"]
        flight_attributes : list, optional
            The attributes of the Flight class to be plotted, by default ["x", "y", "z"].
            The attributes must be a list of strings. Each string must be a valid
            attribute of the Flight class, i.e., should point to a attribute of
            the Flight class that is a Function object or a numpy array.

        Returns
        -------
        fig : matplotlib.figure.Figure
            The figure object.
        ax : matplotlib.axes._subplots.AxesSubplot
            The axes object.
        """

        # Create the matplotlib figure
        fig = plt.figure(figsize=figsize)
        fig.suptitle(title, fontsize=16, y=1.02, x=0.5)

        # Create the subplots
        ax = []
        for i in range(n_plots):
            ax.append(plt.subplot(n_rows, n_cols, i + 1))

        # Get the maximum time of all the flights
        max_time = 0

        # Adding the plots to each subplot
        for flight in self.flights:
            for i in range(n_plots):
                try:
                    ax[i].plot(
                        flight.time,
                        flight.__getattribute__(flight_attributes[i])[:, 1],
                        label=flight.name,
                    )
                    # Update the maximum time
                    max_time = flight.tFinal if flight.time[-1] > max_time else max_time
                except AttributeError:
                    raise AttributeError(
                        f"Invalid attribute {flight_attributes[i]} for the Flight class."
                    )

        # Set the labels for the x and y axis
        for i, subplot in enumerate(ax):
            subplot.set_xlabel(x_labels[i])
            subplot.set_ylabel(y_labels[i])

        # Set the limits for the x axis
        for subplot in ax:
            subplot.set_xlim(0, max_time)

        # Set the legend
        if legend:
            fig.legend(
                loc="upper center",
                fancybox=True,
                shadow=True,
                fontsize=10,
                bbox_to_anchor=(0.5, 0.995),
            )

        fig.tight_layout()

        return fig, ax

    def positions(self, figsize=(7, 10), legend=True, filename=None):
        """Plots a comparison of the position of the rocket in the three
        dimensions separately.

        Parameters
        ----------
        figsize : tuple, optional
            standard matplotlib figsize to be used in the plots, by default (7, 10),
            where the tuple means (width, height).
        legend : bool, optional
            Weather or not to show the legend, by default True
        filename : str, optional
            If a filename is provided, the plot will be saved to a file, by default None.
            Image options are: png, pdf, ps, eps and svg.

        Returns
        -------
        None
        """

        # Create the figure
        fig, _ = self.__create_comparison_figure(
            figsize=figsize,
            legend=legend,
            n_rows=3,
            n_cols=1,
            n_plots=3,
            title="Comparison of the position of the rocket",
            x_labels=["Time (s)", "Time (s)", "Time (s)"],
            y_labels=["x (m)", "y (m)", "z (m)"],
            flight_attributes=["x", "y", "z"],
        )

        # Saving the plot to a file if a filename is provided, showing the plot otherwise
        if filename:
            fig.savefig(filename)
            plt.close()
        else:
            plt.show()
            plt.close()

        return None

    def velocities(self, figsize=(7, 10 * 4 / 3), legend=True, filename=None):
        """Plots a comparison of the velocity of the rocket in the three
        dimensions separately.

        Parameters
        ----------
        figsize : tuple, optional
            standard matplotlib figsize to be used in the plots, by default (7, 10),
            where the tuple means (width, height).
        legend : bool, optional
            Weather or not to show the legend, by default True
        filename : str, optional
            If a filename is provided, the plot will be saved to a file, by default None.
            Image options are: png, pdf, ps, eps and svg.

        Returns
        -------
        None
        """

        # Create the figure
        fig, _ = self.__create_comparison_figure(
            figsize=figsize,
            legend=legend,
            n_rows=4,
            n_cols=1,
            n_plots=4,
            title="Comparison of the velocity of the flights",
            x_labels=["Time (s)", "Time (s)", "Time (s)", "Time (s)"],
            y_labels=["speed (m/s)", "vx (m/s)", "vy (m/s)", "vz (m/s)"],
            flight_attributes=["speed", "vx", "vy", "vz"],
        )

        # Saving the plot to a file if a filename is provided, showing the plot otherwise
        if filename:
            fig.savefig(filename)
            plt.close()
        else:
            plt.show()
            plt.close()

        return None

    def stream_velocities(self, figsize=(7, 10 * 4 / 3), legend=True, filename=None):
        """Plots a stream plot of the free stream velocity of the rocket in the
        three dimensions separately. The free stream velocity is the velocity of
        the rocket relative to the air.

        Parameters
        ----------
        figsize : tuple, optional
            standard matplotlib figsize to be used in the plots, by default (7, 10 * 4 / 3),
            where the tuple means (width, height).
        legend : bool, optional
            Weather or not to show the legend, by default True
        filename : str, optional
            If a filename is provided, the plot will be saved to a file, by default None.
            Image options are: png, pdf, ps, eps and svg.

        Returns
        -------
        None
        """

        # Create the figure
        fig, _ = self.__create_comparison_figure(
            figsize=figsize,
            legend=legend,
            n_rows=4,
            n_cols=1,
            n_plots=4,
            title="Comparison of the free stream velocity of the flights",
            x_labels=["Time (s)", "Time (s)", "Time (s)", "Time (s)"],
            y_labels=[
                "Freestream speed (m/s)",
                "Freestream vx (m/s)",
                "Freestream vy (m/s)",
                "Freestream vz (m/s)",
            ],
            flight_attributes=[
                "freestreamSpeed",
                "streamVelocityX",
                "streamVelocityY",
                "streamVelocityZ",
            ],
        )

        # Saving the plot to a file if a filename is provided, showing the plot otherwise
        if filename:
            fig.savefig(filename)
            plt.close()
        else:
            plt.show()
            plt.close()

        return None

    def accelerations(self, figsize=(7, 10 * 4 / 3), legend=True, filename=None):
        """Plots a comparison of the acceleration of the rocket in the three
        dimensions separately.

        Parameters
        ----------
        figsize : tuple, optional
            standard matplotlib figsize to be used in the plots, by default (7, 10),
            where the tuple means (width, height).
        legend : bool, optional
            Weather or not to show the legend, by default True
        filename : str, optional
            If a filename is provided, the plot will be saved to a file, by default None.
            Image options are: png, pdf, ps, eps and svg.

        Returns
        -------
        None
        """

        # Create the figure
        fig, _ = self.__create_comparison_figure(
            figsize=figsize,
            legend=legend,
            n_rows=4,
            n_cols=1,
            n_plots=4,
            title="Comparison of the acceleration of the flights",
            x_labels=["Time (s)", "Time (s)", "Time (s)", "Time (s)"],
            y_labels=[
                "Acceleration (m/s^2)",
                "ax (m/s^2)",
                "ay (m/s^2)",
                "az (m/s^2)",
            ],
            flight_attributes=["acceleration", "ax", "ay", "az"],
        )

        # Saving the plot to a file if a filename is provided, showing the plot otherwise
        if filename:
            fig.savefig(filename)
            plt.close()
        else:
            plt.show()
            plt.close()

        return None
