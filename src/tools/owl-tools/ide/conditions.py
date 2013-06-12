# tools/user/ide/conditions.py
#
# Copyright 2013 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import logging
logger = logging.getLogger(__name__)

#producer
def make_item(condition, resource, source=None, item=None):
    #generate item
    try:
        if not item and source:
            item = source.get()
        condition.acquire()
        #add item to resource
        resource.put(item)
        condition.notify()
        condition.release()
    except Exception, e:
        logger.exception('make_item failed')

#consumer
def get_item(condition, resource, action):
    condition.acquire()
    item = ''
    while True:
        item = get_from_q(resource)
        if item != False:
            break
        condition.wait()
    condition.release()
    try:
        result = action(item)
    except Exception, e:
        logger.exception('get_item: %s', action.__name__)
    return result

def get_from_q(q):
    logger.debug('get from q:')
    logger.debug(q.qsize())
    result = ''
    if not q.empty():
        while not q.empty():
            result += str(q.get())
            q.task_done()
        logger.debug('get_from_q: %s',result)
        return result
    return False
