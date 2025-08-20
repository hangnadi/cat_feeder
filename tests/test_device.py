from feeder.device import DeviceState

def test_device_dispense_logic():
    d = DeviceState(hopper_capacity_g=500, remaining_g=500)
    ok, _ = d.can_dispense(100)
    assert ok
    d.dispense(100)
    assert d.remaining_g == 400
    assert d.feeds_today == 1
