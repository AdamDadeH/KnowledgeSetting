from unittest import TestCase

from source.inline_handler import SubstitutionHandler
from concept_store.local_concept_store import LocalConceptStore
from core.concept import Concept

class TestInlineHandler(TestCase):
    meow = Concept.from_title_content(title="meow", content="«cat() goes meow")
    cat = Concept.from_title_content(title="cat", content="Fluffy mammal with claws")
    named_meow = Concept(
        content="«named_cat(«mrmeow()) goes meow",
        content_type="test",
        name="meow",
    )
    named_cat = Concept(
        content="Fluffy mammal will claws",
        content_type="test",
        name="named cat",
        inline_content=lambda x: "«cat() named {}".format(x[0]),
        instance_rep=lambda x: "cat",
    )
    mrmeow=Concept(
        content="Mr. Meow!",
        content_type="test",
        name="Mr Meow",
        inline_content=lambda x:"Mr. Meow")
    repo = LocalConceptStore(
        {"meow": meow, "cat": cat, "named_cat": named_cat, "named_meow": named_meow, "mrmeow": mrmeow}, {}
    )

    def test_text(self):
        sub = SubstitutionHandler([], {})
        input = "I am just a regular string"
        output = sub.substitute(input)
        self.assertEqual(output, input)

    def test_constant_sub(self):

        sub = SubstitutionHandler(["cat"], self.repo)
        output = sub.substitute(self.meow.get_concept())
        self.assertEqual(output, "Fluffy mammal with claws goes meow")

    def test_constant_nosub(self):
        sub = SubstitutionHandler(["meow"], self.repo)
        output = sub.substitute(self.meow.get_concept())
        self.assertEqual(output, "cat goes meow")

    def test_parametric_sub(self):
        sub = SubstitutionHandler(["named_cat","mrmeow"], self.repo)
        output = sub.substitute(self.named_meow.get_content())
        print(output)
