# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2022 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.
"""
Provides plot helper class to deal with flint proxy.
"""

import typing
from typing import Union
from typing import Optional
from typing import Tuple

import numpy
import gevent
import contextlib

from . import proxy
from bliss.common import event
from bliss.common import deprecation


class BasePlot(object):

    # Name of the corresponding silx widget
    WIDGET = NotImplemented

    # Available name to identify this plot
    ALIASES = []

    def __init__(self, flint, plot_id, register=False):
        """Describe a custom plot handled by Flint."""
        self._plot_id = plot_id
        self._flint = flint
        self._xlabel = None
        self._ylabel = None
        self._init()
        if flint is not None:
            if register:
                self._init_plot()

    def _init(self):
        """Allow to initialize extra attributes in a derived class, without
        redefining the constructor"""

    def _init_plot(self):
        """Inherits it to custom the plot initialization"""
        if self._xlabel is not None:
            self.submit("setGraphXLabel", self._xlabel)
        if self._ylabel is not None:
            self.submit("setGraphYLabel", self._ylabel)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, txt):
        self._title = str(txt)
        self.submit("setGraphTitle", self._title)

    @property
    def xlabel(self):
        return self._xlabel

    @xlabel.setter
    def xlabel(self, txt):
        self._xlabel = str(txt)
        self.submit("setGraphXLabel", self._xlabel)

    @property
    def ylabel(self):
        return self._ylabel

    @ylabel.setter
    def ylabel(self, txt):
        self._ylabel = str(txt)
        self.submit("setGraphYLabel", self._ylabel)

    def __repr__(self):
        try:
            # Protect problems on RPC
            name = self._flint.get_plot_name(self._plot_id)
        except Exception:
            name = None
        return "{}(plot_id={!r}, flint_pid={!r}, name={!r})".format(
            self.__class__.__name__, self.plot_id, self.flint_pid, name
        )

    def submit(self, method, *args, **kwargs):
        return self._flint.run_method(self.plot_id, method, args, kwargs)

    # Properties

    @property
    def flint_pid(self):
        return self._flint._pid

    @property
    def plot_id(self):
        return self._plot_id

    @property
    def name(self):
        return self._flint.get_plot_name(self._plot_id)

    def focus(self):
        """Set the focus on this plot"""
        self._flint.set_plot_focus(self._plot_id)

    def export_to_logbook(self):
        """Set the focus on this plot"""
        self._flint.export_to_logbook(self._plot_id)

    def get_data_range(self):
        """Returns the current data range used by this plot"""
        return self.submit("getDataRange")

    # Clean up

    def is_open(self) -> bool:
        """Returns true if the plot is still open in the linked Flint
        application"""
        try:
            return self._flint.plot_exists(self._plot_id)
        except Exception:
            # The proxy is maybe dead
            return False

    def close(self):
        self._flint.remove_plot(self.plot_id)

    # Interaction

    def _wait_for_user_selection(self, request_id):
        """Wait for a user selection and clean up result in case of error"""
        proxy.FLINT_LOGGER.warning("Waiting for selection in Flint window.")
        flint = self._flint
        results = gevent.queue.Queue()
        event.connect(flint._proxy, request_id, results.put)
        try:
            result = results.get()
            return result
        except Exception:
            try:
                flint.cancel_request(request_id)
            except Exception:
                proxy.FLINT_LOGGER.debug(
                    "Error while canceling the request", exc_info=True
                )
            proxy.FLINT_LOGGER.warning("Plot selection cancelled. An error occurred.")
            raise
        except KeyboardInterrupt:
            try:
                flint.cancel_request(request_id)
            except Exception:
                proxy.FLINT_LOGGER.debug(
                    "Error while canceling the request", exc_info=True
                )
            proxy.FLINT_LOGGER.warning("Plot selection cancelled by bliss user.")
            raise

    def select_shapes(
        self,
        initial_selection: typing.Optional[typing.List[typing.Any]] = None,
        kinds: typing.Union[str, typing.List[str]] = "rectangle",
    ):
        """
        Request user selection of shapes.

        `initial_selection` is a list of ROIs from `bliss.controllers.lima.roi`.

        It also supports key-value dictionary for simple rectangle.
        In this case, the dictionary contains "kind" (which is "Rectangle"),
        and "label", "origin" and "size" which are tuples of 2 floats.

        Arguments:
            initial_selection: List of shapes already selected.
            kinds: List or ROI kind which can be created (for now, "rectangle"
                (described as a dict), "lima-rectangle", "lima-arc",
                "lima-vertical-profile",
                "lima-horizontal-profile")
        """
        flint = self._flint
        request_id = flint.request_select_shapes(
            self._plot_id, initial_selection, kinds=kinds
        )
        result = self._wait_for_user_selection(request_id)
        return result

    def select_points(self, nb):
        flint = self._flint
        request_id = flint.request_select_points(self._plot_id, nb)
        return self._wait_for_user_selection(request_id)

    def select_shape(self, shape):
        flint = self._flint
        request_id = flint.request_select_shape(self._plot_id, shape)
        return self._wait_for_user_selection(request_id)

    def _set_colormap(
        self,
        lut: Optional[str] = None,
        vmin: Optional[Union[float, str]] = None,
        vmax: Optional[Union[float, str]] = None,
        normalization: Optional[str] = None,
        gamma_normalization: Optional[float] = None,
        autoscale: Optional[bool] = None,
        autoscale_mode: Optional[str] = None,
    ):
        """
        Allows to setup the default colormap of this plot.

        Arguments:
            lut: A name of a LUT. At least the following names are supported:
                 `"gray"`, `"reversed gray"`, `"temperature"`, `"red"`, `"green"`,
                 `"blue"`, `"jet"`, `"viridis"`, `"magma"`, `"inferno"`, `"plasma"`.
            vmin: Can be a float or "`auto"` to set the min level value
            vmax: Can be a float or "`auto"` to set the max level value
            normalization: Can be on of `"linear"`, `"log"`, `"arcsinh"`,
                           `"sqrt"`, `"gamma"`.
            gamma_normalization: float defining the gamma normalization.
                                 If this argument is defined the `normalization`
                                 argument is ignored
            autoscale: If true, the auto scale is set for min and max
                       (vmin and vmax arguments are ignored)
            autoscale_mode: Can be one of `"minmax"` or `"3stddev"`
        """
        flint = self._flint
        flint.set_plot_colormap(
            self._plot_id,
            lut=lut,
            vmin=vmin,
            vmax=vmax,
            normalization=normalization,
            gammaNormalization=gamma_normalization,
            autoscale=autoscale,
            autoscaleMode=autoscale_mode,
        )


