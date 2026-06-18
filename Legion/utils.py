def wait_for_target_cursor(API, timeout_loops=30):
    """
    Safely waits (up to 3 secs by default) for the server to send a target cursor.
    Requires the engine API object to be passed in.
    """
    while not API.HasTarget() and timeout_loops > 0 and not API.StopRequested:
        API.ProcessCallbacks()
        API.Pause(0.1)
        timeout_loops -= 1


def get_mobs_by(API, notorieties, dist):
    mobs = []
    for n in notorieties:
        # For some reason it always returns None if all notorieties are passed in one go
        inrange = API.NearestMobiles([n], dist)
        if inrange:
            mobs.extend(inrange)

    return mobs
