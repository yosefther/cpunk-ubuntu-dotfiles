# Commit messages

Use `type(scope): imperative summary` for commit titles. Keep the summary
specific, lowercase after the prefix, and preferably within 72 characters.

Use `feat` for new behavior, `fix` for corrections, `docs` for documentation,
and `refactor` for changes that preserve behavior. Scopes should identify the
area, such as `menu`, `wallpapers`, `theme`, `desktop`, or `installer`.

For changes that need explanation, add a blank line and describe the problem,
the resulting behavior, and the reason for the approach. Record validation
only when it was actually performed. Avoid vague claims such as "improve
things," "reliable," or "all tests pass" without supporting detail.

Keep commits focused on one coherent change. Preserve existing authorship
when editing history, and coordinate before rewriting shared commits.

To use this repository's template:

```sh
git config commit.template .github/commit-template.txt
```

Example:

```text
feat(wallpapers): discover personal images in the wallpaper menu

Read supported images from the user's wallpaper directory so new choices
appear without editing the menu script. Keep personal images local.
```
