import logging
import os

import voluptuous as vol

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME, CONF_RESOURCE, CONF_UNIT_OF_MEASUREMENT,
    CONF_VALUE_TEMPLATE )
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_ATTR = 'attribute'
CONF_SELECT = 'select'

DEFAULT_NAME = 'Web scrape2'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_RESOURCE): cv.string,
    vol.Required(CONF_SELECT): cv.string,
    vol.Optional(CONF_ATTR): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_VALUE_TEMPLATE): cv.template
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Web scrape sensor."""
    name = config.get(CONF_NAME)
    resource = config.get(CONF_RESOURCE)
    select = config.get(CONF_SELECT)
    attr = config.get(CONF_ATTR)
    unit = config.get(CONF_UNIT_OF_MEASUREMENT)
    value_template = config.get(CONF_VALUE_TEMPLATE)
    if value_template is not None:
        value_template.hass = hass

    if os.path.exists("/usr/lib/chromium/chromedriver"):
        driver = "/usr/lib/chromium/chromedriver"
    elif os.path.exists("/usr/lib/chromium-browser/chromedriver"):
        driver = "/usr/lib/chromium-browser/chromedriver"
    else:
        _LOGGER.error("chromedriver hasn't been installed")
        return False

    add_entities([
        Scrape2Sensor(resource, name, select, attr, value_template, unit, driver)], True)


class Scrape2Sensor(Entity):
    """Representation of a web scrape sensor."""

    def __init__(self, resource, name, select, attr, value_template, unit, driver):
        """Initialize a web scrape sensor."""
        self._resource = resource
        self._name = name
        self._state = None
        self._select = select
        self._attr = attr
        self._value_template = value_template
        self._unit_of_measurement = unit
        self._driver = driver

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def update(self):
        """Get the latest data from the source and updates the state."""

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-using")
        driver = webdriver.Chrome(self._driver, options=chrome_options)
        driver.get( self._resource)
        innerHTML = driver.execute_script("return document.body.innerHTML")
        driver.quit()

        raw_data = BeautifulSoup(innerHTML, 'html.parser')
        _LOGGER.debug(raw_data)

        try:
            if self._attr is not None:
                value = raw_data.select(self._select)[0][self._attr]
            else:
                value = raw_data.select(self._select)[0].text
            _LOGGER.debug(value)
        except IndexError:
            _LOGGER.error("Unable to extract data from HTML")
            return

        if self._value_template is not None:
            self._state = self._value_template.render_with_possible_json_value(
                value, None)
        else:
            self._state = value
