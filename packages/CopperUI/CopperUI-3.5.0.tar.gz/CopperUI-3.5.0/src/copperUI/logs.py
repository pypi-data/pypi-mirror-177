from random import randint


load = ["mowing the grass", "writing a poem", "doing homework", "reading docs", "taking a nap"]
fail = ["got startled and dropped it", "ran out of bubblegum", "got lost", "forgot to do the dishes", "huh?"]
succeed = ["yay! all done", "finished", "99%...", "finishing up..."]

def loading():
    """funny random loading messages"""
    return load[randint(0, len(load)-1)]

def failure():
    """funny random failure messages"""
    return fail[randint(0, len(fail)-1)]

def sucess():
    """funny random sucess messages"""
    return succeed[randint(0, len(succeed)-1)]