# Cryptography I with Dan Boneh

## Commit Hook

In order to autogenerate aggregate notes pdf, run the following from the root
of the git repo (i.e. one directory above this):

```bash
chmod +x ./cryptography/bin/generate-pdf-hook.sh
ln -s ../../cryptography/bin/generate-pdf-hook.sh .git/hooks/pre-commit
```

This will generate a new `resources/notes.pdf` on every commit.