class _DataPlot(BasePlot):
    """
    Plot providing a common API to store data

    This was introduced for baward compatibility with BLISS <= 1.8

    FIXME: This have to be deprecated and removed. Plots should be updated using
    another API
    """

    # Data handling

    def upload_data(self, field, data):
        """
        Update data as an identifier into the server side

        Argument:
            field: Identifier in the targeted plot
            data: Data to upload
        """
        deprecation.deprecated_warning(
            "Method", "upload_data", replacement="set_data", since_version="1.9"
        )
        return self.submit("updateStoredData", field, data)

    def upload_data_if_needed(self, field, data):
        """Upload data only if it is a numpy array or a list"""
        deprecation.deprecated_warning(
            "Method",
            "upload_data_if_needed",
            replacement="set_data",
            since_version="1.9",
        )
        if isinstance(data, (numpy.ndarray, list)):
            self.submit("updateStoredData", field, data)
            return field
        else:
            return data

    def add_data(self, data, field="default"):
        # Get fields
        deprecation.deprecated_warning(
            "Method", "add_data", replacement="set_data", since_version="1.9"
        )
        if isinstance(data, dict):
            fields = list(data)
        else:
            fields = numpy.array(data).dtype.fields
        # Single data
        if fields is None:
            data_dict = dict([(field, data)])
        # Multiple data
        else:
            data_dict = dict((field, data[field]) for field in fields)
        # Send data
        for field, value in data_dict.items():
            self.upload_data(field, value)
        # Return data dict
        return data_dict

    def remove_data(self, field):
        self.submit("removeStoredData", field)

    def select_data(self, *names, **kwargs):
        deprecation.deprecated_warning(
            "Method",
            "select_data",
            replacement="set_data/add_curve/add_curve_item/set_data",
            since_version="1.9",
        )
        self.submit("selectStoredData", *names, **kwargs)

    def deselect_data(self, *names):
        deprecation.deprecated_warning(
            "Method",
            "deselect_data",
            replacement="set_data/add_curve/add_curve_item",
            since_version="1.9",
        )
        self.submit("deselectStoredData", *names)

    def clear_data(self):
        self.submit("clear")

    def get_data(self, field=None):
        return self.submit("getStoredData", field=field)


