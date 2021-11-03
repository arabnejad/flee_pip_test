from flee import flee
from flee.datamanager import handle_refugee_data
import numpy as np
import flee.postprocessing.analysis as a

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""


def test_removelink():
    print("Testing basic data handling and simulation kernel.")

    end_time = 80
    e = flee.Ecosystem()

    l1 = e.addLocation(name="A", movechance=0.3)

    l2 = e.addLocation(name="B", movechance=0.0)
    l3 = e.addLocation(name="C", movechance=0.0)
    l4 = e.addLocation(name="D", movechance=0.0)

    e.linkUp(endpoint1="A", endpoint2="B", distance=834.0)
    e.linkUp(endpoint1="A", endpoint2="C", distance=1368.0)
    e.linkUp(endpoint1="A", endpoint2="D", distance=536.0)

    assert e.remove_link(startpoint="A", endpoint="C")

    print("Test successful!")


if __name__ == "__main__":
    test_removelink()
