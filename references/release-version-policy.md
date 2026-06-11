# Release Version Policy

The initial public adapter version was `1.0.0`. Only the exact current numeric
tag is supported. A `VERSION` file alone is not enough for release; the tag and
GitHub Release must point to the same commit that the root control plane pins.

Minor and major movement is owner-directed. Patch releases are used for normal
compatible fixes after `1.0.0`.
