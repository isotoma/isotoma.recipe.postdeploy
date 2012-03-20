import shelve
from zc.buildout import UserError

def handle_max(buildout, p, k, previous):
    val = int(buildout[p][k])
    if previous:
        val =  max(int(val), previous)
    return val, val

def handle_list(buildout, p, k, previous):
    # Get the current buildout state and combine it with the previous state
    # so we know about all items that were ever in the list
    current = set(buildout[p].get_list(k))
    old = set(current)
    if previous:
        old = old.union(previous)

    # Things that used to be in the list but are no longer. Because we use
    # sets we lost ordering, so we do an alpha sort so that consumers of
    # this data at least get a stable ordering.
    just_removed = list(old - current)
    just_removed.sort()

    return old, just_removed


def get_history(path, buildout, keys):
    store = shelve.open(path)
    data = {}

    for key in keys:
        action = "removed"
        if " " in key:
            key, action = key.split(" ", 1)
            key, action = key.strip(), action.strip()

        p, k = key.split(":")

        handle = dict(
            removed = handle_list,
            max = handle_max,
            ).get(action, None)

        if not handle:
            raise UserError("'%s' is not a valid tracking mechanism" % action)

        val = None
        if store.has_key(key):
            val = store[key]

        data.setdefault(p, {})
        store[key], data[p][k] = handle(buildout, p, k, val)

    store.close()

    return data