# Plot classes


class Plot1D(_DataPlot):

    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.silx_plots.Plot1D"

    # Available name to identify this plot
    ALIASES = ["curve", "plot1d"]

    def update_axis_marker(
        self, unique_name: str, channel_name, position: float, text: str
    ):
        """
        Display a vertical marker for a specific x-axis channel name.

        Arguments:
            unique_name: Unique name identifying this marker
            channel_name: X-axis name in which the marker have to be displayed (for example `axis:foo`)
                          The marker will only be displayed if the actual plot's x-axis is this channel
            position: Position of this marker in the `channel_name` axis
            text: Text to display with the marker
        """
        self._flint.update_axis_marker(
            self._plot_id, unique_name, channel_name, position, text
        )

    def add_curve(self, x, y, **kwargs):
        """
        Create a curve in this plot.
        """
        if x is None:
            x = numpy.arange(len(y))
        if y is None:
            raise ValueError("A y value is expected. None found.")
        self.submit("addCurve", x, y, **kwargs)

    @property
    def xscale(self):
        """
        Scale of the x-axis of this plot.

        The value is one of "linear", "log"
        """
        return self.submit("getXAxisScale")

    @xscale.setter
    def xscale(self, scale):
        self.submit("setXAxisScale", scale)

    @property
    def yscale(self):
        """
        Scale of the y-axis of this plot.

        The value is one of "linear", "log"
        """
        return self.submit("getYAxisScale")

    @yscale.setter
    def yscale(self, scale):
        self.submit("setYAxisScale", scale)

    def set_xaxis_scale(self, value):
        """
        Set the X-axis scale of this plot.

        Deprecated in BLISS 1.10. prefer using `xscale` property

        Argument:
            value: One of "linear" or "log"
        """
        self.xscale = value

    def set_yaxis_scale(self, value):
        """
        Set the Y-axis scale of this plot.

        Deprecated in BLISS 1.10. prefer using `xscale` property

        Argument:
            value: One of "linear" or "log"
        """
        self.yscale = value

    def clear_items(self):
        """Remove all the items described in this plot

        If no transaction was open, it will update the plot and refresh the plot
        view.
        """
        self.submit("clearItems")

    def add_curve_item(self, xname: str, yname: str, legend: str = None, **kwargs):
        """Define a specific curve item

        If no transaction was open, it will update the plot and refresh the plot
        view.
        """
        self.submit("addCurveItem", xname, yname, legend=legend, **kwargs)

    def remove_item(self, legend: str):
        """Remove a specific item.

        If no transaction was open, it will update the plot and refresh the plot
        view.
        """
        self.submit("removeItem", legend)

    def item_exists(self, legend: str):
        """True if a specific item exists."""
        return self.submit("itemExists", legend)

    def set_data(self, **kwargs):
        """Set data named from keys with associated values.

        If no transaction was open, it will update the plot and refresh the plot
        view.
        """
        self.submit("setData", **kwargs)

    def append_data(self, **kwargs):
        """Append data named from keys with associated values.

        If no transaction was open, it will update the plot and refresh the plot
        view.
        """
        self.submit("appendData", **kwargs)

    @contextlib.contextmanager
    def transaction(self, resetzoom=True):
        """Context manager to handle a set of changes and a single refresh of
        the plot. This is needed cause the action are done on the plot
        asynchronously"""
        self.submit("setAutoUpdatePlot", False)
        try:
            yield
        finally:
            self.submit("setAutoUpdatePlot", True)
            self.submit("updatePlot", resetzoom=resetzoom)


