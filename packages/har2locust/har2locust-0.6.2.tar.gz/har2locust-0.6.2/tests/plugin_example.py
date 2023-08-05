# This file has some advanced examples of how to massage your recording
# Use it as inspiration for the techniques, not as a recommendation for exactly what to do
from har2locust.plugin import entriesprocessor, astprocessor
from ast import *
import re


@entriesprocessor
def parametrize_ssn(entries):
    # self.customer (gets added below by get_customer_from_reader)
    for e in entries:
        if "postData" in e["request"]:
            e["request"]["postData"]["text"] = re.sub(
                r'"personalId":"\d*"',
                "\"personalId\":self.customer['ssn']",
                e["request"]["postData"]["text"],
            )


@entriesprocessor
def skip_origin_header(entries):
    # this particular site doesnt care about origin header and skipping it makes the locustfile much neater
    for e in entries:
        request = e["request"]
        request["headers"] = [h for h in request["headers"] if h["name"] != "origin"]


@astprocessor
def get_customer_from_reader(tree: Module, values: dict):
    class T(NodeTransformer):
        def visit_ImportFrom(self, node: ImportFrom) -> ImportFrom:
            # import a slightly different RestUser, from another package
            if node.names[0].name == "RestUser":
                node.module = "svs_locust"
            self.generic_visit(node)
            return node

        def visit_ClassDef(self, node: ClassDef) -> ClassDef:
            class_extra_props = parse("tb = True")
            node.body[0] = class_extra_props.body[0]  # this will overwrite the "host = ..." line
            self.generic_visit(node)
            return node

        def visit_FunctionDef(self, node: FunctionDef) -> FunctionDef:
            # wrap the entire task function body in a with-block.
            if node.name == "t":
                with_block = parse(
                    f"""
with self.reader.user() as self.customer:
    pass
                    """
                ).body[0]
                assert isinstance(with_block, With), with_block
                with_block.body = node.body
                node.body = [with_block]
            self.generic_visit(node)
            return node

        def visit_Call(self, node: Call) -> Call:
            # call rest_ instead of rest for those urls that have &_<timestamp> at the end
            if isinstance(node.func, Attribute) and node.func.attr == "rest":
                c = node.args[1]
                if isinstance(c, Constant) and re.search(r"&_=\d+$", c.value):
                    node.func.attr = "rest_"
                    c.value = re.sub(r"&_=\d+$", "", c.value)
            self.generic_visit(node)
            return node

    T().visit(tree)


# More examples

# @entriesprocessor
# def log_something_and_drop_everthing_but_the_first_request(entries):
#     logging.info(f"hello")
#     entries[:] = [entries[0]]  # update list in-place
