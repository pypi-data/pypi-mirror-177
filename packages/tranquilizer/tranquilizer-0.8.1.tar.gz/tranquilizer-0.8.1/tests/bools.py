from tranquilizer import tranquilize

@tranquilize(method='post')
def true_or_false(input: bool):
    return {'value': input}
