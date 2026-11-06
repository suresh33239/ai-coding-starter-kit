# Optional data inventory — for software that stores user information

**Template, not an audit result.** This is useful for apps with a database, saved documents, accounts, cloud synchronization or backups. **Skip it for stateless scripts and tools** that store no persistent user data.

The AI should inspect the actual code and existing storage before filling it. It should ask the owner only about important unresolved privacy or retention decisions. Mark unknown items **Not verified**—never guess, and never put actual personal records, secrets, credentials or customer data here.

| Data collection / purpose | Owner and who may view/edit | Sensitivity | Where stored and any network disclosure | Backup/restore and export | Retention/deletion | Failure/recovery behavior | Evidence/status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Example: saved notes | User's own account; access rules TBD | May contain personal text | Device only / Not verified | Not verified | Not verified | Unreadable data must not be overwritten | Example only — not audited |

## For each new persistent data type

1. Find the **existing** storage and ownership pattern first. Reuse it where appropriate; don't create a second source of truth.
2. Record if the data is local, backed up, synced, uploaded to third parties, exported, deleted or excluded from recovery. Explain important exclusions to the owner.
3. Identify how the app handles failed reads, partial writes, corruption, missing permissions, account switching and restore **where applicable**. An unreadable record is not an empty one; never overwrite it with a default merely to keep the app running.
4. Define the smallest relevant test: a save/read-back, failed write, backup/restore, access isolation, or deletion check. Use **synthetic test data** only.
5. Review sensitive-data disclosure and retention requirements for the intended platform and release channel; distinguish what is implemented from what is merely planned.

This inventory records behavior and decisions; it does **not** mandate encryption, cloud sync, a database, logging, or other infrastructure for a simple project. Changes to stored data, permissions, encryption, deletion or migrations still require separate owner approval.
