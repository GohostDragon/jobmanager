#include "python.h" 

static PyObject*

job_strlen(PyObject* self, PyObject* args)
{
    const char* str = NULL;
    int len;

    if (!PyArg_ParseTuple(args, "s", &str)) // 매개변수 값을 분석하고 지역변수에 할당 시킵니다.
        return NULL;

    len = strlen(str);

    return Py_BuildValue("i", len);
}

static PyObject*
job_salcount(PyObject* self, PyObject* args)
{
    int quotient = 0;
    int sal = 0;
    int result = 0;

    if (!PyArg_ParseTuple(args, "i", &sal)) //피제수와 제수 할당
        return NULL;

    if (sal > 10000000)
    {
        result = (int)((int)((sal / 12)) / 209);
    }
    else if (10000000 > sal && sal > 1000000)
    {
        result = int(sal / 209);
    }
    else
    {
        result = sal;
    }

    return Py_BuildValue("i", result);
}

static PyMethodDef JobMethods[] = {
    {"strlen", job_strlen, METH_VARARGS,
    "count a string length."},
    {"salcount", job_salcount, METH_VARARGS,
    "salcount function \n return salcount is dividend / divisor"},
    {NULL, NULL, 0, NULL}    //배열의 끝을 나타낸다.
};


static struct PyModuleDef jobmodule = {
    PyModuleDef_HEAD_INIT,
    "job",            // 모듈 이름
    "It is test module.", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
    -1,JobMethods
};

PyMODINIT_FUNC
PyInit_job(void)
{
    return PyModule_Create(&jobmodule);
}
