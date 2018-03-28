
def __script__ [input] {

    broadcast("broadcasting_this") #this doesn't work, because it's a circular dependency

}


import piping *

# defines the callback for calling
__trigger__ = any(
    cron("* * * * *"),
    all(
        new_result("script1"),
        new_result("script2", 10), # 10 new items from
    ),
    listen("broadcasting_this"), #TODO: this needs work
)

# result of execute will be fed to __script__
def __execute__ [] {
    {
        "a": take("script1"),
        "b": take("script2", 20),
        "c": take_new("script3"),
        "d": take_all("script4"),
    }
}
