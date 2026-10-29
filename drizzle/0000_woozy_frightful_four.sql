CREATE TABLE `bookings` (
	`id` integer PRIMARY KEY NOT NULL,
	`order_id` integer NOT NULL,
	`user_id` text NOT NULL,
	`movie_id` integer NOT NULL,
	`title` text NOT NULL,
	`show_key` text NOT NULL,
	`show_date` text NOT NULL,
	`show_time` text NOT NULL,
	`seats_json` text NOT NULL,
	`price_cents` integer NOT NULL,
	`paid_cents` integer NOT NULL,
	`status` text NOT NULL,
	`payment` text NOT NULL,
	`mode` text NOT NULL,
	`created` text NOT NULL,
	`cancelled` text,
	FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`user_id`) REFERENCES `profiles`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`movie_id`) REFERENCES `movies`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE INDEX `bookings_owner` ON `bookings` (`user_id`);--> statement-breakpoint
CREATE INDEX `bookings_show` ON `bookings` (`show_key`);--> statement-breakpoint
CREATE TABLE `api_cache` (
	`key` text PRIMARY KEY NOT NULL,
	`data` text NOT NULL,
	`updated` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `seat_claims` (
	`show_key` text NOT NULL,
	`seat` integer NOT NULL,
	`booking_id` integer NOT NULL,
	PRIMARY KEY(`show_key`, `seat`),
	FOREIGN KEY (`booking_id`) REFERENCES `bookings`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `favourites` (
	`user_id` text NOT NULL,
	`movie_id` integer NOT NULL,
	PRIMARY KEY(`user_id`, `movie_id`),
	FOREIGN KEY (`user_id`) REFERENCES `profiles`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`movie_id`) REFERENCES `movies`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `rate_limits` (
	`key` text PRIMARY KEY NOT NULL,
	`count` integer NOT NULL,
	`window` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `app_meta` (
	`key` text PRIMARY KEY NOT NULL,
	`value` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `movies` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`name` text NOT NULL,
	`data` text NOT NULL,
	`price_cents` integer NOT NULL,
	`seats` integer NOT NULL,
	`active` integer DEFAULT 1 NOT NULL,
	`version` integer DEFAULT 1 NOT NULL
);
--> statement-breakpoint
CREATE TABLE `orders` (
	`id` integer PRIMARY KEY NOT NULL,
	`user_id` text NOT NULL,
	`request_key` text NOT NULL,
	`request_hash` text NOT NULL,
	`status` text NOT NULL,
	`payment` text NOT NULL,
	`mode` text NOT NULL,
	`total_cents` integer NOT NULL,
	`discount_cents` integer NOT NULL,
	`snacks` integer NOT NULL,
	`snack_cents` integer NOT NULL,
	`created` text NOT NULL,
	FOREIGN KEY (`user_id`) REFERENCES `profiles`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `orders_request` ON `orders` (`user_id`,`request_key`);--> statement-breakpoint
CREATE TABLE `profiles` (
	`id` text PRIMARY KEY NOT NULL,
	`name` text NOT NULL,
	`email` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `votes` (
	`user_id` text NOT NULL,
	`movie_id` integer NOT NULL,
	PRIMARY KEY(`user_id`, `movie_id`),
	FOREIGN KEY (`user_id`) REFERENCES `profiles`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`movie_id`) REFERENCES `movies`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `waiting` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`user_id` text NOT NULL,
	`movie_id` integer NOT NULL,
	`show_key` text NOT NULL,
	`show_date` text NOT NULL,
	`show_time` text NOT NULL,
	`seat_count` integer NOT NULL,
	`created` text NOT NULL,
	FOREIGN KEY (`user_id`) REFERENCES `profiles`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`movie_id`) REFERENCES `movies`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `waiting_user_show` ON `waiting` (`user_id`,`show_key`);