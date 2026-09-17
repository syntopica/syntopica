# TODO

## Onboarding

- [ ] Model identifiers are still constants under `clips/src/models/`, so which
  model a transport asks for is not configuration. The `runners` block now
  selects the transport and the clips README says plainly that the model inside
  it does not come from the instance. Smallest next step: decide whether a
  model belongs in `syntopica.config.json` at all, or whether the transport is
  the right granularity and the claim should stay retired.
