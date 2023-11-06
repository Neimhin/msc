
One node on your Pi will be the ICN node that implements interoperability.

Each group builds its owns scenario, and the scenarios interoperate with each other via ICN nodes.

Naming Syntax
whoami

types of requests:
- get groups (not secured)
- get private groups
- get group meta data (syntax of naming, group name)
- if "shared_secret_key" is empty then don't use encryption
- we will use HTTP and restrict to just JSON

#### What goes in the JSON messages
**verbs/types of requests**
