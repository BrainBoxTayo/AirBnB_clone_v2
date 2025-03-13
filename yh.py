from models.engine.file_storage import FileStorage
from models.state import State

fs = FileStorage()

new_state = State()
print(new_state.id)

fs.delete(new_state)
print(fs.all(State))