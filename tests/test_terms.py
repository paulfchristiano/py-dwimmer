from terms import *
import pytest

@pytest.mark.parametrize("temp", [
    "testing",
    "{} is above {}",
    "{} {} next to each other..."
])
def test_template_creation(temp):
    template = Template(temp)
    assert "{}".join(template.parts)

@pytest.mark.parametrize("test", [
    Template("hello"),
    Template("testing")(),
    RefNum(4),
    Template("a {} b")(Template("testing")),
    Action.reply(Template("hello")())
])
def test_interning(test):
    assert from_id(test.id).id == test.id
