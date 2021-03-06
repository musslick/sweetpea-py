"""..."""


class ToolError(Exception):
    """An error raised when a command-line tool fails."""

    def __init__(self, returncode: int, stdout: str, stderr: str):
        message_lines = [str(returncode)]
        if stdout:
            message_lines.append("\n    stdout output captured below:\n" + stdout)
        if stderr:
            message_lines.append("\n    stderr output captured below:\n" + stderr)
        super().__init__(''.join(message_lines))
