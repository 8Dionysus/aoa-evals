# Experience certification gate integrity v1

This fixture family stays public-safe and bounded.

Case families:

- review-ready candidate packet
- missing authority packet
- missing regression packet
- missing rollback packet
- recharter-required compatibility packet

Replacement cases must preserve the same authority ceiling: the eval may say a
packet is ready for authorized operator review, but it must not certify,
approve release, promote a deployment ring, or permit durable rollback.
