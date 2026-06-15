# ⚠️ Staged copy of the future `recursive-recording` repo

This folder is a **durable backup** of a standalone repo built locally at
`/home/user/recursive-recording` (the build container is ephemeral; GitHub MCP was
token-expired, so it couldn't be pushed as its own repo). It does NOT belong in
recursive-tarot long-term — extract it into `playfulprocess/recursive-recording`:

```
# once GitHub is re-authorized:
#   create repo recursive-recording, then from a checkout of this folder:
git init && git add . && git commit -m "import recursive-recording" && git push
```

Start at `recording/README.md`; try `recording/karaoke/alice-karaoke.html` in a browser.
