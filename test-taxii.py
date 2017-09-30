
###############################################################################

client = create_client(
    'test.taxiistand.com',
    use_https=True,
    discovery_path='/read-write/services/discovery')

services = client.discover_services()
for service in services:
    print('Service type={s.type}, address={s.address}'
          .format(s=service))

collections = client.get_collections(
    uri='https://test.taxiistand.com/read-write/services/collection-management')
for collection in collections:
    print(collection)
    
    content_blocks = client.poll(collection_name='all-data')
    for block in content_blocks:
        print(block.content)
        print(collection.name)
        print(collection.description)
        print(collection.type)
        print(collection.polling_services)
        print(collection.volume)
        print('---')




