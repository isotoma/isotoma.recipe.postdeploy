import shelve
from zc.buildout import UserError

def get_values_removed_from_lists(path, buildout, keys):
    store = shelve.open(path)
    removed = {}

    for key in keys:
        p, k = key.split(":")

	# Get the current buildout state and combine it with the previous state
	# so we know about all items that were ever in the list
        current = set(buildout[p].get_list(k))
        old = set(current)
        if store.has_key(key):
            old = old.union(store[key])

        store[key] = old

	# Things that used to be in the list but are no longer. Because we use
	# sets we lost ordering, so we do an alpha sort so that consumers of
	# this data at least get a stable ordering.
        just_removed = list(old - current)
        just_removed.sort()

        removed.setdefault(p, {})
        removed[p][k] = just_removed

    store.close()

    return removed

