from kadi_apy import KadiManager
import uuid

    
dict_1= {"description": "",
         "extras": [
        {"key": "General Info","type": "dict","value": [
            {"key": "Specimen ID", 
            "type": "str",
            "validation": {
                "options": [
                    "a",
                    "b",
                    "c",
                    "d"
                ],
                "required": True
                },
            },
          {"key": "Company or Vendor Name",
            "type": "str"},
          {"key": "Location",
            "type": "dict",
            "value": [{"key": "Building",
                       "type": "str",
                       "validation": {
                            "options": [
                            "3",
                            "4"]}},
              {
                "key": "Floor",
                "type": "int"
              },
              {
                "key": "Institution (Location)",
                "type": "str"
              },
              {
                "key": "Room Number",
                "type": "str"
              }
            ]
          },
          {
            "key": "Operator/s in Charge",
            "type": "dict",
            "value": [
              {
                "key": "Last Name",
                "type": "str",
                "value": "null"
              },
              {
                "key": "First Name",
                "type": "str",
                "value": "null"
              },
              {
                "key": "Institution Name",
                "type": "str",
                "value": "null"
              },
              {
                "key": "User Role",
                "type": "str",
                "value": "null"
              },
              {
                "key": "User Token",
                "type": "str",
                "value": "null"
              }
            ]
          }
        ]
      },
      {
        "key": "Spatial Information",
        "type": "dict",
        "value": [
          {
            "key": "Shape",
            "type": "str",
            "value": "null"
          },
          {
            "key": "Dimensions Information",
            "type": "dict",
            "value": [
              {
                "key": "Diameter",
                "type": "float",
                "unit": "mm"
              }
            ]
          },
          {
            "key": "Face Orientation Information",
            "type": "dict",
            "value": [
              {
                "key": "Tribological Interest Side(s)",
                "type": "str",
                "value": "null"
              },
              {
                "key": "Indicated Face Orientation",
                "type": "dict",
                "value": [
                  {
                    "key": "Orientation Indication Feature Type",
                    "type": "str",
                    "value": "null"
                  },
                  {
                    "key": "Orientation Indication Feature Side",
                    "type": "str",
                    "value": "null"
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "key": "Material Information",
        "type": "dict",
        "value": [
          {
            "key": "Material Category",
            "type": "str",
            "value": "null"
          },
          {
            "key": "Material Name",
            "type": "str",
            "value": "null"
          },
          {
            "key": "Material Empirical Formula",
            "type": "str",
            "value": "null"
          },
          {
            "key": "Nominally Known Material Information",
            "type": "dict",
            "value": [
              {
                "key": "Is Specimen Material Ferromagnetic",
                "type": "bool"
              }
            ]
          }
        ]
      }
    ],
    "license": "CC-BY-4.0",
    "tags": [
      "flins",
      "sapphire"
    ],
    "title": "Sphere FLINS 3",
    "type": "record"
  }

# Not allowed
# - value null is not allowed, so delete value
# - visibility is not supported

def Template_Create(instance, data, group_id=None):
    template = KadiManager(instance=instance).template(identifier=("sphere-flins-"+str(uuid.uuid4())),type='record', data=data, create=True)
    template.add_group_role(group_id=group_id, role_name='editor')
    
# print(Template_Create('Malte Flachmann', data=dict_1, group_id=8))





def Template_Delete(id):
    KadiManager('Malte Flachmann').template(id=id).delete()

# Template_Delete(id=322)


