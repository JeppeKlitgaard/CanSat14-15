#include <Python.h>
#include "cancrc.h"

static char module_docstring[] = "Wrapper for cancrc."
static char softcrc_docstring[] = "Calculates a CRC."

static PyObject *cancrc_softcrc(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"softcrc", cancrc_softcrc, METH_VARARGS, softcrc_docstring},
    {NULL, NULL, 0, NULL}
};

/* Initialize the module */
PyMODINIT_FUNC init_cancrc(void)
{
    PyObject *m = Py_InitModule3("_cancrc", module_methods, module_docstring);
    if (m == NULL)
        return;
 }

 static PyObject *cancrc_softcrc(PyObject *self, PyObject *args)
{
    double m, b;
    PyObject *checksum = PyBytes_FromString()
    PyObject *x_obj, *y_obj, *yerr_obj;
 
    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "ddOOO", &m, &b, &x_obj, &y_obj,
                                         &yerr_obj))
        return NULL;
 
    /* Interpret the input objects as numpy arrays. */
    PyObject *x_array = PyArray_FROM_OTF(x_obj, NPY_DOUBLE, NPY_IN_ARRAY);
    PyObject *y_array = PyArray_FROM_OTF(y_obj, NPY_DOUBLE, NPY_IN_ARRAY);
    PyObject *yerr_array = PyArray_FROM_OTF(yerr_obj, NPY_DOUBLE,
                                            NPY_IN_ARRAY);
 
    /* If that didn't work, throw an exception. */
    if (x_array == NULL || y_array == NULL || yerr_array == NULL) {
        Py_XDECREF(x_array);
        Py_XDECREF(y_array);
        Py_XDECREF(yerr_array);
        return NULL;
    }
 
    /* How many data points are there? */
    int N = (int)PyArray_DIM(x_array, 0);
 
    /* Get pointers to the data as C-types. */
    double *x    = (double*)PyArray_DATA(x_array);
    double *y    = (double*)PyArray_DATA(y_array);
    double *yerr = (double*)PyArray_DATA(yerr_array);
 
    /* Call the external C function to compute the chi-squared. */
    double value = chi2(m, b, x, y, yerr, N);
 
    /* Clean up. */
    Py_DECREF(x_array);
    Py_DECREF(y_array);
    Py_DECREF(yerr_array);
 
    if (value < 0.0) {
        PyErr_SetString(PyExc_RuntimeError,
                    "Chi-squared returned an impossible value.");
        return NULL;
    }
 
    /* Build the output tuple */
    PyObject *ret = Py_BuildValue("d", value);
    return ret;
}