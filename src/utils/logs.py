from src.configs import VERBOSITY


# https://www.codegrepper.com/code-examples/python/python+print+error+in+red
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def log(*args, verbosity=1, rgb=(200, 200, 200)):
    if verbosity <= VERBOSITY:
        colored_args = tuple([colored(*rgb, arg) for arg in args])
        print(*colored_args)


def log_red(*args, **kwargs):
    log(*args, **kwargs, rgb=(200, 50, 50))


def log_pink(*args, **kwargs):
    log(*args, **kwargs, rgb=(255, 105, 180))


def log_yellow(*args, **kwargs):
    log(*args, **kwargs, rgb=(200, 200, 50))


def log_green(*args, **kwargs):
    log(*args, **kwargs, rgb=(50, 200, 50))


def log_cyan(*args, **kwargs):
    log(*args, **kwargs, rgb=(50, 200, 200))


#####################################################
def log_obj_stage(*args, **kwargs):
    log(*args, **kwargs)


if __name__ == "__main__":
    log('test')
    log('test', rgb=(255, 0, 0))
    log('test', rgb=(0, 255, 0))
    log('test', rgb=(0, 0, 255))
    log('test', rgb=(0, 0, 0))
    log_red('red')
    log_yellow('yellow')
    log_cyan('cyan')
    log_green('green')

