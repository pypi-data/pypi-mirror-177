# PythonSignal Signal/Event Python PyPackage

A small implementation of signals, inspired by a snippet of Django signal

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install python_sginal
```

```python
#Define NameSpace
from python_signal import Namespace
_signals = Namespace()

#reciever
user_login = _signals.signal('user_login')

@user_login.connect
def after_user_login(current_user):
    pass

#sender
user_login.send(user)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
