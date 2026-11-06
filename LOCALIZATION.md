# Localization from the foundation, without translating everything at once

Localize the **architecture** from the beginning; translate additional languages when there is a real user need and a review plan. Retrofitting hard-coded text late can be expensive, but translating every hypothetical locale on day one is also wasteful.

## Foundation rules

- Keep all user-visible strings in one framework-appropriate resource system: e.g. Android string resources, Apple string catalogs, or web i18n catalogs.
- Use stable descriptive keys, plural/quantity support, format placeholders, and reusable text. Never concatenate translated sentence fragments.
- Use locale-aware dates, numbers, currency, sorting, measurements, units and time zones where relevant. Keep **stored data** locale-neutral.
- Plan for longer strings, different scripts, right-to-left layouts, accessibility labels, and text scaling.
- Make the base language complete before scaling. Add only priority locales approved for the release.
- Machine translation is a draft: validate placeholders, XML/JSON syntax, truncation, meaning, and especially safety, finance, privacy and medical language. Be transparent when native-language review is unavailable.
- Keep translation scope tied to accepted features; do not translate obsolete or unapproved screens.

## Localization plan

| Item | Decision |
| --- | --- |
| Base language | TBD |
| Launch locales | TBD |
| Later locales | TBD |
| Translation method and review capacity | TBD |
| Locale formatting and RTL testing | TBD |
| Language switch / fallback behavior | TBD |

**Stage checkpoints:** (1) extracted resources and base strings; (2) priority launch translations; (3) focused UI and functional checks; (4) release validation. Do not hold up a usable prototype to fully translate every possible language.
