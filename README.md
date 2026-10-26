# Young Adult Age-Up Household Flow

`move_young_adult_without_noble_parent` processes the Sim after they age up to
young adult. Vacant lots are limited to residential lots. A spouse candidate
must be a human young adult of the opposite sex; an existing eligible spouse
is preferred, otherwise an eligible unmarried Sim who is not a parent, child,
or sibling is selected and married.

```mermaid
flowchart TD
    A["A Sim ages up to young adult"] --> B{"Has a noble career?"}
    B -- Yes --> C["Find a vacant residential lot in the current world"]
    C --> D{"Lot and new household available?"}
    D -- No --> X["Report failure; do not move"]
    D -- Yes --> E["Move Sim into the new household"]
    E --> F["Find an opposite-sex human young adult spouse"]
    F --> G{"Eligible spouse found and\nmarriage tuning available?"}
    G -- Yes --> H["Move spouse into household and marry them"]
    G -- No --> I["Report that no eligible spouse was found"]

    B -- No --> J{"Does a parent have a noble career?"}
    J -- Yes --> K{"Is the Sim the eldest child\namong that parent's children in this household?"}
    K -- Yes --> L["Keep Sim in the current household"]
    L --> M["Find eligible spouse, move them in, and marry them"]
    K -- No --> N["Move Sim to a vacant residential lot\non any world"]

    J -- No --> O{"Is this the only human young adult or adult\nin the current household?"}
    O -- Yes --> P["Keep Sim in the current household"]
    O -- No --> N
```
