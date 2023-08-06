import time, uuid, hashlib, typing


class timedotc:
    def __init__(
        self,
        secret_key: str = uuid.uuid4().hex,
        method: typing.Optional[str] = "sub",
    ) -> None:
        self.secret_key = secret_key
        self.method = method

    def verify(self, code: str, target: str):
        if self.method == "sub":
            code_hash = self._sub(code)
        elif self.method == "add":
            code_hash = self._add(code)
        else:
            raise ValueError("Invalid method")

        return code_hash == target

    def hash(self, code: str):
        return hashlib.sha256("".join([str(code), self.secret_key]).encode("utf-8")).hexdigest()

    def _sub(self, code: str):
        diffs = "".join(
            [
                str(abs((d1 - d2) % 10))
                for d1, d2 in zip(self._get_time(), [int(d) for d in list(str(code))])
            ]
        )
        return self.hash(diffs)

    def _add(self, code: str):
        diffs = "".join(
            [
                str(abs((d1 + d2) % 10))
                for d1, d2 in zip(self._get_time(), [int(d) for d in list(str(code))])
            ]
        )
        return self.hash(diffs)

    def _get_time(self):
        return [int(d) for d in list(time.strftime("%H%M"))]
