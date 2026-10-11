# muse notifications and reminders

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: skills roster + schema (`Notification` event) + plugin families.

`Notification` is a real hook event. Reminder skills (`tbh-reminders`
family: memory, skill, todo, goal, verify, scope reminders) inject
system-reminders at safe points. Plugins can ship a `reminders` capability.
`voice` transcribes audio clips to text (notification-adjacent input).