class ScatterView(_DataPlot):

    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.silx_plots.ScatterView"

    # Available name to identify this plot
    ALIASES = ["scatter"]

    def _init(self):
        # Make it public
        self.set_colormap = self._set_colormap

    def set_data(self, x, y, value, resetzoom=True, **kwargs):
        if x is None or y is None or value is None:
            self.clear_data()
        else:
            self.submit("setData", x, y, value, resetzoom=resetzoom, **kwargs)


class ScatterView3D(_DataPlot):

    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.silx_plots.ScatterView3D"

    # Available name to identify this plot
    ALIASES = ["scatter3d"]

    def _init(self):
        # Make it public
        self.set_colormap = self._set_colormap

    def set_marker(self, symbol):
        """
        Set the kind of marker to use for scatters.

        Attributes:
            symbol: One of '.', ',', 'o'.
        """
        self.submit("setMarker", symbol)

    def set_data(self, x, y, z, value):
        if x is None or y is None or z is None or value is None:
            self.clear_data()
        else:
            self.submit("setData", x, y, z, value)


class Plot2D(_DataPlot):

    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.silx_plots.Plot2D"

    # Available name to identify this plot
    ALIASES = ["plot2d"]

    def _init(self):
        # Make it public
        self.set_colormap = self._set_colormap

    def _init_plot(self):
        super(Plot2D, self)._init_plot()
        self.submit("setKeepDataAspectRatio", True)
        self.submit("setDisplayedIntensityHistogram", True)

    @property
    def yaxis_direction(self) -> str:
        """Direction of the y-axis.

        One of "up", "down"
        """
        return self.submit("getYaxisDirection")

    @yaxis_direction.setter
    def yaxis_direction(self, direction: str):
        self.submit("setYaxisDirection", direction)

    def add_image(self, data, **kwargs):
        self.submit("addImage", data, **kwargs)

    def select_mask(self, initial_mask: numpy.ndarray = None, directory: str = None):
        """Request a mask image from user selection.

        Argument:
            initial_mask: An initial mask image, else None
            directory: Directory used to import/export masks

        Return:
            A numpy array containing the user mask image
        """
        flint = self._flint
        request_id = flint.request_select_mask_image(
            self._plot_id, initial_mask, directory=directory
        )
        return self._wait_for_user_selection(request_id)


class Plot3D(_DataPlot):

    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.silx_plots.Plot3D"

    # Available name to identify this plot
    ALIASES = ["3d", "plot3d"]

    def add_scatter_item(
        self,
        x: str,
        y: str,
        z: str,
        v: str,
        legend: str = None,
        symbol: str = ",",
        symbol_size=None,
        lut=None,
        vmin=None,
        vmax=None,
    ):
        """
        Create a scatter item in the plot.
        """
        self.submit(
            "addScatterItem",
            x,
            y,
            z,
            v,
            legend=legend,
            symbol=symbol,
            symbolSize=symbol_size,
            lut=lut,
            vmin=vmin,
            vmax=vmax,
        )

    def add_mesh_item(
        self,
        vertices: str,
        faces: str,
        legend: str = None,
        color: numpy.ndarray = None,
    ):
        """
        Create a mesh item in the plot.
        """
        self.submit(
            "addMeshItem", vertices=vertices, faces=faces, legend=legend, color=color
        )

    def clear_items(self):
        """Remove all the items described in this plot

        If no transaction was open, it will update the plot and refresh the plot
        view.
        """
        self.submit("clearItems")

    def reset_zoom(self):
        """Reset the zoom of the camera."""
        self.submit("resetZoom")

    def remove_item(self, legend: str):
        """Remove a specific item.

        If no transaction was open, it will update the plot and refresh the plot
        view.
        """
        self.submit("removeItem", legend)

    def set_data(self, **kwargs):
        """Set data named from keys with associated values.

        If no transaction was open, it will update the plot and refresh the plot
        view.
        """
        self.submit("setData", **kwargs)

    @contextlib.contextmanager
    def transaction(self, resetzoom=True):
        """Context manager to handle a set of changes and a single refresh of
        the plot. This is needed cause the action are done on the plot
        asynchronously"""
        self.submit("setAutoUpdatePlot", False)
        try:
            yield
        finally:
            self.submit("setAutoUpdatePlot", True)
            self.submit("updatePlot", resetzoom=resetzoom)


