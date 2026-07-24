import contextlib
import io
import traceback


class CodeExecutor:

    def execute(self, code: str) -> str:

        stdout = io.StringIO()

        namespace = {
            "__builtins__": __builtins__,
        }

        try:

            with contextlib.redirect_stdout(stdout):
                exec(code, namespace)

            output = stdout.getvalue().strip()

            if not output:
                output = "Code executed successfully."

            return (
                "Generated Code:\n\n"
                f"{code}\n\n"
                "Execution Output:\n"
                f"{output}"
            )

        except Exception:

            return (
                "Generated Code:\n\n"
                f"{code}\n\n"
                "Execution Error:\n"
                f"{traceback.format_exc()}"
            )