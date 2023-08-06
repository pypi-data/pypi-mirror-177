"""An NMR control component."""
from flowchem.components.base_component import FlowchemComponent
from flowchem.devices.flowchem_device import FlowchemDevice


class NMRControl(FlowchemComponent):
    def __init__(self, name: str, hw_device: FlowchemDevice):
        """NMR Control component."""
        super().__init__(name, hw_device)
        self.add_api_route("/acquire-spectrum", self.acquire_spectrum, methods=["PUT"])
        self.add_api_route("/stop", self.stop, methods=["PUT"])

        # Ontology: fourier transformation NMR instrument
        self.metadata.owl_subclass_of = "http://purl.obolibrary.org/obo/OBI_0000487"

    async def acquire_spectrum(self):
        """Acquire an NMR spectrum."""
        ...

    async def stop(self):
        """Stops acquisition and exit gracefully."""
        ...
