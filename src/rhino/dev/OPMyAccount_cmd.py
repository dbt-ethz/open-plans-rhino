from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from auth import Login


def RunCommand( is_interactive ):
    resp = Login(email='test@gmail.com', password='testtest')
    print(resp)

    
if __name__ == "__main__":
    RunCommand(True)