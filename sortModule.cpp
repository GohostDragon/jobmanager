#include "python.h" 

static PyObject*

job_strlen(PyObject* self, PyObject* args)
{
    const char* str = NULL;
    int len;

    if (!PyArg_ParseTuple(args, "s", &str)) // �Ű����� ���� �м��ϰ� ���������� �Ҵ� ��ŵ�ϴ�.
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

    if (!PyArg_ParseTuple(args, "i", &sal)) //�������� ���� �Ҵ�
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
    {NULL, NULL, 0, NULL}    //�迭�� ���� ��Ÿ����.
};


static struct PyModuleDef jobmodule = {
    PyModuleDef_HEAD_INIT,
    "job",            // ��� �̸�
    "It is test module.", // ��� ������ ���� �κ�, ����� __doc__�� ����˴ϴ�.
    -1,JobMethods
};

PyMODINIT_FUNC
PyInit_job(void)
{
    return PyModule_Create(&jobmodule);
}
