from setuptools import setup

setup(
    name="todo_app",
    version="0.1",
    py_modules=["todo_app.main", "todo_app.db_manager"],
    install_requires=["ttkbootstrap"],
)
