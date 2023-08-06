# ## Simple function to get an object's name as a string
# def name_of_global_obj(target_object):
#     return [objname for objname, oid in globals().items()
#             if id(oid)==id(target_object)][0]

# # Upadate contact properties to HubSpot
# def hs_update_contact(hs_contact_id, **property_name_also_an_object, token_key):
#   """
#   Update contact properties by a specific contact id which can be obtained by a search API call. 
#   Args:
#         hs_contact_id (:obj:`str`, required): hubspot id of a specific contact/email.
#         token_key (:obj:`str`, required): HubSpot Private App Token. See more: https://developers.hubspot.com/docs/api/private-apps
#         properties_list (:obj:`list`, required): A list of properties you need to retrieve information. Ex: ['email', 'createdate', 'lastmodifieddate']
#   """
# #   prop_1 = name_of_global_obj(property_name_also_an_object)
#   url = 'https://api.hubapi.com/crm/v3/objects/contacts/{}'.format(hs_contact_id)
#   payload = json.dumps({
#   "properties": {
#     "last_abandoned_date": "{}".format(last_abandoned_date),
#     "last_abandoned_product": "{}".format(last_abandoned_product),
#     "last_abandoned_url": "{}".format(last_abandoned_url)
#   }
# })
#   headers = {'Authorization' : 'Bearer {}'.format(token_key),
#              'content-type': 'application/json'}
#   response = requests.request("PATCH", url, headers=headers, data=payload).json()
#   result = json_normalize(response)
#   return result

