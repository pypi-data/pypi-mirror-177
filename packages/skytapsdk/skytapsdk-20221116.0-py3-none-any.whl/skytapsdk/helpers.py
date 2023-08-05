from restfly import APIEndpoint, APISession


def links_iterator(api: APISession, path: str = "", **kwargs) -> list:
    """If API returns paginated results that use a 'Links' header.  Iterate over those to get all."""
    _count = kwargs.get("count", 100)
    _offset = kwargs.get("offset", 0)
    _params = {
        "count": _count,
        "offset": _offset,
    }
    _params.update(kwargs)

    response = api.get(path=path, params=_params)
    results = response.json()
    while "link" in response.headers and 'rel="next"' in response.headers["Link"]:
        _params["offset"] = _params["offset"] + _count
        response = api.get(path=path, params=_params)
        results += response.json()
    return results


class LinksIterator(APIEndpoint):
    """If API returns paginated results that use a 'Links' header.  Iterate over those to get all."""

    COUNT: int = 100
    OFFSET: int = 0

    def get_results(self, count: int = COUNT, offset: int = OFFSET, **kwargs) -> list:
        params = {
            "count": count,
            "offset": offset,
        }
        params.update(kwargs)
        response = self._api.get(path=self._path, params=params)
        results = response.json()
        while "link" in response.headers and 'rel="next"' in response.headers["Link"]:
            params["offset"] = params["offset"] + count
            response = self._api.get(path=self._path, params=params)
            results += response.json()
        return results
