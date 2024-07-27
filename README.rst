================================
protocol_wire
================================


development
-----------

setup::

  $ python3.10 -m venv env310
  $ . env310/bin/activate
  (env310)$ pip install -U pip setuptools wheel
  (env310)$ pip install -e '.[develop]'
  (env310)$ pip list --format freeze --exclude-editable > constraints.txt

