# Log Scrubber

The aim of this experiment is to streamline the output log.

This experiment is a pre-rebot modifier that transforms the log based on three
orthogonal and combinable tags:

  * `inline`: Replace this keyword's callsite with its body.
  * `opaque`: Remove the keyword's body but keep non-assign messages.
  * `unroll`: Replace `FOR` and `WHILE` nodes with their children or their
    children's bodies.

## Implementation

This experiment implements a pre-rebot modifier to not affect the execution of
existing tests.

The `opaque` and  `unroll` tags are implemented in the `start_keyword` hook and
are fairly straightforward.

On the other hand, the `inline` transformation has to be done from the parent
to preserve the order of the parent's body's keywords. This is done by
always reconstructing every body, when a keyword tagged as `inline` is found
its body is appened to the parent's body, which is inefficient. If a keyword is
not run, it is never inlined as it does not have a body to inline.

Additionally, `BuiltIn.Run Keyword` is implicitly `inline`.

Note that it is not possible to inline keywords in pre-run modifiers because
the keyword's body is not (as far as i know) accessible at runtime, it is
created during test execution.

## Running

  robot --prerebotmodifier LogScrubber.py tests.robot

## Results

The results can be observed in the generated `log.html` file. This approach
seems to work well, but efficiency might be a concern for larger logs.
