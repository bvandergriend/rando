#Test of jsonschema module

from jsonschema import validate

from jsonschema import Draft7Validator, validators

schema = {
    "type" : "object",
    "properties" : {
        "age" : {"type" : "integer",
                 "minimum" : 0,
                 "description" : "Years elapsed since birth"},
        "name" : {"type" : "string"},
        "color" : {"enum" : ["red", "blue", "green"]},
        "is_tall" : {"type" : "boolean",
                     "default" : False},
        },
    "additionalProperties" : False,
}

instance = {
    "age" : 0,
    "name" : "sally",
    "color" : "red",
    #"dog" : "baxter",
}

#Basic validation

print("Validating")

validate(instance, schema=schema)

print ("Done")
print ()

#Populate the defaults. The below is code just copy+pasted from the jsonschema docs

def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties" : set_defaults},
    )


DefaultValidatingDraft7Validator = extend_with_default(Draft7Validator)

print ("Before")
print (instance)

DefaultValidatingDraft7Validator(schema).validate(instance)

print ("After")
print (instance)
