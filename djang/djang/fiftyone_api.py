# pip install fiftyone-devicedetection

from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from fiftyone_pipeline_cloudrequestengine.cloudrequestengine import CloudRequestEngine
from fiftyone_devicedetection.devicedetection_pipelinebuilder import DeviceDetectionCloud

# Function to read the property values.
def check_property(property):
    if property.has_value():
        return str(property.value())
    return property.no_value_message()

# Create the engines required.
cloudRequestEngine = CloudRequestEngine({"resource_key": "AQSZCf4SD7B8OXoc2kg"})
deviceDetectionCloudEngine = DeviceDetectionCloud()

# Create a simple pipeline to access the engine with.
pipeline = PipelineBuilder() \
    .add(cloudRequestEngine) \
    .add(deviceDetectionCloudEngine) \
    .build()

def main( request ):

    # Create the flow data object.
    flowData = pipeline.create_flowdata()

    # Add evidence to the flow data.
    flowData.evidence.add("head.user-agent", request.headers['User-Agent'])

    # Process the flowdata.
    flowData.process()


    data = { "devicetype" : check_property(flowData.device.devicetype),
    "hardwarevendor" : check_property(flowData.device.hardwarevendor),
    "browsername" : check_property(flowData.device.browsername),
    "priceband" : check_property(flowData.device.priceband),
    "releaseage" : check_property(flowData.device.releaseage) }

    return data