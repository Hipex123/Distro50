#include <pybind11/pybind11.h>

namespace py = pybind11;

int addNumbers(int a, int b)
{
    return a + b;
}

PYBIND11_MODULE(distro50ls, handle)
{
    handle.doc() = "This is a test";
    handle.def("addNumbersPy", &addNumbers);
}