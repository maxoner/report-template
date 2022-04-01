{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "committed-involvement",
   "metadata": {},
   "outputs": [],
   "source": [
    "import ctypes as ct\n",
    "import contextlib"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "sacred-preserve",
   "metadata": {},
   "outputs": [],
   "source": [
    "@contextlib.contextmanager\n",
    "def load_dll(path):\n",
    "    lib = ct.cdll.LoadLibrary(path)\n",
    "    yield lib\n",
    "    libHandle = lib._handle\n",
    "    del lib\n",
    "    ct.windll.kernel32.FreeLibrary(libHandle)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "coordinate-engine",
   "metadata": {},
   "outputs": [],
   "source": [
    "with load_dll(\"okawsp6.dll\") as wsp_lib:\n",
    "    res = wsp_lib.wspPST(ct.c_double(6.0))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "statewide-general",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(res)"
   ]
  }
 ],
 "metadata": {
  "jupytext": {
   "cell_metadata_filter": "-all",
   "notebook_metadata_filter": "-all",
   "text_representation": {
    "extension": ".py",
    "format_name": "light"
   }
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
