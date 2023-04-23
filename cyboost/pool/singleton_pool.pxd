cdef extern from "boost/pool/singleton_pool.hpp" namespace "boost" nogil:

    cdef cppclass singleton_pool[TAG, SIZE, ALLOCATOR=*]:

        @staticmethod
        bint release_memory()

        @staticmethod
        bint purge_memory()
