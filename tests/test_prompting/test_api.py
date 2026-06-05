"""Tests for beanapp.prompting.api."""

from src.beanapp.prompting.api import AVAILABLE_PROMPTS, register, prompt


class TestRegister:
    def test_decorator_registers(self):
        saved = AVAILABLE_PROMPTS.get((str, "cli"))
        @register(str)
        def prompt_str(message, data_type):
            pass

        try:
            assert (str, "cli") in AVAILABLE_PROMPTS
            assert AVAILABLE_PROMPTS[(str, "cli")] is prompt_str
        finally:
            if saved is not None:
                AVAILABLE_PROMPTS[(str, "cli")] = saved
            else:
                AVAILABLE_PROMPTS.pop((str, "cli"), None)

    def test_custom_interface(self):
        @register(int, interface="test_interface")
        def prompt_int(message, data_type):
            pass

        assert (int, "test_interface") in AVAILABLE_PROMPTS
        del AVAILABLE_PROMPTS[(int, "test_interface")]


class TestPrompt:
    def test_direct_match(self):
        saved = AVAILABLE_PROMPTS.get((int, "cli"))
        @register(int)
        def prompt_int(message, data_type):
            return 21

        try:
            assert prompt(int) == 21
        finally:
            if saved is not None:
                AVAILABLE_PROMPTS[(int, "cli")] = saved
            else:
                AVAILABLE_PROMPTS.pop((int, "cli"), None)

    def test_error_when_no_prompt(self):
        class NewType:
            pass

        assert prompt(NewType, message="test", interface="test_error") is None

    def test_mro_fallback(self):
        class Parent:
            pass

        saved = AVAILABLE_PROMPTS.get((Parent, "cli"))
        @register(Parent)
        def prompt_parent(message, data_type):
            return 42

        class Child(Parent):
            pass

        try:
            assert prompt(Child) == 42
        finally:
            if saved is not None:
                AVAILABLE_PROMPTS[(Parent, "cli")] = saved
            else:
                AVAILABLE_PROMPTS.pop((Parent, "cli"), None)

    def test_mro_fallback_with_pydantic(self):
        import pydantic

        saved = AVAILABLE_PROMPTS.get((pydantic.BaseModel, "cli"))
        @register(pydantic.BaseModel)
        def prompt_base_model(message, data_type):
            return "from base"

        class MyModel(pydantic.BaseModel):
            name: str

        try:
            assert prompt(MyModel) == "from base"
        finally:
            if saved is not None:
                AVAILABLE_PROMPTS[(pydantic.BaseModel, "cli")] = saved
            else:
                AVAILABLE_PROMPTS.pop((pydantic.BaseModel, "cli"), None)

    def test_mro_fallback_child_wins(self):
        class GrandParent:
            pass

        class Parent(GrandParent):
            pass

        class Child(Parent):
            pass

        @register(GrandParent, interface="test_error")
        def prompt_grandparent(message, data_type):
            return "grandparent"

        @register(Parent, interface="test_error")
        def prompt_parent(message, data_type):
            return "parent"

        assert prompt(Child, interface="test_error") == "parent"
