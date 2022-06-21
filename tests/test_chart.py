"""
A test module used to test
chart module
"""

import abc
import unittest
import unittest.mock
from typing import Callable

from normalizer import Normalizer
from ipyvizzu import Chart, ChartProperty, Data, Config, Snapshot, Style
from ipyvizzu.event import EventHandler


class TestChart(unittest.TestCase, abc.ABC):
    """
    An abstract test class used to test
    chart.Chart()
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.normalizer = Normalizer()

    def setUp(self) -> None:
        self.patch = unittest.mock.patch(self.get_mock())
        self.trash = self.patch.start()
        self.chart = Chart()

    def tearDown(self) -> None:
        self.patch.stop()

    def get_mock(self) -> str:
        """
        A method used to return
        mocked method's name
        """
        return "ipyvizzu.chart.display_javascript"


class TestChartInit(TestChart):
    """
    A test class used to test
    the initialization of Chart()
    """

    def test_init(self) -> None:
        """
        A test method used to test
        Chart() with default constructor parameters
        """
        with unittest.mock.patch(self.get_mock()) as output:
            Chart()
            self.assertEqual(
                self.normalizer.normalize_output(output, 1),
                "window.ipyvizzu.createChart("
                + "element, "
                + "id, "
                + "'https://cdn.jsdelivr.net/npm/vizzu@~0.4.0/dist/vizzu.min.js', "
                + "'800px', '480px');",
            )

    def test_init_vizzu(self) -> None:
        """
        A test method used to test
        Chart()'s vizzu constructor parameter
        """
        with unittest.mock.patch(self.get_mock()) as output:
            Chart(vizzu="https://cdn.jsdelivr.net/npm/vizzu@0.4.1/dist/vizzu.min.js")
            self.assertEqual(
                self.normalizer.normalize_output(output, 1),
                "window.ipyvizzu.createChart("
                + "element, "
                + "id, "
                + "'https://cdn.jsdelivr.net/npm/vizzu@0.4.1/dist/vizzu.min.js', "
                + "'800px', '480px');",
            )

    def test_init_div(self) -> None:
        """
        A test method used to test
        Chart()'s width and height constructor parameters
        """
        with unittest.mock.patch(self.get_mock()) as output:
            Chart(width="400px", height="240px")
            self.assertEqual(
                self.normalizer.normalize_output(output, 1),
                "window.ipyvizzu.createChart("
                + "element, "
                + "id, "
                + "'https://cdn.jsdelivr.net/npm/vizzu@~0.4.0/dist/vizzu.min.js', "
                + "'400px', '240px');",
            )

    def test_init_display_invalid(self) -> None:
        """
        A test method used to test
        Chart()'s display constructor parameter with an invalid value
        """
        with self.assertRaises(ValueError):
            Chart(display="invalid")

    def test_init_display_begin(self) -> None:
        """
        A test method used to test
        Chart()'s display constructor parameter with the begin value
        """
        self.chart = Chart(display="begin")
        with unittest.mock.patch(self.get_mock()) as output:
            self.chart.animate(Snapshot("abc1234"))
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'begin', false, "
                + "id, "
                + "undefined);",
            )

    def test_init_display_actual(self) -> None:
        """
        A test method used to test
        Chart()'s display constructor parameter with the actual value
        """
        self.chart = Chart(display="actual")
        with unittest.mock.patch(self.get_mock()) as output:
            self.chart.animate(Snapshot("abc1234"))
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'actual', false, "
                + "id, "
                + "undefined);",
            )

    def test_init_display_end(self) -> None:
        """
        A test method used to test
        Chart()'s display constructor parameter with the end value
        """
        self.chart = Chart(display="end")
        with unittest.mock.patch(self.get_mock()) as output:
            self.chart.animate(Snapshot("abc1234"))
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'end', false, "
                + "id, "
                + "undefined);",
            )

    def test_init_register_events(self) -> None:
        """
        A test method used to test
        Chart()._register_events() method
        """

        class IPyEvents:
            """
            A class used to mock
            get_ipython().events object
            """

            @staticmethod
            def register(
                event: str, function: Callable  # pylint: disable=unused-argument
            ) -> None:
                """
                A method used to mock
                get_ipython().events.register() method
                """
                function()

        class IPy:
            """
            A class used to mock
            get_ipython() object
            """

            events = IPyEvents

        get_ipython_mock = "ipyvizzu.chart.get_ipython"
        with unittest.mock.patch(get_ipython_mock, return_value=IPy()):
            with unittest.mock.patch(self.get_mock()) as output:
                Chart()
                self.assertEqual(
                    self.normalizer.normalize_output(output, 2),
                    "if (window.IpyVizzu) { window.IpyVizzu.clearInhibitScroll(element); }",
                )


class TestChartMethods(TestChart):
    """
    A test class used to test
    the methods of the chart which are related to method module
    """

    def test_animate_chart_target_has_to_be_passed(self) -> None:
        """
        A test method used to test
        Chart().animate() method without arguments
        """
        with self.assertRaises(ValueError):
            self.chart.animate()

    def test_animate_chart_target_has_to_be_passed_even_if_chart_anim_opts_passed(
        self,
    ) -> None:
        """
        A test method used to test
        Chart().animate() method without chart target and with anim options
        """
        with self.assertRaises(ValueError):
            self.chart.animate(duration="500ms")

    def test_animate_one_chart_target(self) -> None:
        """
        A test method used to test
        Chart().animate() method with a chart target
        """
        with unittest.mock.patch(self.get_mock()) as output:
            data = Data()
            data.add_record(["Rock", "Hard", 96])
            self.chart.animate(data)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'actual', false, "
                + '{"data": {"records": [["Rock", "Hard", 96]]}}, '
                + "undefined);",
            )

    def test_animate_one_chart_target_with_chart_anim_opts(self) -> None:
        """
        A test method used to test
        Chart().animate() method with a chart target and anim options
        """
        with unittest.mock.patch(self.get_mock()) as output:
            data = Data()
            data.add_record(["Rock", "Hard", 96])
            self.chart.animate(data, duration="500ms")
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'actual', false, "
                + '{"data": {"records": [["Rock", "Hard", 96]]}}, '
                + '{"duration": "500ms"});',
            )

    def test_animate_snapshot_chart_target(self) -> None:
        """
        A test method used to test
        Chart().animate() method with a Snapshot chart target
        """
        with unittest.mock.patch(self.get_mock()) as output:
            snapshot = Snapshot("abc1234")
            self.chart.animate(snapshot)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'actual', false, "
                + "id, "
                + "undefined);",
            )

    def test_animate_snapshot_chart_target_with_chart_anim_opts(self) -> None:
        """
        A test method used to test
        Chart().animate() method with a Snapshot chart target and anim options
        """
        with unittest.mock.patch(self.get_mock()) as output:
            snapshot = Snapshot("abc1234")
            self.chart.animate(snapshot, duration="500ms")
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'actual', false, "
                + "id, "
                + '{"duration": "500ms"});',
            )

    def test_animate_more_chart_target(self) -> None:
        """
        A test method used to test
        Chart().animate() method with multiple chart targets
        """
        with unittest.mock.patch(self.get_mock()) as output:
            data = Data()
            data.add_record(["Rock", "Hard", 96])
            config = Config({"channels": {"label": {"attach": ["Popularity"]}}})
            style = Style({"title": {"backgroundColor": "#A0A0A0"}})
            self.chart.animate(data, config, style)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'actual', false, "
                + '{"data": {"records": [["Rock", "Hard", 96]]}, '
                + '"config": {"channels": {"label": {"attach": ["Popularity"]}}}, '
                + '"style": {"title": {"backgroundColor": "#A0A0A0"}}}, '
                + "undefined);",
            )

    def test_animate_more_chart_target_with_chart_anim_opts(self) -> None:
        """
        A test method used to test
        Chart().animate() method with multiple chart targets and anim options
        """
        with unittest.mock.patch(self.get_mock()) as output:
            data = Data()
            data.add_record(["Rock", "Hard", 96])
            config = Config({"channels": {"label": {"attach": ["Popularity"]}}})
            style = Style({"title": {"backgroundColor": "#A0A0A0"}})
            self.chart.animate(data, config, style, duration="500ms")
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'actual', false, "
                + '{"data": {"records": [["Rock", "Hard", 96]]}, '
                + '"config": {"channels": {"label": {"attach": ["Popularity"]}}}, '
                + '"style": {"title": {"backgroundColor": "#A0A0A0"}}}, '
                + '{"duration": "500ms"});',
            )

    def test_animate_more_chart_target_with_conflict(self) -> None:
        """
        A test method used to test
        Chart().animate() method with same chart targets
        """
        data = Data()
        data.add_record(["Rock", "Hard", 96])
        config1 = Config({"channels": {"label": {"attach": ["Popularity"]}}})
        config2 = Config({"title": "Test"})
        style = Style({"title": {"backgroundColor": "#A0A0A0"}})
        with self.assertRaises(ValueError):
            self.chart.animate(data, config1, style, config2)

    def test_animate_more_chart_target_with_snapshot(self) -> None:
        """
        A test method used to test
        Chart().animate() method with multiple chart targets and a Snapshot chart target
        """
        data = Data()
        data.add_record(["Rock", "Hard", 96])
        config = Config({"channels": {"label": {"attach": ["Popularity"]}}})
        style = Style({"title": {"backgroundColor": "#A0A0A0"}})
        snapshot = Snapshot("abc1234")
        with self.assertRaises(NotImplementedError):
            self.chart.animate(data, config, style, snapshot)

    def test_animate_more_calls(self) -> None:
        """
        A test method used to test
        multiple Chart().animate() methods
        """
        with unittest.mock.patch(self.get_mock()) as output:
            data = Data()
            data.add_record(["Rock", "Hard", 96])
            config1 = Config({"channels": {"label": {"attach": ["Popularity"]}}})
            config2 = Config({"title": "Test"})
            style = Style({"title": {"backgroundColor": "#A0A0A0"}})
            self.chart.animate(data, config1, style)
            self.chart.animate(config2)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'actual', false, "
                + '{"data": {"records": [["Rock", "Hard", 96]]}, '
                + '"config": {"channels": {"label": {"attach": ["Popularity"]}}}, '
                + '"style": {"title": {"backgroundColor": "#A0A0A0"}}}, '
                + "undefined);\n"
                + "window.ipyvizzu.animate(element, id, 'actual', false, "
                + '{"config": {"title": "Test"}}, '
                + "undefined);",
            )

    def test_animate_with_not_default_scroll_into_view(self) -> None:
        """
        A test method used to test
        Chart().animate() method with scroll into view
        """
        with unittest.mock.patch(self.get_mock()) as output:
            data = Data()
            data.add_record(["Rock", "Hard", 96])
            scroll_into_view = not self.chart.scroll_into_view
            self.chart.scroll_into_view = scroll_into_view
            self.chart.animate(data)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                f"window.ipyvizzu.animate(element, id, 'actual', {str(scroll_into_view).lower()}, "
                + '{"data": {"records": [["Rock", "Hard", 96]]}}, '
                + "undefined);",
            )

    def test_feature(self) -> None:
        """
        A test method used to test
        Chart.feature() method
        """
        with unittest.mock.patch(self.get_mock()) as output:
            self.chart.feature("tooltip", True)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                'window.ipyvizzu.feature(element, id, "tooltip", true);',
            )

    def test_store(self) -> None:
        """
        A test method used to test
        Chart.store() method
        """
        with unittest.mock.patch(self.get_mock()) as output:
            self.chart.store()
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.store(element, id, id);",
            )


class TestChartEvents(TestChart):
    """
    A test class used to test
    the methods of the Chart() which are related to events
    """

    def test_on(self) -> None:
        """
        A test method used to test
        Chart().on() method
        """
        with unittest.mock.patch(self.get_mock()) as output:
            handler_method = """event.renderingContext.fillStyle =
                (event.data.text === 'Jazz') ? 'red' : 'gray';"""
            self.chart.on("plot-axis-label-draw", handler_method)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.setEvent("
                + "element, id, id, 'plot-axis-label-draw', "
                + "event => "
                + "{ event.renderingContext.fillStyle = "
                + "(event.data.text === 'Jazz') ? 'red' : 'gray'; });",
            )

    def test_off(self) -> None:
        """
        A test method used to test
        Chart().off() method
        """
        with unittest.mock.patch(self.get_mock()) as output:
            handler_method = "alert(JSON.stringify(event.data));"
            handler = EventHandler("click", handler_method)
            self.chart.off(handler)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.clearEvent(element, id, id, 'click');",
            )


class TestChartLogs(TestChart):
    """
    A test class used to test
    the methods of the Chart() which are related to logging
    """

    def test_log_config(self) -> None:
        """
        A test method used to test
        Chart().log() method with config value
        """
        with unittest.mock.patch(self.get_mock()) as output:
            self.chart.log(ChartProperty.CONFIG)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.log(element, id, 'config');",
            )

    def test_log_style(self) -> None:
        """
        A test method used to test
        Chart().log() method with styles value
        """
        with unittest.mock.patch(self.get_mock()) as output:
            self.chart.log(ChartProperty.STYLE)
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.log(element, id, 'styles');",
            )

    def test_log_invalid(self) -> None:
        """
        A test method used to test
        Chart().log() method with an invalid value
        """
        with self.assertRaises(AttributeError):
            self.chart.log(ChartProperty.INVALID)  # pylint: disable=no-member


class TestChartDisplay(TestChart):
    """
    A test class used to test
    the methods of the chart which are related to display
    """

    def test_repr_html_if_display_is_not_manual(self) -> None:
        """
        A test method used to test
        Chart()._repr_html_() method if display is not manual
        """
        self.chart.animate(Snapshot("abc1234"))
        with self.assertRaises(AssertionError):
            self.chart._repr_html_()  # pylint: disable=protected-access

    def test_show_if_display_is_not_manual(self) -> None:
        """
        A test method used to test
        Chart().show() method if display is not manual
        """
        self.chart.animate(Snapshot("abc1234"))
        with self.assertRaises(AssertionError):
            self.chart.show()

    def test_repr_html(self) -> None:
        """
        A test method used to test
        Chart()._repr_html_() method if display is manual
        """
        self.chart = Chart(display="manual")
        display_mock = "ipyvizzu.Chart._display"
        with unittest.mock.patch(display_mock) as output:
            self.chart.animate(Snapshot("abc1234"))
            self.assertEqual(
                self.chart._showed,  # pylint: disable=protected-access
                False,
            )
            self.chart._repr_html_()  # pylint: disable=protected-access
            self.assertEqual(
                self.chart._showed,  # pylint: disable=protected-access
                True,
            )
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'manual', false, "
                + "id, "
                + "undefined);",
            )

    def test_show(self) -> None:
        """
        A test method used to test
        Chart().show() method if display is manual
        """
        self.chart = Chart(display="manual")
        display_mock = "ipyvizzu.Chart._display"
        with unittest.mock.patch(display_mock) as output:
            self.chart.animate(Snapshot("abc1234"))
            self.assertEqual(
                self.chart._showed,  # pylint: disable=protected-access
                False,
            )
            self.chart.show()
            self.assertEqual(
                self.chart._showed,  # pylint: disable=protected-access
                True,
            )
            self.assertEqual(
                self.normalizer.normalize_output(output),
                "window.ipyvizzu.animate(element, id, 'manual', false, "
                + "id, "
                + "undefined);",
            )

    def test_repr_html_after_repr_html(self) -> None:
        """
        A test method used to test
        Chart()._repr_html_() method after Chart()._repr_html_() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart._repr_html_()  # pylint: disable=protected-access
        with self.assertRaises(AssertionError):
            self.chart._repr_html_()  # pylint: disable=protected-access

    def test_repr_html_after_show(self) -> None:
        """
        A test method used to test
        Chart()._repr_html_() method after Chart().show() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart.show()
        with self.assertRaises(AssertionError):
            self.chart._repr_html_()  # pylint: disable=protected-access

    def test_show_after_show(self) -> None:
        """
        A test method used to test
        Chart().show() method after Chart().show() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart.show()
        with self.assertRaises(AssertionError):
            self.chart.show()

    def test_show_after_repr_html(self) -> None:
        """
        A test method used to test
        Chart().show() method after Chart()._repr_html_() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart._repr_html_()  # pylint: disable=protected-access
        with self.assertRaises(AssertionError):
            self.chart.show()

    def test_animate_after_repr_html(self) -> None:
        """
        A test method used to test
        Chart().animate() method after Chart()._repr_html_() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart._repr_html_()  # pylint: disable=protected-access
        with self.assertRaises(AssertionError):
            self.chart.animate(Snapshot("abc1234"))

    def test_animate_after_show(self) -> None:
        """
        A test method used to test
        Chart().animate() method after Chart().show() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart.show()
        with self.assertRaises(AssertionError):
            self.chart.animate(Snapshot("abc1234"))

    def test_feature_after_repr_html(self) -> None:
        """
        A test method used to test
        Chart().feature() method after Chart()._repr_html_() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart._repr_html_()  # pylint: disable=protected-access
        with self.assertRaises(AssertionError):
            self.chart.feature("tooltip", True)

    def test_feature_after_show(self) -> None:
        """
        A test method used to test
        Chart().feature() method after Chart().show() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart.show()
        with self.assertRaises(AssertionError):
            self.chart.feature("tooltip", True)

    def test_store_after_repr_html_(self) -> None:
        """
        A test method used to test
        Chart().store() method after Chart()._repr_html_() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart._repr_html_()  # pylint: disable=protected-access
        with self.assertRaises(AssertionError):
            self.chart.store()

    def test_store_after_show(self) -> None:
        """
        A test method used to test
        Chart().store() method after Chart().show() called
        """
        self.chart = Chart(display="manual")
        self.chart.animate(Snapshot("abc1234"))
        self.chart.show()
        with self.assertRaises(AssertionError):
            self.chart.store()
