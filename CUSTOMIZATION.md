# Customized GitHub Profile Setup

This profile package is customized for `porwalyash438`.

## Publish
1. Create or open the public repository named exactly `porwalyash438`.
2. Copy the *contents* of this folder into that repository root (README.md must be at the root).
3. Commit and push to `main`.
4. Open **Settings → Secrets and variables → Actions** and add a repository secret named `METRICS_TOKEN` containing a GitHub personal access token. Do not commit tokens. A fine-grained token should have the minimum repository/user permissions required by the Metrics action; check the action documentation for current requirements.
5. In **Settings → Actions → General**, allow workflows to create and approve pull requests or, at minimum, ensure workflow permissions allow contents write. The included workflows need to commit generated SVGs.
6. Open **Actions**, enable workflows if asked, and run **Charts and cards** and **Metrics** manually.

## Edit your profile
- `README.md`: profile introduction, links, stack, featured projects.
- `assets/skills.json`: editable skill ratings (illustrative values; set your own).
- `assets/langmix.json`: editable programming-language ratings (not live percentages).
- `assets/projects.json`: only add repository names owned by `porwalyash438` for generated repository cards.
- `.github/workflows/metrics.yml`: account username and `Asia/Kolkata` timezone are configured.
- `scripts/banner/generate.py`: banner metadata is personalized. The included banner is a custom terminal-style SVG and does not require regeneration. If you regenerate it, install `scripts/banner/requirements.txt` dependencies first.

## Project ownership note
The Railway Reservation System link currently points to `vManav123/railway-reservation-system`, as that is the repository URL previously associated with the project. It is not owned by `porwalyash438`, so it is linked directly rather than configured as an owned-repository card. If you have your own fork or repository, update that link.
