import pytest

from robot.backends.dummy import DummyServoAssembly
from robot.servo import ServoBoard, Servo, GPIOPin, PinValue, PinMode, CommandError

def _get_dummy_servo_assembly():
    servo_assembly_backend = DummyServoAssembly()
    servo_assembly_frontend = ServoBoard("SERIAL", servo_assembly_backend)
    return servo_assembly_frontend, servo_assembly_backend


def test_servo_initialisation():
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    assert servo_assembly_frontend.serial == "SERIAL"
    assert len(servo_assembly_frontend.servos) == 4
    assert len(servo_assembly_frontend.pins) == 10


def test_servo_list():
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    for s in servo_assembly_frontend.servos:
        assert type(s) == Servo


def test_pin_list():
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    for p in servo_assembly_frontend.pins:
        assert type(p) == GPIOPin


def test_direct_valid_command():
    """Test a valid direct command."""
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    result = servo_assembly_frontend.direct_command("hello", "world")
    assert result == "helloworld"


def test_direct_invalid_command():
    """Test a invalid direct command."""
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    with pytest.raises(CommandError):
        servo_assembly_frontend.direct_command("expecting", "an", "error")


def test_read_ultrasound():
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    
    result = servo_assembly_frontend.read_ultrasound(1, 0)
    assert type(result) == float
    assert 0 < result


def test_pin_validation():
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()

    servo_assembly_frontend._validate_pin(3)
    with pytest.raises(ValueError):
        servo_assembly_frontend._validate_pin(-4)

    with pytest.raises(ValueError):
        servo_assembly_frontend._validate_pin(servo_assembly_frontend._num_pins + 1)


def test_servo_initialisation():
    """Test the servo is setup properly by ServoBoard."""
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    servo = servo_assembly_frontend.servos[0]

    assert servo._position is None


def test_servo_position():
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    servo = servo_assembly_frontend.servos[0]

    assert servo.position is None
    servo.position = None
    assert servo.position is None
    servo.position = 0.5
    assert servo.position == 0.5


def test_servo_range():
    """Test the range limits on the servo."""
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    servo = servo_assembly_frontend.servos[0]

    servo.position = 1
    servo.position = -1
    servo.position = 0

    with pytest.raises(ValueError):
        servo.position = 2

    with pytest.raises(ValueError):
        servo.position = -5


def test_pin_initialisation():
    """Test the pin is setup properly by ServoBoard."""
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    pin = servo_assembly_frontend.pins[0]

    assert pin._index == 0
    assert type(pin._backend) == type(servo_assembly_backend)
    assert pin.mode == PinMode.INPUT


def test_pin_mode_set():
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    pin = servo_assembly_frontend.pins[0]

    for mode in PinMode:
        pin.mode = mode


def test_pin_read():
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    pin = servo_assembly_frontend.pins[0]

    assert type(pin.read()) == PinValue

    pin.mode = PinMode.INPUT_PULLUP
    assert type(pin.read()) == PinValue

    with pytest.raises(ValueError):
        pin.mode = PinMode.OUTPUT_LOW
        pin.read()

def test_pin_analogue_read():
    servo_assembly_frontend, servo_assembly_backend = _get_dummy_servo_assembly()
    pin = servo_assembly_frontend.pins[7]

    assert type(pin.read_analogue()) == float

    pin.mode = PinMode.INPUT_PULLUP
    assert type(pin.read_analogue()) == float

    pin.mode = PinMode.OUTPUT_LOW
    with pytest.raises(ValueError):
        pin.read_analogue()

    pin2 = servo_assembly_frontend.pins[0]

    with pytest.raises(ValueError):
        pin2.read_analogue()
