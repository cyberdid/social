# Gemini keyframe pilot — 2026-11-08

## Scope and result

One locally available TikTok clip was used for a bounded visual pilot. The source account and caption were withheld from the model prompt. Gemini 3.8 Flash ran with `high` effort through the user's Agy CLI. It reviewed three extracted frames at 0, 5 and 10 seconds from a 15.278-second clip.

The model described an indoor scene with a person in bright pink-and-black clothing, other people in police-marked clothing, and a corridor/doorway across the sampled frames. A visual spot-check of those same frames supports this broad description. It does **not** establish continuous movement between frames, legal status, identity, location, recording date, intent, cause, or connection to the incident. Text overlaid on the video makes a legal-procedure assertion and uses a claimed professional label; those are claims made by the publisher and are not established by the images.

The output remains a **candidate visual observation**, not a verified fact or provider-accuracy benchmark. No source caption, audio, external website, or metadata was used in this pass. The model response contains more detailed visible descriptors than needed for analysis; those details and individual identifiers are intentionally omitted here.

## Provenance

- Source locator: `https://www.tiktok.com/@slidstvo.info/video/7704350612959317255`
- Duration: 15.278005 seconds
- Source SHA-256: `4da4c42d76324b0c4aa7828fcce1bfcfaf06e045f889ebe5276083896e4f91ba`
- Frame at 0 ms SHA-256: `7535555aaa05e1ab12516af34505e5a67a817cbf49c966dcc0f033cfb0cc4e0d`
- Frame at 5,000 ms SHA-256: `fba7c72db30e8e35945c515ccc4070316a9c8dc854be364080cc0cb9b89a4c82`
- Frame at 10,000 ms SHA-256: `a105db529da0ff6669bfc6dba9084e491b33af89d4ccf043f56500165b59a8bd`
- Pipeline run manifest SHA-256: `b85fdba10d4ebf9ad8f80c901eee909d3b85a21b0c9cff82c5e875e06a2c30ec`
- Private local model response: `/home/cyberdid/Downloads/SocialIncidentVideos/semantic-pilot/gemini-3.8-flash-high-keyframes-7704350612959317255.json`
- Private local run receipt: `/home/cyberdid/Downloads/SocialIncidentVideos/runs/tiktok-video-pipeline-2026-11-08/run_manifest.json`

## Token use and permission boundary

The first full-video Agy attempt was blocked in headless mode when it requested `file` and `ffprobe`; it returned no analysis and reported 55,606 total tokens. A second, isolated keyframe pass used a session-only allow rule for the read-only `file` command; it returned an observation and reported 36,703 total tokens. The combined Agy-reported total was 92,309 tokens across these two attempts. No broad permission bypass was enabled. Agy reported no denied actions for the successful keyframe pass.

This token use is too high to justify sending all videos through this model. The current runner therefore keeps semantic model analysis optional and selective; it does not call Agy/Gemini automatically.

## Limits

- Three still frames are not a continuous video review; action between them is unresolved.
- The model did not assess audio, source claims, event identity, location, or filming date.
- The visible overlay is evidence that the claim was presented in the clip, not evidence that the claim is true.
- The single-clip pilot has no independently adjudicated benchmark and cannot estimate model precision or recall.
- The run does not meet the master plan's provider-benchmark gate. It records feasibility and cost only.
