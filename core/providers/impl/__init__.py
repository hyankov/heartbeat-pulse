# Register the providers here
__all__ = [
    'ping',
    'fake'
]

#TODO: Dynamic
#sub_folder = "implementations"
#dir_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), sub_folder)
#for (module_loader, name, ispkg) in pkgutil.iter_modules([ dir_name ]):
    #if name != "base":
        #importlib.import_module('.' + name, __package__ + "." + sub_folder)