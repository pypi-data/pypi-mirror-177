# creppl/ui/prompts.py


def show_header():
    print("Creppl - C++ REPL (Read, Evaluate, Print, Loop) written in Python.")
    print("Type \"$help\" for more information.")


def get_input_prompt(curr_line: int):
    prompt = ">>>" + f"[{curr_line}]".center(5) + ": "
    return prompt