class CurveStack(BasePlot):
    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.curve_stack.CurveStack"

    # Available name to identify this plot
    ALIASES = ["curvestack"]

    def set_data(self, curves, x=None, reset_zoom=None):
        """
        Set the data displayed in this plot.

        Arguments:
            curves: The data of the curves (first dim is curve index, second dim
                    is the x index)
            x: Mapping of the real X axis values to use
            reset_zoom: If True force reset zoom, else the user selection is
                        applied
        """
        self.submit("setData", data=curves, x=x, resetZoom=reset_zoom)

    def clear_data(self):
        self.submit("clear")


class TimeCurvePlot(BasePlot):
    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.time_curve_plot.TimeCurvePlot"

    # Available name to identify this plot
    ALIASES = ["timecurveplot"]

    def select_x_axis(self, name: str):
        """
        Select the x-axis to use

        Arguments:
            name: Name of the data to use as x-axis
        """
        self.submit("setXName", name)

    @property
    def xaxis_duration(self):
        return self.submit("xDuration")

    @xaxis_duration.setter
    def xaxis_duration(self, second: int):
        """
        Select the x-axis duration in second

        Arguments:
            second: Amount of seconds displayed in the x-axis
        """
        self.submit("setXDuration", second)

    def select_x_duration(self, second: int):
        """
        Select the x-axis duration in second

        Arguments:
            second: Amount of seconds displayed in the x-axis
        """
        self.xaxis_duration = second

    @property
    def ttl(self):
        return self.submit("ttl")

    @ttl.setter
    def ttl(self, second: int):
        """
        Set the time to live of the data.

        After this period of time, a received data is not anymore displayable
        in Flint.

        Arguments:
            second: Amount of seconds a data will live
        """
        self.submit("setTtl", second)

    def add_time_curve_item(self, yname, **kwargs):
        """
        Select a dedicated data to be displayed against the time.

        Arguments:
            name: Name of the data to use as y-axis
            kwargs: Associated style (see `addCurve` from silx plot)
        """
        self.submit("addTimeCurveItem", yname, **kwargs)

    def set_data(self, **kwargs):
        """
        Set the data displayed in this plot.

        Arguments:
            kwargs: Name of the data associated to the new numpy array to use
        """
        self.submit("setData", **kwargs)

    def append_data(self, **kwargs):
        """
        Append the data displayed in this plot.

        Arguments:
            kwargs: Name of the data associated to the numpy array to append
        """
        self.submit("appendData", **kwargs)

    def clear_data(self):
        self.submit("clear")


