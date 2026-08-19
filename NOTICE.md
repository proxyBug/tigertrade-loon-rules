# Third-Party Notices and Data Provenance

This repository maintains its own source lists and generator. Domain names are factual network identifiers and are cross-checked against official endpoints, live DNS/TLS/HTTP observations, and the community datasets below. No upstream generator code, documentation prose, or traffic payloads are copied into this repository.

## Community comparison sources

### v2fly/domain-list-community

- Repository: https://github.com/v2fly/domain-list-community
- Files consulted: `data/itiger`, `data/futu`
- Audited snapshot: `5e1035c6f2458efa45ac825a798960ed0c310110`
- License reported by GitHub: MIT
- License text: https://github.com/v2fly/domain-list-community/blob/master/LICENSE

### blackmatrix7/ios_rule_script

- Repository: https://github.com/blackmatrix7/ios_rule_script
- Dataset consulted: `rule/Loon/TigerFintech/TigerFintech.list`
- Audited snapshot: `86ada72372ec0586be75901f47d5ccca6e28c655`
- License reported by GitHub: GPL-2.0
- License text: https://github.com/blackmatrix7/ios_rule_script/blob/master/LICENSE

The blackmatrix7 dataset was used as a discovery and comparison source. Candidate domains were independently reviewed against current network behavior and additional public evidence before inclusion. Its source code and documentation are not incorporated here.

## Official sources

- Tiger Trade runtime/bootstrap configuration: https://up.play-analytics.com/
- Pinned Tiger runtime evidence matrix: `evidence/tiger-runtime-2026-08-20.json`
- Pinned community comparison matrix: `evidence/community-comparison-2026-08-20.json`
- Moomoo OpenAPI documentation: https://openapi.moomoo.com/moomoo-api-doc/en/
- Futu OpenAPI documentation: https://openapi.futunn.com/futu-api-doc/en/
- Futu Trustee corporate confirmation: https://www.futuhk.com/en/about-us/newsroom/futu-trustee-launches-groundbreaking-futu-pension-family-trust

## Project license

The original code, tests, documentation, and independently maintained rule compilation in this repository are released under the repository's MIT License. Third-party repositories remain governed by their respective licenses.
