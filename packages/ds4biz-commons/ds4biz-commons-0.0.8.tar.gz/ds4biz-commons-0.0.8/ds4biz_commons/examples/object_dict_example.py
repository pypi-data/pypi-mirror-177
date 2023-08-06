from ds4biz_commons.utils.dict_utils import ObjectDict
import json


o=ObjectDict()

o.name="Fulvio"
o.surname="D'Antonio"

o.contactinfo.address.street="via di qui"
o.contactinfo.address.number=10
o.contactinfo.telephone="+39 061234567"

print(json.dumps(o,indent=2))


