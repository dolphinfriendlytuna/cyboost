from cython.operator cimport dereference as deref
from libcpp cimport bool
from libcpp.map cimport map as cppmap
from libcpp.vector cimport vector
from libcpp.algorithm cimport sort
from cyboost.pool.pool_alloc cimport pool_allocator, pool_allocator_tag
from cyboost.pool.singleton_pool cimport singleton_pool
from cyboost.pool.less cimport less


ctypedef pool_allocator[long] ALLOCATOR

cdef extern from *:
    ctypedef void* eight "sizeof(long)"

def test_map():

    cdef cppmap[long, long, less[long], ALLOCATOR] m
    cdef cppmap[long, long].iterator head

    import psutil, os
    proc = psutil.Process(os.getpid())

    start = proc.memory_info().rss

    # fillup map
    for i in range(10000):
        m[i] = i**2

    # drain map
    while not m.empty():
        head = m.begin()

        t = deref(head).first
        v = deref(head).second

        m.erase(head)

    singleton_pool[pool_allocator_tag, eight].purge_memory()

    import time; time.sleep(1)

    end = proc.memory_info().rss

    print(start / 1024 / 1024)
    print(end / 1024 / 1024)
    assert start == end, f'{start} vs {end}'