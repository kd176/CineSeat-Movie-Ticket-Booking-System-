# CineSeat — shared cinema booking project

A public demo cinema with a Vinext/React frontend, Cloudflare Worker API and D1 SQL database. 56 seeded films, multiple shows per order, up to 8 seats per show, best-seat suggestions, private tickets and receipts, cancellations, FIFO group waiting lists, favourites and community votes.

Worldwide interest comes from Simkl's public trending feed and represents that community's viewing activity, not all global viewers. Daily, weekly and monthly boards are cached for an hour and identify stale results.

## Identity and permissions
Browsing is public. Booking and preferences require platform-owned Sign in with ChatGPT. Trusted identity headers identify users; all write endpoints enforce ownership and same-origin requests. `ADMIN_EMAIL` is a secret environment variable configured in hosting. Only that account can manage movies and record demo counter payments. Never trust a browser-provided user ID or payment amount.

## Data integrity
The `(show_key, seat)` primary key prevents duplicate seat claims. A D1 atomic batch commits every order, booking and seat claim together, or rolls everything back. Idempotency keys prevent repeat checkout. Prices and discounts are computed server-side in integer paise. Cancelling releases claims and attempts FIFO allocation. Waitlist bookings have payment pending.

## Running and checks
`npm ci`, `npm run db:generate` for intentional schema changes, `npm run build`. Hosting provisions the DB binding and applies schema-only migrations. Initial catalogue seeding happens server-side once. Follow the Sites workflow for publication.

Run `node tests/backend.mjs` and `node tests/frontend.mjs`. Backend tests use SQLite with foreign keys and transactions. Frontend tests exercise script adapters with DOM stubs; they do not replace real-browser layout testing.

## Demo boundaries
No money is charged. Tickets are project artifacts, not admission to actual cinemas. Shows, seat inventory, prices and some movie runtime slots are demonstration data. Payments and refunds are simulated. Existing browser-only accounts and test tickets are not imported into authenticated accounts. No email, SMS, payment gateway or real cinema integration is configured. Shows are interpreted in Asia/Kolkata; inventory refreshes every 20 seconds while the page is visible.

## Final project edition — October 2026
- Three fictional Delhi NCR theatres with deterministic, four-hour-slot schedules. A film has one daily performance per theatre. Physical screen/time slots are unique within each theatre for seeded films.
- Each performance fixes language/dubbing, subtitle availability, 2D/3D, projection and audio. HD/2K is separate from 2D/3D. All technology configurations and dubbed/3D variants are demo offerings, not statements about a commercial screening.
- 40 seats per new performance: Classic A–D, Premium E–F (+₹60), Recliner G–H (+₹200), plus theatre-specific format surcharge. The server calculates and validates the total in paise. Legacy bookings retain their original inventory.
- Booking/waitlist experience snapshots preserve theatre, screen, language, subtitles, formats and individual seat prices through cancellation, receipts, downloads and counter settlement.
- Community ratings are 1–10, one editable vote per authenticated account. No fabricated starter ratings.
- The `server/enrichment.json` and `server/releases.json` data files provide attributed movie details and a dated India release snapshot. The week view means Monday–Sunday in India; upcoming means after today's India date.
- Print-ready submission overview and demo script: `/project-guide.html`.

### Source orientation
`server/api.mjs`: HTTP handling and transaction logic. `server/experiences.mjs`: theatre configurations, deterministic schedules and pricing. `db/schema.ts` / `drizzle/`: durable schema and migrations. `public/web/final.js` / `final.css`: final discovery and theatre-selection UI layered on existing features. `tests/backend.mjs`: SQLite-backed integration checks. `tests/frontend.mjs`: DOM-stub script smoke tests, not a replacement for real-browser layout QA.

### Run the submitted source locally
1. Install Node.js 22.13 or newer, then run `npm ci` in the extracted project folder.
2. Run `npm run build` once to generate the local Worker configuration.
3. On a fresh local database, apply these files in order (do not repeat an already applied migration):
   ```sh
   node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_woozy_frightful_four.sql
   node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0001_thankful_amphibian.sql
   ```
4. Run `npm run dev` and open its printed loopback URL. The portable starter provides a local-only mock ChatGPT identity for development. Hosted authentication remains platform-owned; the mock is never deployed.
5. For local administrator testing only, set `ADMIN_EMAIL=seedy@sites.test` in an ignored `.dev.vars` file. Never put real secrets into source control. Use the signed-in site owner's account for deployed administration.
6. Run `node tests/backend.mjs` and `node tests/frontend.mjs` for automated checks. These use isolated test state and do not modify hosted bookings.

### Final verification notes
Desktop browser QA verified discovery posters, this-week announcements, credits/trailer source links, three theatre performances, adjacent recliner suggestions and the correctly priced bag. Backend integration tests cover authenticated checkout and ownership; the hosted account sign-in flow cannot be completed without the visitor's own account. Mobile layouts use responsive CSS but were not separately tested on a physical phone.
