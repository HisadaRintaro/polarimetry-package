from dataclasses import replace

def record_step(name: str):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            new_status: dict[str,str] = {**self.status, name: "PERFORM"}
            before = replace(self, status=new_status)

            result = func(before, *args, **kwargs)

            final_status: dict[str, str] = {**result.status, name: "COMPLETE"}
            return replace(result, status=final_status)

        return wrapper
    return decorator

