# -*- coding: utf-8 -*-
"""Generate the 'How to Contribute' grammar — the contribute guide, dogfooded as a grammar.

Each item is one (what x how) how-to: a thing you can make (a deck, an edit, a sequence,
a course) by an avenue (the app, GitHub, an AI on the repo, the recursive.eco MCP). The
WHAT and HOW live in item.metadata so the Emergence Explorer can group rows by `what`
(organize by what you want to contribute) or columns by `how` (organize by the skill/tool)
— the contribute matrix draws itself, no bespoke layout.

Grammars (deck / edit / sequence) work through every avenue; a course is an MDX file in
the repo, so it's code-only (GitHub or an AI on the repo) — those two cells are simply
the items that don't exist for the course row.

Run from repo root:  python scripts/build_contribute_grammar.py
"""
import json, io, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "tarot", "how-to-contribute", "grammar.json")
PRICING = "https://flow.recursive.eco/pricing"   # prod (published); dev alias is dev.flow.recursive.eco/pricing

# HOW — the avenues (columns). cost: free | ai | mcp
HOW = {
    "app":     dict(label="In the app", host="recursive.eco", order=1,
                    skill="No tools — just the website", needs="A free recursive.eco account", cost="free"),
    "github":  dict(label="On GitHub", host="github.com", order=2,
                    skill="Git / GitHub — edit a file, open a PR", needs="A free GitHub account", cost="free"),
    "ai-repo": dict(label="An AI on the repo", host="Claude.ai / Desktop / Code", order=3,
                    skill="An AI assistant pointed at the repo", needs="Any AI assistant", cost="ai"),
    "mcp":     dict(label="The recursive.eco MCP", host="any MCP client", order=4,
                    skill="Claude Code, or your token in any MCP client", needs="The MCP connected (Claude — or any MCP client)", cost="mcp"),
}

# WHAT — the content types (rows). avenues = which HOWs apply.
WHAT = {
    "community-deck": dict(label="Your own deck", order=1, example="Clown Town",
                           noun="a community grammar — your own deck",
                           avenues=["app", "github", "ai-repo", "mcp"]),
    "edit-historic":  dict(label="Fix a historic deck", order=2, example="Visconti-Sforza",
                           noun="a correction to a historic deck",
                           avenues=["app", "github", "ai-repo", "mcp"]),
    "sequence":       dict(label="A sequence / playlist", order=3, example="Sing & Sing 2",
                           noun="a sequence grammar — a karaoke or paired set",
                           avenues=["app", "github", "ai-repo", "mcp"]),
    "course":         dict(label="A course", order=4, example="this guide",
                           noun="a written course (MDX in the repo)",
                           avenues=["github", "ai-repo"]),   # code-only: no app, no MCP
}

# Per-WHAT verbs, plugged into the per-HOW step template.
ACTION = {
    "community-deck": "start a new grammar and add your cards",
    "edit-historic":  "open the deck and fix the card",
    "sequence":       "create a sequence grammar (a karaoke or a paired set)",
    "course":         "draft a new course",
}
ACTION_FILE = {  # the file you touch on the GitHub/code routes
    "community-deck": "add a new `tarot/<your-deck>/grammar.json`",
    "edit-historic":  "edit the deck's `grammar.json`",
    "sequence":       "add a sequence `grammar.json`",
    "course":         "add a course `.mdx` under `pages/courses/`",
}

def steps(what, how):
    a = ACTION[what]
    if how == "app":
        return f"Sign in to recursive.eco, open **Create**, and {a}. Save, then publish."
    if how == "github":
        return f"On github.com, {ACTION_FILE[what]}. Edit it, then **open a pull request** — the change is reviewed before it goes live."
    if how == "ai-repo":
        return f"Point an AI assistant (Claude.ai, Claude Desktop, or Claude Code) at the repo and ask it to {a}. Review its draft and open a PR."
    if how == "mcp":
        return f"With the recursive.eco MCP connected, just **ask** your assistant to {a} — it acts on your library directly, no files to touch."
    return ""

def cost_section(cost):
    if cost == "free":
        return "Free."
    if cost == "ai":
        return f"You pay your own AI provider's usage. See [recursive.eco pricing]({PRICING})."
    if cost == "mcp":
        return f"Free to connect. Generated images, audio and storage are billed — see [recursive.eco pricing]({PRICING})."
    return ""

def build():
    items = []
    for wkey, w in sorted(WHAT.items(), key=lambda kv: kv[1]["order"]):
        for hkey in w["avenues"]:
            h = HOW[hkey]
            items.append({
                "id": f"{wkey}__{hkey}",
                "name": f"{w['label']} — {h['label']}",
                "category": "how-to",
                "keywords": [wkey, hkey, h["cost"]],
                "metadata": {
                    # the two matrix axes — drag these in the Emergence Explorer
                    "what": wkey, "what_label": w["label"],
                    "how": hkey, "how_label": h["label"],
                    "skill": h["skill"], "cost": h["cost"], "needs": h["needs"],
                },
                "sections": {
                    "What you'll do": f"Contribute {w['noun']} ({h['label'].lower()}). Example: {w['example']}.",
                    "Steps": steps(wkey, hkey),
                    "What you need": h["needs"],
                    "Cost": cost_section(h["cost"]),
                },
            })

    grammar = {
        "_grammar_commons": {"schema_version": "1.0", "license": "CC-BY-SA-4.0",
            "attribution": [{"name": "PlayfulProcess", "note": "The contribute guide, dogfooded as a grammar."}]},
        "name": "How to Contribute — a Grammar of Ways In",
        "description": (
            "The contribute guide as a grammar: every item is one way IN — a thing you can make "
            "(your own deck, a fix to a historic deck, a sequence/playlist, a course) by an avenue "
            "(the app, GitHub, an AI on the repo, or the recursive.eco MCP). Each item carries its "
            "`what` and `how` in metadata, so the Emergence Explorer can group by what you want to "
            "contribute OR by the skill/tool — the contribute matrix draws itself. Grammars work "
            "through every avenue; a course is an MDX file in the repo, so it's code-only. This guide "
            "is itself a grammar you can fork and edit — which is exactly its point."
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "default_view": "study",
        "provenance": "reference",
        "metadata": {"common_name": "How to Contribute", "category": "reference"},
        "_generated": True, "_built_by": "scripts/build_contribute_grammar.py",
        "items": items,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(grammar, io.open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    whats = len({i["metadata"]["what"] for i in items})
    hows = len({i["metadata"]["how"] for i in items})
    print(f"wrote {OUT}\n  {len(items)} items across {whats} what x {hows} how")

if __name__ == "__main__":
    build()
