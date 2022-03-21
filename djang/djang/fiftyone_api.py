
# pip install fiftyone-devicedetection
# pip install fiftyone-location

from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from fiftyone_pipeline_cloudrequestengine.cloudrequestengine import CloudRequestEngine
from fiftyone_devicedetection.devicedetection_pipelinebuilder import DeviceDetectionCloud
from fiftyone_location.location_pipelinebuilder import LocationCloud

# Function to read the property values.
def check_property(property):
    if property.has_value():
        return str(property.value())
    return property.no_value_message()

# Create the engines required.
cloudRequestEngine = CloudRequestEngine({"resource_key": "AQRoCk2bbGnvyKYK2kg"})
deviceDetectionCloudEngine = DeviceDetectionCloud()
fodLocationCloudEngine = LocationCloud({"locationProvider": "fiftyonedegrees"})

# Create a simple pipeline to access the engine with.
pipeline = PipelineBuilder() \
    .add(cloudRequestEngine) \
    .add(deviceDetectionCloudEngine) \
    .add(fodLocationCloudEngine) \
    .build()


def main( request ):

    # Create the flow data object.
    flowData = pipeline.create_flowdata()

    # Add evidence to the flow data.
    flowData.evidence.add("header.user-agent", 
                    "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G960U) " +
                    "AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/10.1 " +
                    "Chrome/71.0.3578.99 Mobile Safari/537.36")
    flowData.evidence.add("query.51D_Pos_latitude", "51.458048")
    flowData.evidence.add("query.51D_Pos_longitude", "-0.9822207999999999")

    # Process the flowdata.
    flowData.process()

    # Retreive the properties.
    print("device.DeviceType: " + check_property(flowData.device.devicetype))
    print("device.SetHeaderHardwareAccept-CH: " + check_property(flowData.device.get_internal('setheaderhardwareaccept-ch')))
    print("device.SetHeaderBrowserAccept-CH: " + check_property(flowData.device.get_internal('setheaderbrowseraccept-ch')))
    print("device.HardwareName: " + check_property(flowData.device.hardwarename))
    print("device.HardwareModel: " + check_property(flowData.device.hardwaremodel))
    print("device.HardwareVendor: " + check_property(flowData.device.hardwarevendor))
    print("device.IsMobile: " + check_property(flowData.device.ismobile))
    print("device.PlatformVendor: " + check_property(flowData.device.platformvendor))
    print("device.SetHeaderPlatformAccept-CH: " + check_property(flowData.device.get_internal('setheaderplatformaccept-ch')))
    print("device.PlatformName: " + check_property(flowData.device.platformname))
    print("device.PlatformVersion: " + check_property(flowData.device.platformversion))
    print("device.PlatformRank: " + check_property(flowData.device.platformrank))
    print("device.BrowserVendor: " + check_property(flowData.device.browservendor))
    print("device.BrowserName: " + check_property(flowData.device.browsername))
    print("device.BrowserVersion: " + check_property(flowData.device.browserversion))
    print("location.Town: " + check_property(flowData.location.town))
    print("location.Country: " + check_property(flowData.location.country))
    print("location.County: " + check_property(flowData.location.county))
    print("location.Region: " + check_property(flowData.location.region))
    print("location.State: " + check_property(flowData.location.state))