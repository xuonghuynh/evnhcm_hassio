import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from datetime import timedelta
from . import evnhcm
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

CONF_MA = "makhach"
CONF_PASS = "matkhau"
CONF_DATE = "day"

ICON = "mdi:flash"

TIME_BETWEEN_UPDATES = timedelta(minutes=30)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=" "): cv.string,
        vol.Optional(CONF_PASS, default='1234567890'): cv.string,
        vol.Optional(CONF_MA, default='xxx'): cv.string,
        vol.Optional(CONF_DATE, default='1'): cv.string,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Version sensor platform."""

    name = config.get(CONF_NAME)
    matkhau = config.get(CONF_PASS)
    makhach = config.get(CONF_MA)
    date = config.get(CONF_DATE)

    #get session HA
    #session = async_get_clientsession(hass)

    #call xu ly data
    bill_data = BillData(evnhcm.HassioVersion(name, matkhau , makhach, date))
    total_bill_data = TotalBillData(evnhcm.HassioVersion(name, matkhau , makhach, date))

    async_add_entities([VersionSensor(bill_data, 'evnhcm'), VersionSensor(total_bill_data, 'evnhcm_tien_thang')], True)

class BillData:
    """Get the latest data and update the states."""

    def __init__(self, vnhass):
        """Initialize the data object."""
        self.vnhass = vnhass

    @Throttle(TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest version information."""
        self.vnhass.bill_data()
class TotalBillData:
    """Get the latest data and update the states."""

    def __init__(self, vnhass):
        """Initialize the data object."""
        self.vnhass = vnhass

    @Throttle(TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest version information."""
        self.vnhass.total_bill_data()
class VersionSensor(Entity):
    """Representation of a Home Assistant version sensor."""

    def __init__(self, haversion, name):
        """Initialize the Version sensor."""
        self.haversion = haversion
        self._name = name
        self._state = None

    def update(self):
        """Get the latest version information."""
        self.haversion.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    # @property
    # def device_class(self):
    #     """Return the name of the sensor."""
    #     return 'energy'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.haversion.vnhass.state

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return self.haversion.vnhass.attribute

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    # @property
    # def unit_of_measurement(self):
    #     """Return the unit of measurement."""
    #     return 'kWh'

