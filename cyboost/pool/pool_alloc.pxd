cdef extern from "boost/pool/pool_alloc.hpp" namespace "boost" nogil:

    cdef cppclass pool_allocator[T]:
        pool_allocator()
        #allocator(const fast_pool_allocator &)
        #allocator(const allocator[U] &) #unique_ptr unit tests fail w/this
        T * address(T &)
        const T * address(const T &) const
        T * allocate( size_t n ) # Not to standard.  should be a second default argument
        void deallocate(T * , size_t)
        size_t max_size() const
        void construct( T *, const T &) #C++98.  The C++11 version is variadic AND perfect-forwarding
        void destroy(T *) #C++98
        void destroy[U](U *) #unique_ptr unit tests fail w/this

    cdef cppclass pool_allocator_tag:
        pass

    cdef cppclass fast_pool_allocator[T]:
        fast_pool_allocator()
        #allocator(const fast_pool_allocator &)
        #allocator(const allocator[U] &) #unique_ptr unit tests fail w/this
        T * address(T &)
        const T * address(const T &) const
        T * allocate( size_t n ) # Not to standard.  should be a second default argument
        void deallocate(T * , size_t)
        size_t max_size() const
        void construct( T *, const T &) #C++98.  The C++11 version is variadic AND perfect-forwarding
        void destroy(T *) #C++98
        void destroy[U](U *) #unique_ptr unit tests fail w/this

    cdef cppclass fast_pool_allocator_tag:
        pass

