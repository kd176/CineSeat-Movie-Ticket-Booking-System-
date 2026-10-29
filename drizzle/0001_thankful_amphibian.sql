CREATE TABLE `ratings` (
	`user_id` text NOT NULL,
	`movie_id` integer NOT NULL,
	`value` integer NOT NULL,
	PRIMARY KEY(`user_id`, `movie_id`),
	FOREIGN KEY (`user_id`) REFERENCES `profiles`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`movie_id`) REFERENCES `movies`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
ALTER TABLE `bookings` ADD `experience_json` text;--> statement-breakpoint
ALTER TABLE `waiting` ADD `experience_json` text;