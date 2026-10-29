# Movie content and media

The movie catalogue preserves its original 56 IDs. `enrichment.json` supplies cast, director and original release year. Each entry includes its source link. District entries are a snapshot retrieved on 29 October 2026; general film credits are curated against the corresponding Wikipedia film article. Names and dates are factual metadata. No critic ratings or fabricated votes were introduced.

`releases.json` contains five India release announcements sourced from the linked District detail pages on 29 October 2026. Dates can change; the app must show the snapshot date and source. Three announced titles release on 30 October 2026; King and Avengers: Doomsday are December announcements. They are not real cinema inventory and do not imply advance booking availability.

Poster files are promotional artwork owned by their respective film rights holders. `posterSource` and `posterRemote` retain the source page and actual retrieved asset URL. Local copies are resized to at most 600×900 for this non-commercial student movie catalogue. Do not present artwork as original CineSeat designs. Most poster images were visually inspected in a contact sheet. The Drishyam Hindi poster was corrected after detecting a Malayalam-edition mismatch.

Video buttons use retrieved YouTube URLs from District's trailer/teaser metadata or publisher trailers (YRF for Pathaan; Vidhu Vinod Chopra Films for 3 Idiots). `videos` preserves language and video type where available. Missing trailer links must have a clear unavailable state; never fabricate a video URL or label a search-results page as a teaser. No movie video is downloaded or hosted locally.

`poster-sources.json` is the supporting image-search source register. `scripts/enrich-movies.py` optionally refreshes local posters from the reviewed remote URLs; it does not replace the factual metadata.
