
SYSADMIN_EXCLUSIVE_POLICIES = [
    ('/domain_orgs', ['POST']),
    ('/domain_orgs/<id>', ['DELETE'])
]

SYSADMIN_RESOURCES = [
    ('/domain_orgs', ['GET']),
    ('/domain_orgs/<id>', ['PUT', 'GET'])
]

USER_RESOURCES = []
