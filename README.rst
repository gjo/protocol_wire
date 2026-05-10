================================
protocol_wire
================================


development
-----------

setup::

  $ python3.14t -m venv env314t
  $ . env314t/bin/activate
  (env314t)$ pip install 'pip==26.1'
  (env314t)$ pip install --uploaded-prior-to=P7D -U pip setuptools wheel
  (env314t)$ pip install --uploaded-prior-to=P7D -e '.[develop]'
  (env314t)$ pip list --format=freeze --exclude-editable --exclude=protocol_wire > constraints.txt

