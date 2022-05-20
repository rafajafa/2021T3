from src.data_store import data_store

SECRET = 'C0Jp43mts6noiF4eXTawzthtRL1kRV'

def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['dms'] = []
    store['ID_COUNT'] = 0
    store['MSGID_COUNT'] = 0
    data_store.set(store)
