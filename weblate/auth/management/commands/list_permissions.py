# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from weblate.auth.data import ACL_GROUPS, GLOBAL_PERMISSIONS, PERMISSIONS, ROLES
from weblate.utils.management.base import BaseCommand

PERM_NAMES = {
    "billing": "Billing (see :ref:`billing`)",
    "change": "Changes",
    "comment": "Comments",
    "component": "Component",
    "glossary": "Glossary",
    "machinery": "Automatic suggestions",
    "memory": "Translation memory",
    "project": "Projects",
    "reports": "Reports",
    "screenshot": "Screenshots",
    "source": "Source strings",
    "suggestion": "Suggestions",
    "translation": "Translations",
    "upload": "Uploads",
    "unit": "Strings",
    "vcs": "VCS",
}


class Command(BaseCommand):
    help = "List permissions"

    def handle(self, *args, **options):
        """List permissions."""
        self.stdout.write("Managing per-project access control\n\n")

        for name in ACL_GROUPS:
            self.stdout.write(f"{name}\n\n\n")

        self.stdout.write("\n\n")

        last = ""

        table = []
        rows = []

        for key, name in PERMISSIONS:
            base = key.split(".")[0]
            if base != last:
                if last:
                    table.append((PERM_NAMES[last], rows))
                last = base
                rows = []

            rows.append(
                (
                    name,
                    ", ".join(
                        f"`{name}`" for name, permissions in ROLES if key in permissions
                    ),
                )
            )
        table.append((PERM_NAMES[last], rows))

        rows = [(name, "") for _key, name in GLOBAL_PERMISSIONS]
        table.append(("Site wide privileges", rows))

        len_1 = max(len(group) for group, _rows in table)
        len_2 = max(len(name) for _group, rows in table for name, _role in rows)
        len_3 = max(len(role) for _group, rows in table for _name, role in rows)

        sep = f"+-{'-' * len_1}-+-{'-' * len_2}-+-{'-' * len_3}-+"
        blank_sep = f"+ {' ' * len_1} +-{'-' * len_2}-+-{'-' * len_3}-+"
        row = f"| {{:{len_1}}} | {{:{len_2}}} | {{:{len_3}}} |"
        self.stdout.write(sep)
        self.stdout.write(row.format("Scope", "Permission", "Roles"))
        self.stdout.write(sep.replace("-", "="))
        for scope, rows in table:
            number = 0
            for name, role in rows:
                if number:
                    self.stdout.write(blank_sep)
                self.stdout.write(row.format(scope if number == 0 else "", name, role))
                number += 1
            self.stdout.write(sep)
