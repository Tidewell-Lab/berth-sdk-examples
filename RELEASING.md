# Releasing

We haven't cut a tagged release yet; `main` is what we ship. From v1.0:

1. Update `CHANGELOG.md` and the version in the client's User-Agent (`tidewell_client.py`).
2. Tag the release with a signed tag (`git tag -s`) and push the tag.
3. Announce it in the changelog section of the docs site.

Maintainer signing keys are published on our own domain, the standard way,
so you don't need a keyserver to find them.