class ImageView(_DataPlot):

    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.silx_plots.ImageView"

    # Available name to identify this plot
    ALIASES = ["image", "imageview", "histogramimage"]

    def _init(self):
        # Make it public
        self.set_colormap = self._set_colormap

    def _init_plot(self):
        super(ImageView, self)._init_plot()
        self.submit("setKeepDataAspectRatio", True)
        self.submit("setDisplayedIntensityHistogram", True)

    @property
    def yaxis_direction(self) -> str:
        """Direction of the y-axis.

        One of "up", "down"
        """
        return self.submit("getYaxisDirection")

    @yaxis_direction.setter
    def yaxis_direction(self, direction: str):
        self.submit("setYaxisDirection", direction)

    def set_data(self, data, **kwargs):
        if "origin" in kwargs:
            if kwargs["origin"] is None:
                # Enforce the silx default
                del kwargs["origin"]
        if "scale" in kwargs:
            if kwargs["scale"] is None:
                # Enforce the silx default
                del kwargs["scale"]
        self.submit("setImage", data, **kwargs)

    @property
    def side_histogram_displayed(self) -> bool:
        return self.submit("isSideHistogramDisplayed")

    @side_histogram_displayed.setter
    def side_histogram_displayed(self, displayed: bool):
        self.submit("setSideHistogramDisplayed", displayed)


class StackView(_DataPlot):

    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.silx_plots.StackImageView"

    # Available name to identify this plot
    ALIASES = ["stack", "imagestack", "stackview"]

    def _init(self):
        # Make it public
        self.set_colormap = self._set_colormap

    def set_data(self, data, **kwargs):
        self.submit("setStack", data, **kwargs)


class LiveCurvePlot(BasePlot):

    WIDGET = None

    ALIASES = ["curve"]

    def update_user_data(
        self, unique_name: str, channel_name: str, ydata: Optional[numpy.ndarray]
    ):
        """Add user data to a live plot.

        It will define a curve in the plot using the y-data provided and the
        x-data from the parent item (defined by the `channel_name`)

        The key `unique_name` + `channel_name` is unique. So if it already
        exists the item will be updated.

        Arguments:
            unique_name: Name of this item in the property tree
            channel_name: Name of the channel that will be used as parent for
                this item. If this parent item does not exist, it is created
                but set hidden.
            ydata: Y-data for this item. If `None`, if the item already exists,
                it is removed from the plot
        """
        if ydata is not None:
            ydata = numpy.asarray(ydata)
        self._flint.update_user_data(self._plot_id, unique_name, channel_name, ydata)

    def update_axis_marker(
        self, unique_name: str, channel_name, position: float, text: str
    ):
        """
        Display a vertical marker for a specific x-axis channel name.

        Arguments:
            unique_name: Unique name identifying this marker
            channel_name: X-axis name in which the marker have to be displayed (for example `axis:foo`)
                          The marker will only be displayed if the actual plot's x-axis is this channel
            position: Position of this marker in the `channel_name` axis
            text: Text to display with the marker
        """
        self._flint.update_axis_marker(
            self._plot_id, unique_name, channel_name, position, text
        )

    @property
    def xscale(self):
        """
        Scale of the x-axis of this plot.

        The value is one of "linear", "log"
        """
        return self.submit("getXAxisScale")

    @xscale.setter
    def xscale(self, scale):
        self.submit("setXAxisScale", scale)

    @property
    def yscale(self):
        """
        Scale of the y-axis of this plot.

        The value is one of "linear", "log"
        """
        return self.submit("getYAxisScale")

    @yscale.setter
    def yscale(self, scale):
        self.submit("setYAxisScale", scale)

    @property
    def xaxis_channel_name(self):
        """Returns the channel name used as x-axis, else None"""
        return self.submit("getXAxisChannelName")


class LiveImagePlot(BasePlot):

    WIDGET = None

    ALIASES = ["image"]

    def _init(self):
        # Make it public
        self.set_colormap = self._set_colormap

    def update_marker(
        self,
        unique_name: str,
        position: Optional[Tuple[float, float]] = None,
        text: Optional[str] = None,
        editable: Optional[bool] = None,
    ):
        """
        Create or update a marker into the image.

        Arguments:
            unique_name: Unique name identifying this marker
            position: X and Y position in the image, else None to remove the marker
            text: Text to display with the marker
            editable: If true, the marker can be moved with the mouse
        """
        self.submit(
            "updateMarker",
            uniqueName=unique_name,
            position=position,
            text=text,
            editable=editable,
        )

    def remove_marker(self, unique_name: str):
        """
        Remove a marker already existing.

        If the marker is not there, no feedback is returned.

        Arguments:
            unique_name: Unique name identifying this marker
        """
        self.submit("removeMarker", uniqueName=unique_name)

    def marker_position(self, unique_name: str) -> Optional[Tuple[float, float]]:
        """
        Create or update a marker into the image.

        Arguments:
            unique_name: Unique name identifying this marker

        Returns:
            The position of the marker, else None if the marker does not exist
        """
        p = self.submit("markerPosition", uniqueName=unique_name)
        if p is None:
            return None
        # FIXME: the RPC returns a list instead of a tuple
        return tuple(p)


