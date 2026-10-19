import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import light
from esphome.const import CONF_OUTPUT_ID

from . import Aip33628Panel, aip33628_ns

DEPENDENCIES = ["aip33628"]

Aip33628Light = aip33628_ns.class_("Aip33628Light", light.LightOutput)
LightType = aip33628_ns.enum("LightType", is_class=True)

CONF_AIP33628_ID = "aip33628_id"
CONF_TYPE = "type"

CONFIG_SCHEMA = light.RGB_LIGHT_SCHEMA.extend(
    {
        cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(Aip33628Light),
        cv.GenerateID(CONF_AIP33628_ID): cv.use_id(Aip33628Panel),
        cv.Optional(CONF_TYPE, default="display"): cv.one_of("display", "date_dash", "am_pm", lower=True),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    await light.register_light(var, config)

    panel = await cg.get_variable(config[CONF_AIP33628_ID])
    cg.add(var.set_panel(panel))
    if config[CONF_TYPE] == "date_dash":
        cg.add(var.set_type(LightType.DATE_DASH))
    elif config[CONF_TYPE] == "am_pm":
        cg.add(var.set_type(LightType.AM_PM))
    else:
        cg.add(var.set_type(LightType.PANEL))