class LiveScatterPlot(BasePlot):

    WIDGET = None

    ALIASES = ["scatter"]

    def _init(self):
        # Make it public
        self.set_colormap = self._set_colormap

    @property
    def xaxis_channel_name(self):
        """Returns the channel name used as x-axis, else None"""
        return self.submit("getXAxisChannelName")

    @property
    def yaxis_channel_name(self):
        """Returns the channel name used as y-axis, else None"""
        return self.submit("getYAxisChannelName")


class LiveMcaPlot(BasePlot):

    WIDGET = None

    ALIASES = ["mca"]


class LiveOneDimPlot(BasePlot):

    WIDGET = None

    ALIASES = ["onedim"]


class SpectroPlot(BasePlot):
    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.spectro_plot.SpectroPlot"

    # Available name to identify this plot
    ALIASES = ["spectroplot"]

    def set_data(self, **kwargs):
        """
        Set the data displayed in this plot.

        Arguments:
            kwargs: Name of the data associated to the new numpy array to use
        """
        self.submit("setData", **kwargs)

    def add_data(self, **kwargs):
        self.submit("addData", **kwargs)

    def clear_data(self):
        self.submit("clear")

    def refresh(self):
        self.submit("refresh")

    def set_box_min_max(self, mini, maxi):
        self.submit("setBoxMinMax", mini, maxi)


class GridContainer(_DataPlot):

    # Name of the corresponding silx widget
    WIDGET = "bliss.flint.custom_plots.grid_container.GridContainer"

    # Available name to identify this plot
    ALIASES = ["grid"]

    def get_plot(
        self,
        plot_class: typing.Union[str, object],
        name: str = None,
        unique_name: str = None,
        selected: bool = False,
        closeable: bool = True,
        row: int = None,
        col: int = None,
        row_span: int = None,
        col_span: int = None,
    ):
        """Create or retrieve a plot from this flint instance.

        If the plot does not exists, it will be created in a new tab on Flint.

        Arguments:
            plot_class: A class defined in `bliss.flint.client.plot`, or a
                silx class name. Can be one of "Plot1D", "Plot2D", "ImageView",
                "StackView", "ScatterView".
            name: Not applicable for this container
            unique_name: If defined the plot can be retrieved from flint.
            selected: Not applicable for this container
            closeable: Not applicable for this container
            row: Row number where to place the new widget
            col: Column number where to place the new widget
            row_span: Number of rows to use to place the new widget
            col_span: Number of columns to use to place the new widget
        """
        return self._flint.get_plot(
            plot_class=plot_class,
            name=name,
            selected=selected,
            closeable=closeable,
            unique_name=unique_name,
            parent_id=self._plot_id,
            parent_layout_params=(row, col, row_span, col_span),
        )


CUSTOM_CLASSES = [
    Plot1D,
    Plot2D,
    Plot3D,
    ScatterView,
    ScatterView3D,
    ImageView,
    StackView,
    CurveStack,
    TimeCurvePlot,
    SpectroPlot,
    GridContainer,
]

LIVE_CLASSES = [
    LiveCurvePlot,
    LiveImagePlot,
    LiveScatterPlot,
    LiveMcaPlot,
    LiveOneDimPlot,
]

# For compatibility
CurvePlot = Plot1D
ImagePlot = Plot2D
ScatterPlot = ScatterView
HistogramImagePlot = ImageView
ImageStackPlot = StackView
